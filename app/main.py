from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers.auth import auth_router
from app.routers.locations import locations_router
from app.database import Base, engine, SessionLocal, get_db
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.workers import translation_worker, start_translation_worker
import threading
import os

#threading.Thread(target=translation_worker, daemon=True).start()

app = FastAPI(
    title="ThinkTravel API",
    description="ThinkTravel API for managing",
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Supporto API",
        "url": "http://example.com/contact/",
        "email": "root.thinktravel@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/docs",  # Cambia l'URL di Swagger
    redoc_url="/redoc",  # Cambia l'URL di ReDoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/edmondo")
def get_cv():
    file_path = os.path.join("app", "static", "curriculum", "edmondo.pdf")
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=edmondo.pdf"}
    )

@app.get("/giraudo")
def get_cv():
    file_path = os.path.join("app", "static", "curriculum", "giraudo.pdf")
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=giraudo.pdf"}
    )

@app.get("/ghi")
def get_cv():
    file_path = os.path.join("app", "static", "curriculum", "ghi.pdf")
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=ghi.pdf"}
    )

# Include tutte le route di autenticazione
app.include_router(auth_router, prefix="/auth")
app.include_router(locations_router, prefix="/locations")

app.mount("/images/cities", StaticFiles(directory="app/static/images/cities"), name="cities")
app.mount("/images/countries", StaticFiles(directory="app/static/images/countries"), name="countries")
app.mount("/images/hotels", StaticFiles(directory="app/static/images/hotels"), name="hotels")
app.mount("/curriculum", StaticFiles(directory="app/static/curriculum"), name="curriculum")

@app.get("/")
def root():
    return {"message": "Welcome to ThinkTravel API"}

@app.on_event("startup")
def startup_event():
    start_translation_worker()

