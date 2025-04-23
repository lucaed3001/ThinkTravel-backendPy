from fastapi import FastAPI
from app.routers.auth import auth_router
from app.routers.locations import locations_router
from app.database import Base, engine, SessionLocal, get_db
from fastapi.staticfiles import StaticFiles

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

# Include tutte le route di autenticazione
app.include_router(auth_router, prefix="/auth")
app.include_router(locations_router, prefix="/locations")

app.mount("/images/cities", StaticFiles(directory="app/static/images/cities"), name="cities")

@app.get("/")
def root():
    return {"message": "Welcome to ThinkTravel API"}
