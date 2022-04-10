from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

class Item(BaseModel):
    title: str
    img_url:str 
    description: str
    reference: str 
    author: str 

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn_string=("")
client=MongoClient(conn_string,serverSelectionTimeoutMS=5000)
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db=client.get_database("myFirstDatabase")
blog=db.get_collection("Blog")
@app.post("/create/blog")
async def create_blog(item:Item):
    print(item,item.dict())
    res=blog.insert_one(item.dict())
    print(res)
    return {"msg":"success"}


@app.get("/get/blogs")
async def get_blog():
    items=blog.find()
    list_cur=list(items)
    js=dumps(list_cur)
    return dumps(js)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.delete("/delete/blog/{blogid}")
async def delete_blog(blogid):
    result=blog.delete_one({"_id":ObjectId(blogid)})
    print(result.raw_result)
    if(result.deleted_count>0):
        return {"msg":"hogya"}
    else:
        return {"msg":"L hogya"}
