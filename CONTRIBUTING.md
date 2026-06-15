# Contributing to CareGraph

Thanks for your interest!

## How to contribute
1. Fork the repo and create a feature branch.
2. Set up your environment:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r docker/requirements.txt
   ```
3. Run the demo locally (`streamlit run app/ui.py`).
4. Format & lint (optional):
   ```bash
   ruff format .
   ruff check .
   ```
5. Open a pull request with a clear description and screenshots (if UI changes).

## Code style
- Python 3.11+
- Keep functions small and well‑documented.
- Avoid real PHI; only synthetic data is allowed in this repo.

## Security
See `SECURITY.md`. Report issues privately.
