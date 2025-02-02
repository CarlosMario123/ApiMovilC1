from fastapi import FastAPI
from .config.database import engine, Base
from .tasks.router import router as tasks_router
from .auth.router import router as auth_router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Incluir routers
app.include_router(auth_router)
app.include_router(tasks_router)
