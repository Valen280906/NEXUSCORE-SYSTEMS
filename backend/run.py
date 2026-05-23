import uvicorn

if __name__ == "__main__":
    # Inicia el servidor de desarrollo en http://127.0.0.1:8000
    # reload=True habilita la recarga automática ante cambios de código
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
