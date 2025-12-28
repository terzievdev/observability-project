from fastapi import FastAPI, Request
import uvicorn
import json
import datetime

app = FastAPI(title="Alert Logger")

@app.post("/")
async def root(req: Request):
  payload = await req.json()
  ts = datetime.datetime.utcnow().isoformat()
  print(f"[{ts}] ALERTMANAGER WEBHOOK:\n{json.dumps(payload, indent=2)}\n")
  return {"ok": True}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8081)
