from fastapi import FastAPI, WebSocket, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
# from typing import List # this will be for the multiple documents later on
from package import logger
import uvicorn

# run with --reload
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory 
templates = Jinja2Templates(directory="templates")

@app.get('/')
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello World"})

@app.post('/uploadfile')
async def handle_files(file: UploadFile = File(...)):
    content = await file.read()
    logger.info(content)
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)