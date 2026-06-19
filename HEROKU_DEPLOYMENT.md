# Heroku Deployment Notes

This project is ready to deploy as a small Python app that serves the generated dashboard HTML. Heroku serves the existing files in `html_charts/`; it does not rerun `visualizer.ipynb` during app startup.

## Files Added

- `app.py`: standard-library web server for the generated dashboard.
- `Procfile`: declares the Heroku `web` process.
- `requirements.txt`: intentionally dependency-free, but present so Heroku detects a Python app.
- `.python-version`: pins the Heroku Python runtime to Python 3.12.
- `.slugignore`: keeps notebooks, raw data, virtualenvs, and archived outputs out of the Heroku slug.
- `.gitignore`: keeps local/editor/generated clutter out of Git.
- `app.json`: optional Heroku app metadata.

## Local Test

Run:

```bash
python3 app.py
```

Then open:

```text
http://localhost:5000
```

Useful routes:

- `/`: main dashboard.
- `/dashboard`: same main dashboard.
- `/charts/`: index of standalone chart HTML files.
- `/healthz`: simple health check.

## Deploy

If this folder is not already a Git repository, initialize it first:

```bash
git init
git add .
git commit -m "Prepare dashboard for Heroku"
```

Create the Heroku app:

```bash
heroku login
heroku create your-app-name
```

Deploy:

```bash
git push heroku main
```

If your local branch is named `master`, use:

```bash
git push heroku master:main
```

Open the deployed app:

```bash
heroku open
```

## Updating the Dashboard Later

After changing the notebook or refreshing FRED CSV files, rerun `visualizer.ipynb` so `html_charts/financial_pressure_dashboard.html` is regenerated. Commit the updated `html_charts/` files and push to Heroku again.
