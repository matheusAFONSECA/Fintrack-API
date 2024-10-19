import uvicorn
from fastapi import FastAPI
from fintrack_api.api import API

app = FastAPI()

# Instancia a classe API e inclui as rotas
api = API()
app.include_router(api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
