from fastapi import FastAPI

m_app = FastAPI()
 

@m_app.get("/")
def standart():
    return{
        "hello":"епт"
    }