from pathlib import Path
from fastapi import FastAPI
from starlette.responses import FileResponse, HTMLResponse

REPO_ROOT = Path(__file__).parent.parent

app = FastAPI()


@app.get("/")
async def root():
    return HTMLResponse((REPO_ROOT/"resources/index.html").read_text())

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(REPO_ROOT/"resources/favicon.ico")
