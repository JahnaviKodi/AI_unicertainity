# AI That Knows When to Say I Don't Know

An AI system with uncertainty awareness and abstention capability.

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Run Pipeline
python -c "from src.pipeline import Pipeline; p = Pipeline(); print(p.run('your question here'))"

## Run Tests
pytest tests/ -v

## Run Evaluation
python evaluation\evaluate.py

## Modules
- src/confidence_scorer.py
- src/boundary_detector.py
- src/decision_engine.py
- src/response_generator.py
- src/pipeline.py

## Docs
- docs/ux_guidelines.md
- docs/technical_docs.md