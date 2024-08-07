from fastapi import FastAPI
import uvicorn
from app import router as all_router
app = FastAPI()

app.include_router(all_router)

@app.get("/")
def standart():
    return{
        "hello":"епт"
    }

if __name__ == "__main__":
    uvicorn.run(app = "main:app")