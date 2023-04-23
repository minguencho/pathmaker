from pymongo.mongo_client import MongoClient


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

def drone_select(distance):
    drones = []
    for drone in db['drones'].find({}, {'name': 1, 'range': 1}):
        if drone['range'] > distance:
            drones.append(drone['name'])
    return drones[0]
