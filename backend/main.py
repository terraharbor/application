from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import FileResponse
import os, time, json

DATA_DIR = os.getenv("STATE_DATA_DIR", "./data")
app = FastAPI(title="Terraform HTTP Backend Prototype")

def _project_dir(name: str) -> str:
    path = os.path.join(DATA_DIR, name)
    os.makedirs(path, exist_ok=True)
    return path

def _latest_state(name: str) -> str:
    return os.path.join(_project_dir(name), "latest.tfstate")

# GET  /state/{project}
@app.get("/state/{name}")
async def get_state(name: str):
    path = _latest_state(name)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="State not found")
    return FileResponse(path, media_type="application/octet-stream")

# POST /state/{project}
@app.post("/state/{name}")
async def put_state(name: str, request: Request):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="Empty body")

    proj_dir = _project_dir(name)
    ts = int(time.time())
    version_path = os.path.join(proj_dir, f"{ts}.tfstate")

    # We register the new state version and update the latest state
    for path in (version_path, _latest_state(name)):
        with open(path, "wb") as f:
            f.write(body)

    return Response(status_code=status.HTTP_200_OK)


# LOCK  /state/{project}
@app.api_route("/state/{name}", methods=["LOCK"])
async def lock_state(name: str, request: Request):
    lock_path = os.path.join(_project_dir(name), ".lock")
    body = (await request.body()).decode() or "{}"

    if os.path.exists(lock_path):
        with open(lock_path, "r") as f:
            return Response(f.read(), status_code=status.HTTP_423_LOCKED,
                            media_type="application/json")

    with open(lock_path, "w") as f:
        f.write(body)
    return Response(status_code=status.HTTP_200_OK)

# UNLOCK /state/{project}
@app.api_route("/state/{name}", methods=["UNLOCK"])
async def unlock_state(name: str, request: Request):
    lock_path = os.path.join(_project_dir(name), ".lock")
    if not os.path.exists(lock_path):
        # idempotent : ok even if the lock does not exist
        return Response(status_code=status.HTTP_200_OK)

    req_info = json.loads((await request.body()).decode() or "{}")
    with open(lock_path, "r") as f:
        cur_info = json.loads(f.read() or "{}")

    # if the request ID is provided and does not match the current lock ID, return error 409 Conflict
    if req_info.get("ID") and req_info["ID"] != cur_info.get("ID"):
        return Response(json.dumps(cur_info), status_code=status.HTTP_409_CONFLICT,
                        media_type="application/json")

    os.remove(lock_path)
    return Response(status_code=status.HTTP_200_OK)
