# Cavernicolo (🥩 UGH!)

Agente Cavernicolo carlessiano rude in italiano, ispirato al tutorial [agents-cli quickstart](https://google.github.io/agents-cli/guide/quickstart-tutorial/) e ad Attila flagello di Dio (Diego Abatantuono).
Risparmio estremo di token, zero ringraziamenti, rudezza controllata (livello 1-3).
Funziona sia come **agente ADK / agents-cli**, sia come **filtro Unix** (`cat ARTICLE.md | cavernicolo`), sia come **skill**.

## Quickstart

```bash
# 1. Filtro Unix da pipeline
cat ARTICLE.md | cavernicolo

# 2. Da argomento
cavernicolo "Spiegami come fare un commit in git"

# 3. Via agents-cli
agents-cli run "Spiegami come deployare su Cloud Run"

# 4. Esecuzione suite di valutazione (evals)
cavernicolo --eval
# oppure direttamente:
agents-cli eval run --dataset tests/eval/datasets/cavernicolo-dataset.json --config tests/eval/eval_config.yaml
```

## Architettura

- `app/agent.py`: Definizione del `root_agent` ADK con istruzioni di compressione cavernicolo.
- `bin/cavernicolo`: Script eseguibile Unix filter (collegato in `~/.local/bin/cavernicolo`).
- `tests/eval/`: Suite di valutazione con LLM-as-judge (`response_quality.py`), metriche di brevità e assenza convenevoli.
- `cavernicolo_logo.png`: Mascotte Diego Abatantuono cavernicolo generata con Nano Banana Pro / Gemini Image.
- `.agents/skills/cavernicolo/SKILL.md`: Skill Cavernicolo per coding agents.
