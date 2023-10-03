from fastapi import FastAPI
from eyes_to_read_be.routes.user_routes import user_router
import uvicorn

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
