from math import sin, cos, sqrt, atan2, radians


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