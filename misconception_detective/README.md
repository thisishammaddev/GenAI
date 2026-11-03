# Misconception Detective

A multi-agent learning system that diagnoses patterns in wrong quiz answers, explains the likely mix-up, and offers a targeted retest.

## How it works

1. The learner picks a track and answers eight curated questions.
2. The grading agent scores the answers and maps each distractor to a specific misconception.
3. The concept-coach agent identifies the focus topic and calls the `concept_guide` tool for teaching ground truth.
4. The practice-planner agent prepares a short follow-up question tied to the learner's weak concept.
5. The app displays the final diagnosis, the verified concept guide, and a practice prompt.

The grading layer remains deterministic. The LLM-backed agents only generate coaching and practice guidance. If the model call fails, the app still shows the score, the verified concept guide, and the practice question.

## Run

From the repository root, install dependencies:

```powershell
.\venv\Scripts\python.exe -m pip install -r misconception_detective\requirements.txt
cd misconception_detective
python -m streamlit run app.py
```

The project disables Streamlit's file watcher. In a shared environment with `transformers` installed, its module scan may otherwise report missing optional `torchvision` modules. Restart the app after editing code.

The root `.env` file needs `GOOGLE_API_KEY`. You may set `MISCONCEPTION_MODEL` to a Gemini model available to your account. The default is `gemini-3.6-flash`.

Do not commit `.env` or share API keys.
