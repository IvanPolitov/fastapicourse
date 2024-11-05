from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get('/')
async def root():
    return FileResponse('index.html')


@app.post('/calculate')
async def calculate(num1: int, num2: int):
    result = num1 + num2
    return {'result': result}


@app.get('/calculate')
async def calculate(num1: int, num2: int):
    return {'result': 'use postman'}
