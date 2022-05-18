from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware

conn_string=(
   "mongodb://cl2k87s9f000e0ooheiyc57ee:YHNVfnKIfrOSLol3ZEASIeVB@dashboard.lawcoolify.ml:9001/?readPreference=primary&ssl=false"
)
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

class Item(BaseModel):
    title: str #title of the blog
    image_ref:str ##one keyword related to blog
    description: str ##description of the blog 
    reference: str ## reference enter none if nothing   
    author: str ## author name 

app = FastAPI() ### initializing the fast api app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client=MongoClient(conn_string,serverSelectionTimeoutMS=5000) ## connecting to mongodb
try:
    print(client.server_info())
except Exception:
    print("Unable to connect to the server.")

db=client.get_database("myFirstDatabase")
blog=db.get_collection("Blog")

##create blog route
@app.post("/create/blog")
async def create_blog(item:Item):
    print(item,item.dict())
    res=blog.insert_one(item.dict())
    print(res)
    return {"msg":"success"}

## get all blog route
@app.get("/get/blogs")
async def get_blog():
    items=blog.find()
    list_cur=list(items)
    js=dumps(list_cur)
    return dumps(js)

@app.get("/")
async def root():
    return {"message": "Blog backend created by instagram.com/happypanda.digital"}

## delete route for blog
@app.delete("/delete/blog/{blogid}")
async def delete_blog(blogid):
    result=blog.delete_one({"_id":ObjectId(blogid)})
    print(result.raw_result)
    if(result.deleted_count>0):
        return {"msg":"hogya"}
    else:
        return {"msg":"L hogya"}
