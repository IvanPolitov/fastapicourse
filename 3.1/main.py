from fastapi import FastAPI
from test_data import sample_products
app = FastAPI()


@app.get('/product/{product_id}')
async def get_product(product_id: int):
    result = {'message': 'None'}
    for p in sample_products:
        if p['product_id'] == product_id:
            result = p
            break
    return result


@app.get('/products/search')
async def search_product(keyword: str, category: str, limit: int = 10):
    result = []
    for p in sample_products:
        if keyword in p['name'] and category == p['category']:
            result.append(p)
    return result[:limit]
