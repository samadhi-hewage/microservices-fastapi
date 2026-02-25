from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from jose import jwt
import logging
import time

app = FastAPI(title="API Gateway")

# ------------------ Logger Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ------------------ Service URLs ------------------
STUDENT_SERVICE_URL = "http://127.0.0.1:8001"

# ------------------ JWT Configuration ------------------
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ------------------ Middleware for Logging ------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"Incoming request: {request.method} {request.url}")
    
    # Forward the request to route handler
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    logger.info(f"Response status: {response.status_code} - processed in {process_time:.3f}s")
    
    return response

# ------------------ Root ------------------
@app.get("/")
def root():
    return {"message": "API Gateway running"}

# ------------------ Request Forwarder (Enhanced for Error Handling) ------------------
async def forward_request(method: str, url: str, request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=request.headers.raw,
                content=await request.body(),
                timeout=10.0  # optional timeout
            )

        # Check if microservice returned a non-JSON response
        try:
            content = response.json() if response.content else None
        except Exception:
            content = response.text

        # Raise HTTPException if microservice returned an error
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Student service error: {content}"
            )

        return JSONResponse(
            status_code=response.status_code,
            content=content
        )

    except httpx.RequestError as e:
        # Network or connection errors
        raise HTTPException(
            status_code=503,
            detail=f"Error connecting to student service: {str(e)}"
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

# ------------------ Student Routes (Protected) ------------------
@app.get("/gateway/students", dependencies=[Depends(verify_token)])
async def get_students(request: Request):
    return await forward_request("GET", f"{STUDENT_SERVICE_URL}/api/students", request)

@app.get("/gateway/students/{student_id}", dependencies=[Depends(verify_token)])
async def get_student(student_id: int, request: Request):
    return await forward_request("GET", f"{STUDENT_SERVICE_URL}/api/students/{student_id}", request)

@app.post("/gateway/students", dependencies=[Depends(verify_token)])
async def create_student(request: Request):
    return await forward_request("POST", f"{STUDENT_SERVICE_URL}/api/students", request)

@app.put("/gateway/students/{student_id}", dependencies=[Depends(verify_token)])
async def update_student(student_id: int, request: Request):
    return await forward_request("PUT", f"{STUDENT_SERVICE_URL}/api/students/{student_id}", request)

@app.delete("/gateway/students/{student_id}", dependencies=[Depends(verify_token)])
async def delete_student(student_id: int, request: Request):
    return await forward_request("DELETE", f"{STUDENT_SERVICE_URL}/api/students/{student_id}", request)