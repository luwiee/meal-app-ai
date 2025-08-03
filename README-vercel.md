# Vercel Deployment Instructions

This project is now Vercel-ready!

## How it works
- The Flask app is exposed via `api/index.py` as required by Vercel's Python runtime.
- All dependencies are listed in `requirements.txt`.
- The `vercel.json` file ensures the correct runtime and routes all requests to the Flask app.
- Templates are served from the `templates/` directory as usual.

## Deploy Steps
1. Push this repository to GitHub (or your preferred Git provider).
2. Go to [Vercel](https://vercel.com/) and import your repository.
3. Vercel will auto-detect the Python project and deploy it using the configuration provided.
4. Your app will be available at the generated Vercel URL.

## Notes
- If you need to customize routes or add static files, update `vercel.json` accordingly.
- For local testing, run `python app.py` as before.
