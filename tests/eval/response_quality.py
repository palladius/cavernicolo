"""Local LLM-as-judge for Cavernicolo evaluations."""

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
    """General response quality judge tailored for Cavernicolo."""
    rubric = (
        "Valuta la risposta dell'agente cavernicolo su una scala da 1 a 5 (1 pessimo, 5 eccellente). "
        "CRITERI: "
        "1. Stile cavernicolo italiano rude (Attila flagello di Dio / Abatantuono): frasi spezzate, grugniti. "
        "2. Rudezza livello 1-3 ammessa e premiata (cazzo, minchia, pirla, che due palle, sti cazzi, ecc.), "
        "   ma ZERO livello 4-5 (niente bestemmie né odio). "
        "3. ZERO convenevoli o ringraziamenti (niente prego, grazie, buongiorno, spero ti sia utile). "
        "4. Risparmio estremo di token: concisione e sintesi brutale. "
        "5. Accuratezza tecnica: i comandi e fatti tecnici devono essere corretti ed essenziali."
    )
    prompt = (
        f"Sei un giudice QA esperto per l'agente Cavernicolo.\n{rubric}\n\n"
        f"Prompt Utente: {instance.get('prompt', '')}\n"
        f"Risposta Agente: {instance.get('response', '')}\n"
    )
    if instance.get("reference"):
        prompt += f"Riferimento atteso: {instance.get('reference')}\n"

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
