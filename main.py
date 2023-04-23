from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient


app = FastAPI()
templates = Jinja2Templates(directory="frontend")

# DB 연결
uri = "mongodb+srv://cho000130:cho41455@path.vcffeiq.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["path"]

msg = { 'name' : 'drone1',
        'routes' : '4',
        'cases' : [2,3,3,3],
        'Dst coordinate' : [35.153299,128.102089],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                                #path 0 : [node 0-1, node 0-2]
                                [ 
                                    [ 
                                        [35.155633,128.097057],[35.157422,128.100383]],
                                    [ 
                                        [35.157422,128.100383], [35.153299,128.102089]]],
                                #path 1 : [node 0-3, node 3-2]
                                [ 
                                    [ 
                                        [35.155633,128.097057],[35.151494,128.098007]],
                                    [
                                        [35.151494,128.098007],[35.153299,128.102089]]]
                            ],

                            [
                                [
                                    [
                                        [35.155633,128.097057],[35.157422,128.100383]],
                                    [
                                        [35.157422,128.100383], [35.153299,128.102089]]],
                                [
                                    [
                                        [35.155633,128.097057],[35.151494,128.098007]],
                                    [
                                        [35.151494,128.098007],[35.153299,128.102089]]]
                                    
                            ]
                        ]
}

def insert_nodes(msg):
    db['paths'].insert_one(msg)
    return True

def get_nodes(name):
    dst_node = db['paths'].find_one({'name' : name})['Dst coordinate']
    return dst_node


@app.get("/")
async def demopage(request : Request):
    dst_node = get_nodes(name = 'drone1')
    print(dst_node)
    context = {'request' : request}
    return templates.TemplateResponse("/demo.html",context)
