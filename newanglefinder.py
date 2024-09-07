import math
def calculate_angle(A, B, C):
    """
    Calculate the angle ABC (angle at point B) given three points A, B, and C.
    Args:
    - A, B, C: Tuples representing the coordinates of the three points (x, y).
    
    Returns:
    - Angle in degrees between the three points.
    """
    # Vectors BA and BC
    BA = (A[0] - B[0], A[1] - B[1])
    BC = (C[0] - B[0], C[1] - B[1])

    # Dot product of BA and BC
    dot_product = BA[0] * BC[0] + BA[1] * BC[1]

    # Magnitudes of BA and BC
    mag_BA = math.sqrt(BA[0] ** 2 + BA[1] ** 2)
    mag_BC = math.sqrt(BC[0] ** 2 + BC[1] ** 2)

    # Calculate the cosine of the angle
    cos_angle = dot_product / (mag_BA * mag_BC)

    # Calculate the angle in radians and then convert to degrees
    angle = math.acos(cos_angle)
    angle_degrees = math.degrees(angle)

    return abs(angle_degrees)
def reward_function(params):
    # Example of rewarding the agent to follow center line
    global previous_speed
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.3 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 80
    elif distance_from_center <= marker_2:
        reward = 40
    elif distance_from_center <= marker_3:
        reward = 20
    elif distance_from_center <= marker_4:
        reward = 10
    elif distance_from_center <= marker_5:
        reward = 5
    else:
        reward = 1e-3 # likely crashed/ close to off track
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    if(closest_waypoints[1]==len(waypoints)-1):
        curve_point = waypoints[0] 
    else:
        curve_point = waypoints[closest_waypoints[1]+1]
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    angleu = calculate_angle(prev_point,next_point,curve_point)
    optimalSpeed = (4-((angleu)/180))*3
    reward = reward*2*e**(-0.9*abs(optimalSpeed-params['speed']))
    heading = params['heading']
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    return float(reward)
