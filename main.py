import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY", ""),
)

MODEL = os.environ.get("MODEL", "llama-3.3-70b-versatile")
SYSTEM = {"role": "system", "content": "You are DavTeam Agent built by David. Expert in ARM64/Termux, FastAPI, Bun, Android, SaaS."}

@app.get("/health")
async def health():
    return JSONResponse({"status": "online", "key_set": bool(os.environ.get("GROQ_API_KEY")), "model": MODEL})

@app.post("/chat")
async def rest_chat(body: dict):
    history = list(body.get("history", []))
    history.append({"role": "user", "content": body["message"]})
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[SYSTEM, *history],
        temperature=0.7,
        max_tokens=1024,
    )
    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return {"reply": reply, "history": history}
