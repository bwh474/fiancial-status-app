# Financial Status Visualizer

This project uses local FRED CSV files in `data/` and Altair charts in `visualizer.ipynb` to summarize U.S. household financial pressure.

The main dashboard file to open is:

`html_charts/financial_pressure_dashboard.html`

The core household pressure score is intentionally limited to Debt Service Ratio, Personal Saving Rate, and Credit Card Delinquency Rate. Other indicators are context only.

## Heroku hosting

This repository includes Heroku support files for serving the generated dashboard:

- `app.py`
- `Procfile`
- `requirements.txt`
- `.python-version`
- `.slugignore`
- `app.json`

Run locally with:

```bash
python3 app.py
```

Then open `http://localhost:5000`.

See `HEROKU_DEPLOYMENT.md` for deploy steps.
