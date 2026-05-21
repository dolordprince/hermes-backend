import os, json, urllib.request, urllib.error, traceback
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._json(200, {"status": "online", "agent": "DavTeam", "model": "gemini-2.0-pro-exp-02-05"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data   = json.loads(self.rfile.read(length))
            key    = os.environ.get("GLAMA_API_KEY", "")

            if not key:
                return self._json(500, {"error": "GLAMA_API_KEY not set"})

            payload = json.dumps({
                "model": "gemini-2.0-pro-exp-02-05",
                "messages": [
                    {"role": "system", "content": "You are DavTeam Agent built by David. Expert in ARM64/Termux, FastAPI, Bun, Android, SaaS."},
                    {"role": "user",   "content": data.get("message", "hi")}
                ],
                "max_tokens": 1024
            }).encode()

            req = urllib.request.Request(
                "https://gateway.glama.ai/v1/chat/completions",
                data=payload,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                }
            )
            res   = urllib.request.urlopen(req, timeout=25)
            reply = json.loads(res.read())["choices"][0]["message"]["content"]
            self._json(200, {"reply": reply})

        except urllib.error.HTTPError as e:
            self._json(500, {"error": f"Glama HTTP {e.code}", "body": e.read().decode()})
        except Exception as e:
            self._json(500, {"error": str(e), "trace": traceback.format_exc()})

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
