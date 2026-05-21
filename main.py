import os, json, urllib.request
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"status": "online", "agent": "DavTeam"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length  = int(self.headers.get("Content-Length", 0))
        data    = json.loads(self.rfile.read(length))
        key     = os.environ.get("GROQ_API_KEY", "")
        model   = os.environ.get("MODEL", "llama-3.3-70b-versatile")

        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "You are DavTeam Agent built by David."},
                {"role": "user",   "content": data.get("message", "hi")}
            ],
            "max_tokens": 1024
        }).encode()

        req   = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        res   = urllib.request.urlopen(req, timeout=30)
        reply = json.loads(res.read())["choices"][0]["message"]["content"]

        out = json.dumps({"reply": reply}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(out)
