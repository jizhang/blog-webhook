from fastapi import FastAPI

from .routers import deploy

app = FastAPI()
app.include_router(deploy.router)
