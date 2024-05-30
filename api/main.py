from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.resources.redirect_resource import router as redirect_router
from app.resources.pool_resource import router as pool_router
from app.resources.log_resource import router as log_router
from app.middleware import LoggingMiddleware

app = FastAPI(
    title="Redirect Domain App",
    description="Redirect Domain API using Docker, FastAPI and MySQL",
    contact={
        "name": "Edwuin Gutierrez",
        "email": "edwinguti86@gmail.com",
    },
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

# Set CORS
origins = [
    "http://localhost",
    "http://localhost:8006",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:4000",
    "http://localhost:19006",
]

# Set Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

# Set Routers
app.include_router(pool_router)
app.include_router(redirect_router)
app.include_router(log_router)
