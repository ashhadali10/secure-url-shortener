from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator
import random
import string

app = FastAPI(title="Secure URL Shortener")

class URLRequest(BaseModel):
    url: str

    @validator('url')
    def validate_url_scheme(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError('Only http:// or https:// schemes are allowed')
        if "localhost" in v or "127.0.0.1" in v:
            raise ValueError('Internal URLs are not allowed')
        return v

url_store = {}

# --- STEP 1: Pehle Specific Routes Rakhein ---
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/shorten", status_code=status.HTTP_201_CREATED)
async def shorten_url(request: URLRequest):
    try:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        url_store[short_code] = request.url
        return {"short_code": short_code, "original_url": request.url}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

# --- STEP 2: Sabse Aakhir mein Dynamic/Variable Routes ---
@app.get("/{short_code}")
async def redirect_url(short_code: str):
    original_url = url_store.get(short_code)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"redirect_to": original_url}
