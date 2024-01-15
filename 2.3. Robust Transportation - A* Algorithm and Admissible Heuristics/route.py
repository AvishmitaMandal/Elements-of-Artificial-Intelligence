#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by:
# Niharika Ganji nganji
# Avishmita Mandal avmandal
# Aditya Padgal adpadgal
#
# Based on skeleton code by B551 Course Staff, Fall 2023
#

# !/usr/bin/env python3
import heapq
import math
import sys
def get_route(start, end, cost):

    '''Read Files'''

    segments = {}
    speed_limit = []

    for data in open('road-segments.txt', 'r').readlines():
        segment = data.split()

        city_1 = segment[0]
        city_2 = segment[1]

        if segments.get(city_1)==None:
            segments[city_1] = {}

        if segments.get(city_2)==None:
            segments[city_2] = {}

        segments[city_1][city_2] = (float(segment[2]), float(segment[3]), segment[4])
        segments[city_2][city_1] = (float(segment[2]), float(segment[3]), segment[4])

        speed_limit.append(float(segment[3]))

    max_speed = max(speed_limit)

    '''Let's read GPS Files'''

    gps_data = open('city-gps.txt','r')

    gps = {}

    for line in gps_data.readlines():
        data = line.split()
        gps[data[0]] = {float(data[1]), float(data[2])}


    '''Function returning cost based on given cost choice'''
    def return_cost(cost, fringe_details, end, gps, max_speed):
        if cost == 'segments':
            return fringe_details[2] + 1

        elif cost == 'distance':
            start = fringe_details[0][-1]
            if start not in gps.keys() or end not in gps.keys():
                return 0

            cordinates_start = gps.get(start)
            cordinates_end = gps.get(end)

            lat_start, long_start = cordinates_start
            lat_end, long_end = cordinates_end

            distance = math.sqrt(
                (float(lat_end) - float(lat_start)) ** 2 + (float(long_end) - float(long_start)) ** 2)
            return distance + fringe_details[3]

        elif cost == 'time':
            start = fringe_details[0][-1]
            if start not in gps.keys() or end not in gps.keys():
                return 0

            cordinates_start = gps.get(start)
            cordinates_end = gps.get(end)

            lat_start, long_start = cordinates_start
            lat_end, long_end = cordinates_end

            distance = math.sqrt((float(lat_end) - float(lat_start)) ** 2 + (float(long_end) - float(long_start)) ** 2)
            time = distance/max_speed
            return time + fringe_details[4]

        elif cost == 'delivery':
            start = fringe_details[0][-1]
            if start not in gps.keys() or end not in gps.keys():
                return 0

            cordinates_start = gps.get(start)
            cordinates_end = gps.get(end)

            lat_start, long_start = cordinates_start
            lat_end, long_end = cordinates_end

            distance = math.sqrt((float(lat_end) - float(lat_start)) ** 2 + (float(long_end) - float(long_start)) ** 2)
            time = distance/max_speed
            return time + fringe_details[5]

    '''Main Algorithm'''
    current_state = [start]
    route_taken = []
    visited = [start]
    city_cost = {}

    cost_segment = 0
    cost_distance = 0
    cost_time = 0
    cost_delivery = 0

    fringe = []
    fringe_start = (current_state, route_taken, cost_segment, cost_distance, cost_time, cost_delivery)

    result = return_cost(cost, fringe_start, end, gps, max_speed)
    heapq.heappush(fringe, (result, fringe_start))

    while fringe:
        result, current_fringe_details = heapq.heappop(fringe)

        if current_fringe_details[0][-1] == end:
            return {"total-segments": len(current_fringe_details[1]),
                    "total-miles": current_fringe_details[3],
                    "total-hours": current_fringe_details[4],
                    "total-delivery-hours": current_fringe_details[5],
                    "route-taken": current_fringe_details[1]}

        if current_fringe_details[0][-1] not in visited:
            visited.append(current_fringe_details[0][-1])

        neighbours = segments[current_fringe_details[0][-1]].keys()
        city_cost[current_fringe_details[0][-1]] = result

        for neighbour in neighbours:
            miles, speed, highway_info = segments[current_fringe_details[0][-1]][neighbour]

            time = miles/speed

            if speed<50:
                distance = time
            else:
                distance = time + (time + current_fringe_details[4]) * 2 * math.tanh(miles / 1000)

            updated_segment_cost = current_fringe_details[2] + 1
            updated_distance_cost = current_fringe_details[3] + miles
            updated_time_cost = current_fringe_details[4] + time
            updated_delivery_cost = current_fringe_details[5] + distance

            # Updating new fringe and its associated cost
            fringe_new = (current_fringe_details[0]+[neighbour], current_fringe_details[1] + [
                (str(neighbour), str(highway_info) + " for " + str(miles) + " miles")
            ], updated_segment_cost, updated_distance_cost, updated_time_cost, updated_delivery_cost)

            result = return_cost(cost, fringe_new, end, gps, max_speed)


            if neighbour not in visited:
                heapq.heappush(fringe, (result, fringe_new))
            else:
                if cost != 'segments' and result < city_cost[neighbour]:
                    heapq.heappush(fringe, (result, fringe_new))
                    visited.remove(neighbour)

    return False


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


