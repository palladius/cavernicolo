"""Local LLM-as-judge for Cavernicolo text compressor evaluations."""

import os
import threading
from google import genai
from google.genai import types
from pydantic import BaseModel

_local = threading.local()
MODEL = os.environ.get("EVAL_JUDGE_MODEL", "gemini-2.5-flash")


class _Verdict(BaseModel):
    score: int  # 1-5
    explanation: str


def _client() -> genai.Client:
    client = getattr(_local, "client", None)
    if client is None:
        client = _local.client = genai.Client()
    return client


def evaluate(instance):
    """Judge whether Cavernicolo compresses the input text into rude Italian caveman without answering it."""
    rubric = (
        "Valuta l'output dell'agente Cavernicolo Compressore su una scala da 1 a 5 (1 pessimo, 5 eccellente). "
        "CRITERI FONDAMENTALI: "
        "1. COMPRESSIONE E NON RISPOSTA: L'agente è un FILTRO/COMPRESSORE DI TESTO. "
        "   NON deve rispondere alle domande dell'utente (es. se l'input chiede 'come si fa commit in git?', "
        "   l'output deve essere la domanda compressa tipo 'Come cazzo fare commit git?' e NON la spiegazione 'git commit -m'). "
        "   Se l'agente risponde alla domanda invece di comprimerla, dai 1! "
        "2. STILE CAVERNICOLO ITALIANO RUDE: Frasi spezzate, verbi all'infinito, grugniti (UGH, AÒ), rudezza livello 1-3 "
        "   (cazzo, minchia, merda, pirla, fanculo), ZERO livello 4-5 (no bestemmie). "
        "3. ZERO CONVENEVOLI: Qualsiasi 'cortesemente', 'grazie', 'buongiorno' nell'input deve essere spazzato via. "
        "4. RISPARMIO TOKEN & PRESERVAZIONE TECNICA: L'output deve avere molti meno token dell'input ma conservare i termini tecnici chiave."
    )
    prompt = (
        f"Sei un giudice QA esperto per il filtro di compressione Cavernicolo.\n{rubric}\n\n"
        f"Testo Verboso in Input: {instance.get('prompt', '')}\n"
        f"Testo Compresso dall'Agente: {instance.get('response', '')}\n"
    )
    if instance.get("reference"):
        prompt += f"Esempio di Compressione Attesa: {instance.get('reference')}\n"

    try:
        response = _client().models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                response_mime_type="application/json",
                response_schema=_Verdict,
            ),
        )
        verdict = response.parsed
        if verdict is None:
            return {"score": 3, "explanation": response.text or "No parsed output"}
        return {"score": max(1, min(5, verdict.score)), "explanation": verdict.explanation}
    except Exception as e:
        return {"score": 3, "explanation": f"Eval error: {e}"}
