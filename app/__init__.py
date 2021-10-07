from pathlib import Path
from math import sqrt

import httpx

from jinja2 import Template
from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse, HTMLResponse

REPO_ROOT = Path(__file__).parent.parent

app = FastAPI()

# lat, long
NAME_LUT = {
    (51.457430, -2.128658): "Huw",
    (52.042024, -0.762321): "Rob",
    (51.485020, -0.035252): "James",
    (51.442795, -0.849887): "Ben",
    (51.432219, -0.958467): "Russell",
    (51.466150, -0.924106): "Ibs"
}

def dist(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    return sqrt(x**2 + y**2)

def get_name(loc):
    smallest = 10000000
    name = ""
    for name_loc, this_name in NAME_LUT.items():
        temp = dist(loc, name_loc) 
        if temp < smallest:
            smallest = temp
            name = this_name
    return name


@app.get("/")
async def root():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://api.ip2loc.com/yWECZIoB3U5DtW26IPwGdPxDjajpV3p3/detect')
    
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Item not found")

    content = r.json()
    lat = content["location"]["latitude"]
    lon = content["location"]["longitude"]
    name = get_name((lat, lon))

    t = Template((REPO_ROOT/"resources/index.html.in").read_text())

    return HTMLResponse(t.render(name=name))

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(REPO_ROOT/"resources/favicon.ico")
