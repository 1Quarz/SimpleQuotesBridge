import uvicorn
import datetime
from fastapi import FastAPI
from basemodels import Quote
from database import database, quotesDB

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/add_quote")
async def add_quote(BaseModel: Quote):
    query = quotesDB.insert().values(quote=BaseModel.quote, author=BaseModel.author, timestamp=datetime.datetime.now())
    last_record_id = await database.execute(query)
    return {"message": "Quote added"}


@app.get("/get_quotes")
async def get_quotes():
    query = quotesDB.select()
    result = await database.fetch_all(query)
    return result


if __name__ == "__main__":

    uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Server running on http://127.0.0.1:8000")

