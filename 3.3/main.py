from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    username: str
    password: str


@app.get('/headers')
async def headers(request: Request):
    user_agent = request.headers.get('a-agent')
    accept_language = request.headers.get('Accept-Language')
    if user_agent and accept_language:
        result = {
            'user_agent': user_agent,
            'accept_language': accept_language,
        }
        return result

    return HTTPException(status_code=400, detail="no header")
