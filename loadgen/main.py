import os, time, random, requests

TARGET = os.getenv("TARGET", "http://api:8080")
SLEEP = float(os.getenv("SLEEP", "0.2"))

paths = ["/api/hello", "/api/db"]

while True:
    path = random.choice(paths)
    try:
        requests.get(TARGET + path, timeout=1.5)
    except Exception:
        pass
    time.sleep(SLEEP)
