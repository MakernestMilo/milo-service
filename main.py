"""Entry point. Render runs `python main.py` (or `uvicorn main:app`); both work."""
import os

from milo.app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), proxy_headers=False, access_log=False)
