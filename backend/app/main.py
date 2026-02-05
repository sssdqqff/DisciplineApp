from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import init_db
from .routers import tasks_router, categories_router, users_router, auth_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug_mode,
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.0.0",
    description="API for managing tasks and categories."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(tasks_router)
app.include_router(categories_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}