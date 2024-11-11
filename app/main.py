from fastapi import FastAPI, Request, HTTPException

app = FastAPI()


@app.get('/headers')
async def get_headers(request: Request):
    headers = request.headers
    print(headers)
    if "User-Agent" not in headers:
        raise HTTPException(status_code=400, detail="Missing User-Agent")
    if "Accept-Language" not in headers:
        raise HTTPException(status_code=400, detail="Missing Accept-Language")

    return {
        "User-Agent": request.headers["user-agent"],
        "Accept-Language": request.headers["accept-language"]
    }
