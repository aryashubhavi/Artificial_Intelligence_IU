#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by:
#  primary 
#   Jacob Striebel    (jstrieb)
#  secondary
#   Aishwarya Budhkar (abudhkar)
#   Shubhavi Arya     (aryas)
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#

import sys, copy, math

def get_route__comparison_index(start, end, placename__adjplaces, solution, comparison_index):
  
  fringe = list()
  s = None
  successors = None
  optimally_visited = set()
  
  if start==end:
    return True
  fringe.append([
    [(start, 'segment-info')], # 0 route-taken
    0,                         # 1 total-segments
    0.,                        # 2 total-miles
    0.,                        # 3 total-hours
    0.,                        # 4 total-delivery-hours
  ])
  #visited.add(start)
  while True:
    if 0==len(fringe):
      return False
    s = fringe.pop(0)
    #print(s)
    placename = s[0][-1][0]
    optimally_visited.add(placename)
    successors = None
    if placename not in placename__adjplaces:
      adjplaces = set()
    else:
      adjplaces = placename__adjplaces[placename]
    for adjplace in adjplaces:
     dst_name = adjplace[0]
     if dst_name not in optimally_visited: 
      s_copy    = copy.deepcopy(s)
      miles     = adjplace[1]
      mph       = adjplace[2]
      road_name = adjplace[3]
      time      = miles * (1./mph)
      delivery_t= time
      if mph >= 50:
        delivery_t+= math.tanh(miles/1000) * 2 * (time + s_copy[3])
      s_copy[0].append((dst_name, road_name+' for '+str(miles) + ' miles at '+str(mph)+' mph taking '+str(time)+' hours'))
      s_copy[1] += 1
      s_copy[2] += miles
      s_copy[3] += time
      s_copy[4] += delivery_t
      #sys.stderr.write('  '+str(route_taken)+'\n')
      if dst_name==end:
        solution['route-taken']         = s_copy[0][1:]
        solution['total-segments']      = s_copy[1]
        solution['total-miles']         = s_copy[2]
        solution['total-hours']         = s_copy[3]
        solution['total-delivery-hours']= s_copy[4]
        return True
      insertion_made = False
      i = -1
      l = len(fringe)
      while (i := i+1) < l:
        if False==insertion_made and s_copy[comparison_index] <= fringe[i][comparison_index]:
          fringe.insert(i, s_copy)
          i+=1
          l+=1
          insertion_made = True
        if dst_name==fringe[i][0][-1][0]:
          if False==insertion_made:
            insertion_made=None
            break
          elif True==insertion_made:
            fringe.pop(i)
            break
          else:
            assert False
      if False==insertion_made:
        fringe.append(s_copy)

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.
    
    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    
    name__adjacents = dict()
    for line in open('road-segments.txt', 'r').readlines():
      sline = line.split()
      assert 5==len(sline)
      if sline[0] not in name__adjacents:
        name__adjacents[sline[0]] = set()
      ############    src-name       dst-name  miles-src-to-dst mph-speed-lim    road-name
      ############                   0         1                2                3
      name__adjacents[sline[0]].add((sline[1], float(sline[2]), float(sline[3]), sline[4]))
      if sline[1] not in name__adjacents:
        name__adjacents[sline[1]] = set()
      name__adjacents[sline[1]].add((sline[0], int(sline[2]), int(sline[3]), sline[4]))
    
    name__coordinates = dict()
    for line in open('city-gps.txt', 'r').readlines():
      sline = line.split()
      assert 3==len(sline)
      if sline[0] not in name__adjacents:
        sys.stderr.write('warning: '+sline[0]+' has GPS coordinates but no road leading in or out\n')
      if sline[0] in name__coordinates:
        sys.stderr.write('warning: '+sline[0]+' appears more than once in the GPS coordinates file\n')
      name__coordinates[sline[0]] = (float(sline[1]), float(sline[2]))
    
    sys.stderr.write('info: start = '+start+'\n')
    sys.stderr.write('info: end   = '+end+'\n')
    sys.stderr.write('info: cost  = '+cost+'\n')
    
    route_taken = list()
    #[
    #  ("Martinsville,_Indiana","IN_37 for 19 miles"),
    #  ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #  ("Indianapolis,_Indiana","IN_37 for 7 miles")
    #]
    
    solution = dict()
    solution['route-taken']         = route_taken
    solution['total-segments']      = 0
    solution['total-miles']         = 0.
    solution['total-hours']         = 0.
    solution['total-delivery-hours']= 0.
    
    #{
    #  "total-segments"       : len(route_taken), 
    #  "total-miles"          : 51., 
    #  "total-hours"          : 1.07949, 
    #  "total-delivery-hours" : 1.1364, 
    #  "route-taken"          : route_taken
    #}
    
    if start==end:
      sys.stderr.write('warning: the start and end locations are the same; no search required\n')
    elif start not in name__adjacents:
      sys.stderr.write('warning: the start location of '+start+' has no road leading in or out; search will not execute\n')
    elif end not in name__adjacents:
      sys.stderr.write('warning: the end location of '+end+' has no road leading in or out; search will not execute\n')
    else:
      path_exists = None
      if 'segments'==cost:
        path_exists = get_route__comparison_index(start, end, name__adjacents, solution, comparison_index=1)
      elif 'distance'==cost:
        path_exists = get_route__comparison_index(start, end, name__adjacents, solution, comparison_index=2)
      elif 'time'==cost:
        path_exists = get_route__comparison_index(start, end, name__adjacents, solution, comparison_index=3)
      elif 'delivery'==cost:
        path_exists = get_route__comparison_index(start, end, name__adjacents, solution, comparison_index=4)
      else:
        sys.stderr.write('error: invalid cost function; no search will execute\n')
      
      if True==path_exists:
        sys.stderr.write('info: the shortest path was found\n')
      elif False==path_exists:
        sys.stderr.write('info: no path exits\n')
      elif None==path_exists:
        pass
      else:
        assert False
    
    return solution


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


