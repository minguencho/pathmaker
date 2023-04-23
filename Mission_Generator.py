class Mission_Generator():
    def __init__(self):

        return
    
    def make_mission(routes, drone_name, altitude, Dstcoordinate, receiver_info, pre_inference_model):
        mission_file = {'name' :drone_name,
                        'waypoint': routes,
                        'altitude' : altitude,
                        'ep_coordinate' : Dstcoordinate,
                        'pre_inference_model' : pre_inference_model,
                        'reciever_info' : receiver_info 
        }
        return mission_file