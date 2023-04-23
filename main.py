from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from . import database, path_utils
from Mission_Generator import Mission_Generator

app = FastAPI()
templates = Jinja2Templates(directory="frontend")



BC = {'lat' : 35.154233248776904,'lng':128.09317879693032}
Dstcoordinate = [35.153299,128.102089]
global name
@app.get("/")
async def demopage(request : Request):
    service_able_waypoint = database.get_service_waypoint()
    context = {'request' : request, 'lat' : BC['lat'], 'lng' : BC['lng'], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/demo.html",context)


@app.post("/")
async def post(request: Request):
    global name

    Dst = await request.json()
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    distance = path_utils.bs_dst_distance(BC,Dst)
    print("BC-Dst distance is",distance,"km")
    print("assigned drone is ", database.drone_select(distance))
    name = database.drone_select(distance)
    print(Dst)
    routes = database.get_traj(Dstcoordinate)
    return {"success": True, "routes" : routes}


@app.post("/generate_MF")
async def generate_MF():
    global name
    Dstcoordinate = [35.153299,128.102089]
    mission_generator = Mission_Generator()
    """
    mission_splitter = Misssion_Splitter()
    task_publisher = Task_Publisher()
    """
    routes = database.get_traj(Dstcoordinate)
    drone_name = name
    altitude = database.get_altitude(Dstcoordinate)
    Dstcoordinate = database.get_altitude(Dstcoordinate)
    receiver_info = database.get_receiver_info('mgcho')
    pre_inference_model = b'onnx' 
    mission_file = {}
    mission_file = mission_generator.make_mission(
        routes=routes,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dstcoordinate,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model)  
    print(mission_file)
    
    """
    task_piecees = mission_splitter.mission_split(mission_file)
    task_publisher.publish_list(task_piecees)
    """
    """
    task_pieces = mission_splitter.mission_split(mission_file)
    task_publisher.publish_list(
        messages=task_pieces,
        exchange_name='cap',
        routing_key_name='tocap'
    )"""
    return True