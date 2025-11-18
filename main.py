import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Disaster, Donation, Volunteer

app = FastAPI(title="Bayanihan Relief API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bayanihan Relief API Running"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        from database import db
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ---------- Disaster Endpoints ----------
@app.post("/api/disasters", response_model=dict)
async def create_disaster(disaster: Disaster):
    doc = await create_document("disaster", disaster.model_dump())
    return {"id": str(doc.get("_id")), "message": "Disaster created"}

@app.get("/api/disasters", response_model=List[dict])
async def list_disasters(limit: int = 20):
    docs = await get_documents("disaster", {}, limit)
    # convert ObjectId to string
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs

# ---------- Donation Endpoints ----------
@app.post("/api/donations", response_model=dict)
async def create_donation(donation: Donation):
    doc = await create_document("donation", donation.model_dump())
    return {"id": str(doc.get("_id")), "message": "Donation received. Thank you!"}

@app.get("/api/donations", response_model=List[dict])
async def list_donations(limit: int = 50):
    docs = await get_documents("donation", {}, limit)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs

# ---------- Volunteer Endpoints ----------
@app.post("/api/volunteers", response_model=dict)
async def create_volunteer(volunteer: Volunteer):
    doc = await create_document("volunteer", volunteer.model_dump())
    return {"id": str(doc.get("_id")), "message": "Volunteer registered. Salamat!"}

@app.get("/api/volunteers", response_model=List[dict])
async def list_volunteers(limit: int = 50):
    docs = await get_documents("volunteer", {}, limit)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
