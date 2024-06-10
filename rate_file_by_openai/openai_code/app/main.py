import logging, os, time

from openai import OpenAI

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, HTMLResponse

from . import openai_config

app = FastAPI(title="ORC API",version="0.0.1")

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

logger = logging.getLogger("main")

@app.get("/")
async def healthcheck():
    return {"status": True}

@app.post("/upload")
async def create_upload_file(file: UploadFile):
    if not file:
        return {"error": "No file uploaded"}
    if not (file.filename.endswith(".md") or file.filename.endswith(".html")):
        return {"error": "Wrong file format"}
    file_location = os.path.join('/tmp/', file.filename)
    with open(file_location, "wb+") as file_object:
        while content := await file.read(1024*1024):  # Read in chunks of 1MB
            file_object.write(content)
    return get_response(file_location)


def get_response(file_location):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_config.OPENAI_TOKEN, # OPENAI_TOKEN from file openai_config.py
    )

    f = open(file_location, "r")
    file_content=f.read()
    f.close()

    criteria_file = open("/opt/app/criteria.md", "r")
    criteria_content=criteria_file.read()
    criteria_file.close()

    response = client.chat.completions.create(
        model=openai_config.OPENAI_MODEL,  # Use the appropriate model identifier for GPT-4
        messages=[
    {"role": "system", "content": f"{openai_config.OPENAI_MESSAGES_SYSTEM_CONTENT}:\n{criteria_content}"},
    {"role": "user", "content": f"{openai_config.OPENAI_MESSAGES_USER_CONTENT}\n{file_content}"}
])
    
    return str(response.choices[0].message.content)
