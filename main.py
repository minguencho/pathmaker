from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pymongo.mongo_client import MongoClient
from math import sin, cos, sqrt, atan2, radians
from Mission_Generator import Mission_Generator

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
msg = { 'name' : 'GNU 001',
        'routes' : '2',
        'cases' : [2],
        'Dst coordinate' : [35.153299,128.102089],
        'trajectories' :
                        #trajectories : [route 0, route 1] 
                        [ 
                            #route 0 : [path 0, path 1]
                            [
                            #path 0 : [node 0 , node 1, node2]    
                                    [ 
                                        [35.154233248776904,128.09317879693032],[35.15149231349859,128.09797477268654]],
                                    [ 
                                        [35.15149231349859,128.09797477268654],[35.153299,128.102089]]
                            ],
                            #route 1 : [path 0, path 1]
                            [ 
                                [
                                    [35.155633,128.097057],[35.157422,128.100383]],
                                [
                                    [35.157422,128.100383],[35.155798,128.100232]],
                                [
                                    [35.155798,128.100232], [35.155853,128.104043]]   
                            ]
                        ],
        'altitude' : 10
}


test_drone1 = {  'name' : 'low_drone',
                'payload' : 3,
                'range' : 1.5
}
test_drone2 = {  'name' : 'middle_drone',
                'payload' : 7,
                'range' : 3
}
test_drone3 = {  'name' : 'high_drone',
                'payload' : 10,
                'range' : 5
}

test_user1 = {  'name' : 'mgcho',
                'reciever_info' : 'tensor'
}

def insert_nodes(msg):
    db['paths'].insert_one(msg)
    return True

def insert_drone(test_drone):
    db['drones'].insert_one(test_drone)
    return True

def insert_user(test_user):
    db['users'].insert_one(test_user)
    return True
def insert_missionfile(mission_file):
    db['MissionFile'].insert_one(mission_file)
    return True

def get_nodes(name):
    dst_node = db['paths'].find_one({'name' : name})['Dst coordinate']
    return dst_node

def get_altitude(path_name):
    altitude = db['paths'].find_one({'path': path_name})['altitude']
    return altitude

def get_Dstcoordinate(path_name):
    Dstcoordinate = db['paths'].find_one({'path': path_name})['Dst coordinate']
    return Dstcoordinate

def get_receiver_info(name):
    receiver_info = db['users'].find_one({'name' : name})['receiver_info']
    return receiver_info

def get_service_waypoint():
    waypoint = []
    for route in db['paths'].find_one({}, {'trajectories': 1})['trajectories']:
            last_path = route[-1][-1]
            waypoint.append((last_path))
    return waypoint

def get_traj(Dstcoordinate):
    routes=[]
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    # document가 None이면 trajectories가 없음
    if document is None:
        return []

    # trajectories 필드에서 routes 가져오기
    trajectories = document['trajectories']
    routes = trajectories[0]
    route = []
    for i in routes:
        if i not in route:
            route.append(i)
    """for route in trajectories:
        routes.append(route)"""

    return route

def get_altitude(Dstcoordinate):
    document = db['paths'].find_one({'Dst coordinate': Dstcoordinate})
    Dstcoordinate = document['Dst coordinate']
    return Dstcoordinate

def get_Dstcoordinate(path_name):
    document = db['paths'].find_one({'path': path_name})
    altitude = document['altitude']
    return altitude

def bs_dst_distance(BC,Dst):
    # 지구 반경 (km)
    R = 6373.0

    # 위도, 경도를 라디안으로 변환
    lat1 = radians(BC['lat'])
    lon1 = radians(BC['lng'])
    lat2 = radians(Dst['lat'])
    lon2 = radians(Dst['lng'])

    # 경도, 위도 차이 계산
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # haversine 공식 적용
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c

    return distance
def drone_select(distance):
    drones = []
    for drone in db['drones'].find({}, {'name': 1, 'range': 1}):
        if drone['range'] > distance:
            drones.append(drone['name'])
    return drones[0]

BC = {'lat' : 35.154233248776904,'lng':128.09317879693032}
Dstcoordinate = [35.153299,128.102089]
global name
@app.get("/")
async def demopage(request : Request):
    service_able_waypoint = get_service_waypoint()
    context = {'request' : request, 'lat' : BC['lat'], 'lng' : BC['lng'], 'service_able_waypoint' : service_able_waypoint}
    return templates.TemplateResponse("/demo.html",context)


@app.post("/")
async def post(request: Request):
    global name

    Dst = await request.json()
    print(f"Destination longitude={Dst['lng']}, latitude={Dst['lat']}")
    distance = bs_dst_distance(BC,Dst)
    print("BC-Dst distance is",distance,"km")
    print("assigned drone is ", drone_select(distance))
    name = drone_select(distance)
    print(Dst)
    routes = get_traj(Dstcoordinate)
    return {"success": True, "routes" : routes}


@app.post("/generate_MF")
async def generate_MF():
    global name
    Dstcoordinate = [35.153299,128.102089]
    """mission_generator = Mission_Generator()
    mission_splitter = Misssion_Splitter()
    task_publisher = Task_Publisher()"""
    routes = get_traj(Dstcoordinate)
    drone_name = name
    altitude = get_altitude(Dstcoordinate)
    Dstcoordinate = get_altitude(Dstcoordinate)
    receiver_info = get_receiver_info('mgcho')
    pre_inference_model = b'onnx' 
    mission_file = {}
    mission_file = Mission_Generator.make_mission(
        routes=routes,
        drone_name=drone_name,
        altitude=altitude,
        Dstcoordinate=Dstcoordinate,
        receiver_info=receiver_info,
        pre_inference_model=pre_inference_model)  
    print(mission_file)
    insert_missionfile(mission_file)
    """
    task_pieces = mission_splitter.mission_split(mission_file)
    task_publisher.publish_list(
        messages=task_pieces,
        exchange_name='cap',
        routing_key_name='tocap'
    )"""
    return True