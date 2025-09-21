from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3, time, os

DB = os.getenv("DB_PATH", "db.sqlite3")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(title="LiveBar Backend", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def q(q, args=(), one=False):
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
    cur = con.execute(q, args); rows = cur.fetchall()
    con.commit(); con.close()
    return (rows[0] if rows else None) if one else rows

class Reading(BaseModel):
    source: str
    value: float  # 0..1
    at: float | None = None

@app.get("/api/venues")
def venues(lat: float | None = None, lon: float | None = None, radius: int = 5000, sort: str = "busy"):
    rows = q("SELECT * FROM venues")
    data = []
    for r in rows:
        d = dict(r)
        occ = q("SELECT value FROM readings WHERE venue_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],), one=True)
        d["occupancy"] = occ["value"] if occ else r["seed_occupancy"]
        d["status"] = "green" if d["occupancy"] < 0.3 else ("yellow" if d["occupancy"] < 0.7 else "red")
        data.append(d)
    if sort == "busy":
        data.sort(key=lambda x: x["occupancy"], reverse=True)
    elif sort == "rating":
        data.sort(key=lambda x: x["rating"], reverse=True)
    return data

@app.post("/api/venue/{vid}/reading", status_code=204)
def add_reading(vid: str, r: Reading):
    if not (0.0 <= r.value <= 1.0):
        raise HTTPException(400, "value must be 0..1")
    at = r.at or time.time()
    exist = q("SELECT id FROM venues WHERE id=?", (vid,), one=True)
    if not exist:
        raise HTTPException(404, "venue not found")
    q("INSERT INTO readings (venue_id, source, value, created_at) VALUES (?,?,?,?)", (vid, r.source, r.value, at))
    return None

@app.get("/api/health")
def health(): return {"ok": True}