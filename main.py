import os, json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent import chat, MODEL
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="DavTeam Agent", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health():
    return JSONResponse({"status": "online", "model": MODEL})

@app.websocket("/ws")
async def ws_chat(ws: WebSocket):
    await ws.accept()
    history = []
    try:
        while True:
            data = await ws.receive_text()
            msg  = json.loads(data) if data.startswith("{") else {"message": data}
            reply = await chat(history, msg["message"])
            await ws.send_text(reply)
    except WebSocketDisconnect:
        pass

@app.post("/chat")
async def rest_chat(body: dict):
    history = body.get("history", [])
    reply   = await chat(history, body["message"])
    return {"reply": reply, "history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
