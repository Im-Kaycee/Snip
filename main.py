from fastapi import FastAPI
from routes.urls import router as urls_router
import yaml
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(urls_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"App is running": True}

@app.get("/openapi.yaml", response_class=PlainTextResponse)
def get_openapi_yaml():
    openapi_json = app.openapi()
    return yaml.dump(openapi_json, sort_keys=False)