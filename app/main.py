from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl, validator
from dotenv import load_dotenv
import os
import random
import string

# Load Environment Variables (Secrets Management)
load_dotenv()

app = FastAPI(title="Secure URL Shortener")

# --- Security Model: Input Validation ---
class URLRequest(BaseModel):
    url: str

    # Custom Validator to prevent malicious URLs
    @validator('url')
    def validate_url_scheme(cls, v):
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError('Only http:// or https:// schemes are allowed')
        # Basic check to prevent internal network access (SSRF protection)
        if "localhost" in v or "127.0.0.1" in v:
            raise ValueError('Internal URLs are not allowed')
        return v

# In-memory storage for simplicity (Step 3 mein DB use karenge)
url_store = {}

@app.post("/shorten", status_code=status.HTTP_201_CREATED)
async def shorten_url(request: URLRequest):
    try:
        # Generate random short code
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        url_store[short_code] = request.url
        return {"short_code": short_code, "original_url": request.url}
    
    except Exception as e:
        # Security: Do not expose stack trace to user
        # Log error internally instead (Step 4 mein seekhenge)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    original_url = url_store.get(short_code)
    
    if not original_url:
        # Security: Generic error message
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {"redirect_to": original_url}

@app.get("/health")
async def health_check():
    # Security: Don't expose version info or internal details in health check
    return {"status": "healthy"}
