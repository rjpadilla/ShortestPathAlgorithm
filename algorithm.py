import operator
import csv
import threading
import concurrent.futures
from hashtable import Package, HashTable
from routing import Location, Map
from datetime import datetime, time
from threading import Thread

# Fields
time_of_day = time(8, 0)
end_of_day = time(17, 0)
delivered_together = set()
package_ready = []


def update_time() -> time:
    """Updates the time by one minute each time it's called.
    Runtime complexity of O(1)."""

    global time_of_day
    update = 1
    if time_of_day == end_of_day:
        return False
    else:
        if (time_of_day.minute + update) >= 60:
            time_of_day = time(
                    time_of_day.hour + 1,
                    (time_of_day.minute + update) % 60)
        else:
            time_of_day = time(time_of_day.hour, time_of_day.minute + update)


def distance_covered(location) -> int:
    """Calculate the distance covered using the truck's speed.
    Runtime complexity of O(1)."""

    per_hour = 60
    truck_speed = 18
    mile_per_minute = truck_speed / per_hour
    distance = int(location.distance / mile_per_minute)
    return distance


def delivery_time(location) -> time:
    """Updates the time the delivery of a package.
    Runtime complexity of O(1)."""

    per_hour = 60
    truck_speed = 18
    mile_per_minute = truck_speed / per_hour
    time_to_deliver = int(location.distance / mile_per_minute)

    if (time_of_day.minute + time_to_deliver) >= per_hour:
        time_of_delivery = time(time_of_day.hour + 1,
                                (time_of_day.minute + time_to_deliver) % 60)
    else:
        time_of_delivery = time(time_of_day.hour,
                                time_of_day.minute + time_to_deliver)

    return time_of_delivery


def return_to_hub(hashtable, hub_hashtable) -> None:
    """Returns the truck back home to package base.
    Runtime complexity of O(n)."""

    hub_map = create_map()
    current_location = hashtable.location
    hub_location = hub_hashtable.location

    for location in hub_map.location_adjacency_list.keys():
        if hub_location == location.address:
            hub_location = location
        if current_location == location.address:
            current_location = location

    routes_shortest_paths(hub_map, current_location)

    per_hour = 60
    truck_speed = 18
    mile_per_minute = truck_speed / per_hour
    time_to_return = int(hub_location.distance / mile_per_minute)

    if (time_of_day.minute + time_to_return) >= per_hour:
        time_of_return = time(time_of_day.hour + 1,
                              (time_of_day.minute + time_to_return) % 60)
    else:
        time_of_return = time(time_of_day.hour,
                              time_of_day.minute + time_to_return)

    in_route = True
    while in_route:
        if time_of_day == end_of_day:
            return False
        if time_of_day >= time_of_return:
            in_route = False
        else:
            with hashtable._lock:
                update_time()
    hashtable.location = hub_location.address
    hashtable.distance += hub_location.distance


def load_packages() -> None:
    """Open file, read package items one line at a time,
       create Package objects and append them to a list.
       Return the list once the entire file is processed.
       Runtime complexity of O(n^2)."""
    global package_ready
    with open('Package File.csv') as data:
        for line in csv.reader(data):
            package_list = [item for item in line]
            package = Package(int(package_list[0]),
                              package_list[1],
                              package_list[2],
                              int(package_list[4]),
                              package_list[5],
                              int(package_list[6]),
                              package_list[7])
            package.status = 'Ready For Shipment'
            package_list = []

            if package.notes[0:22] == "Must be delivered with":
                together_id = package.notes[23:].split(",")
                for item in together_id:
                    delivered_together.add(int(item))
                delivered_together.add(package.id)

            if (package.notes ==
                    "Delayed on flight" +
                    "---will not arrive to depot until 9:05 am"):
                package.status = 'Delayed On Flight'
                package_ready.append(package)
            else:
                package_ready.append(package)


def create_map() -> Map:
    """Creates a new map(hashtable) with it's location objects.
    Runtime complexity of O(n^2)."""

    map = Map()
    distance_list = []
    location_list = []

    with open('Distance Table.csv') as data:
        for line in csv.reader(data):
            address = line.pop(0)
            distance = [float(item) for item in line if item != '']
            distance_list.append(distance)
            location = Location(address)
            map.add_location(location)
            location_list.append(location)

    for i, line in enumerate(location_list):
        for j in range(len(distance_list[i]) - 1):
            map.add_undirected_route(location_list[i],
                                     location_list[j],
                                     distance_list[i].pop(0))
    return map


def routes_shortest_paths(map_graph, starting_location) -> None:
    """
    This code uses Dijkstra Shortest Path Alogorithm
    which assigns distance(weight) to a map's(graph)
    routes(edges) and assigns the locations(vertex)
    with a predecessor location(vertex) with the
    smallest route distance(weighted edge).
    Runtime complexity
    of O(n^2).
    """

    # List comprehenstion to store unvisited locations.
    unvisited_locations = [current_location
                           for current_location
                           in map_graph.location_adjacency_list]

    # Starting location is assigned a distance of 0
    starting_location.distance = 0

    # Location's distance and predecessor location
    # attributes are updated for shortes path.
    # Each while loop iteration removes a
    # location from the unvisited_location queue.
    while len(unvisited_locations) > 0:

        # Iterate through the unvisited_locations for the
        # smallest distance between locations. The location
        # with the smallest distance will be popped from
        # the unvisted location and be referenced for the
        # location_adjacency_list to find the shortest path.
        smallest_index = 0
        for i in range(1, len(unvisited_locations)):
            if (unvisited_locations[i].distance <
                    unvisited_locations[smallest_index].distance):
                smallest_index = i
        current_location = unvisited_locations.pop(smallest_index)

        # Iterate through the current_location's adjancency list
        # and uses the current_location and adjacent(the
        # iterable value from the iteration) as the dictionary
        # key for map_graph.route_distance which is used to find
        # an alternative route distance if possible.
        for adjacent in map_graph.location_adjacency_list[current_location]:
            route_distance = map_graph.route_distance[(current_location,
                                                       adjacent)]
            alternative_route_distance = (current_location.distance +
                                          route_distance)

            # If alernative_route_distance is less than the
            # adjacent.distance then the adjacent_vertix
            # distance and predecessor location atributes are
            # updated with alternative_route_distance and
            # current_location respectivily.
            if alternative_route_distance < adjacent.distance:
                adjacent.distance = alternative_route_distance
                adjacent.pre_location = current_location


def next_delivery(hashtable) -> 'location':
    """Greedy algorithm that will select the package for the next delivery.
    Runtime complexity of O(n^2)."""

    closest_delivery_location = None
    closest_delivery_distance = float('inf')
    trucks_map = create_map()
    current_location = hashtable.location

    # Assign's location objects of associated packages
    # to variables to find closest location.
    package_location_list = []
    for package in hashtable.table:
        for location in trucks_map.location_adjacency_list.keys():
            if package.address == location.address:
                package_location_list.append(location)
            if current_location == location.address:
                current_location = location

    # Removes duplicate locations
    package_location_list = list(set(package_location_list))

    routes_shortest_paths(trucks_map, current_location)

    closest_deadline = sorted(hashtable.table,
                              key=operator.attrgetter("deadline")).pop(0)

    # Finds closest location
    for package_location in package_location_list:
        if package_location.distance < closest_delivery_distance:
            closest_delivery_location = package_location
            closest_delivery_distance = package_location.distance

    return closest_delivery_location


def update_package(hashtable) -> None:
    """Updates the package's address. Runtime complexity of O(n)."""

    for package in hashtable.table:
        if (time_of_day >= time(10, 20) and
                package.notes == 'Wrong address listed'):
            package.address = '410 S State St'
            package.zipcode = 84111
            package.notes = 'Wrong address has been corrected'


def deliver_package(location, hashtable) -> None:
    """Delivers the package and updates the package and the hashtables statutes.
    Runtime complexity of O(n)."""

    # Changes the status of the package to delivered.
    for package in hashtable.table:
        if (package.address == location.address and
                package.notes != 'Wrong address listed'):
            print("Package %s delivered at %s with a deadline of %s" %
                  (package.id,
                   datetime.strptime(time_of_day.strftime('%H:%M'),
                                     '%H:%M').strftime('%I:%M%p'),
                   datetime.strptime(package.deadline.strftime('%H:%M'),
                                     '%H:%M').strftime('%I:%M%p')))
            package.status = 'Delivered'
            hashtable.remove()

    hashtable.location = location.address
    hashtable.distance += location.distance


def load_together(hashtable, hub_hashtable) -> None:
    """Loads packages that are delivered together.
    Runtime complexity of O(n)."""

    sorted_packages = sorted(hub_hashtable.table,
                             key=operator.attrgetter("deadline"))

    for package in sorted_packages:
        if package.id in delivered_together:
            if package.status == 'Ready For Shipment':
                if hashtable.insert(package):
                    package.status = 'Out For Delivery'


def load_truck2_only(hashtable, hub_hashtable) -> None:
    """Load the packages from the hub to the truck.
    Runtime complexity of O(n)."""

    sorted_packages = sorted(hub_hashtable.table,
                             key=operator.attrgetter("deadline"))

    for package in sorted_packages:
        if package.status == 'Ready For Shipment':
            if hashtable.id == 2 and package.notes == "Can only be on truck 2":
                if hashtable.insert(package):
                    package.status = 'Out For Delivery'
            else:
                break


def load_trucks(hashtable, hub_hashtable) -> None:
    """Load the packages from the hub to the truck.
    Runtime complexity of O(n)."""

    sorted_packages = sorted(hub_hashtable.table,
                             key=operator.attrgetter("deadline"))

    for package in sorted_packages:
        with hashtable._lock:
            if package.status == 'Ready For Shipment':
                if hashtable.insert(package):
                    package.status = 'Out For Delivery'


def expedite_package(hashtable, hub_hashtable) -> None:
    """Load truck with a deadline first. Runtime complexity of O(n)."""

    sorted_packages = sorted(hub_hashtable.table,
                             key=operator.attrgetter("deadline"))
    expedited_only = [package
                      for package in sorted_packages
                      if package.deadline <= time(10, 30)]

    for package in expedited_only:
        with hashtable._lock:
            if package.status == 'Ready For Shipment':
                if hashtable.insert(package):
                    package.status = 'Out For Delivery'


def route_trucks(truck_hashtable) -> bool:
    """Routes the trucks for delivery if it contains packages.
    Runtime complexity of O(n)."""
    for package in truck_hashtable.table:
        if package is truck_hashtable.EMPTY_SINCE_START:
            pass
        else:
            return True

    return False


def packages_delivered(hub_hashtable) -> bool:
    """End the program once all packages are delivered.
    Runtime complexity of O(n)."""
    global time_of_day
    global end_of_day
    for package in hub_hashtable.table:
        if package.status != 'Delivered':
            return True
        else:
            pass
    end_of_day = time_of_day
    return False


def arrived_packages(hub_hashtable) -> None:
    """Sets the delayed package for ready for shipment.
    Runtime complexity of O(n)."""

    time_of_arrival = time(9, 5)

    if time_of_day == time_of_arrival:
        for package in hub_hashtable.table:
            if package.status == 'Delayed On Flight':
                package.status = 'Ready For Shipment'


def run_algorithm(truck_hashtable, hub_hashtable) -> None:
    """Runs the core algorithm for the routing program.
    Runtime complexity of O(1)."""
    while(packages_delivered(hub_hashtable)):
        if time_of_day >= end_of_day:
            return False
        return_to_hub(truck_hashtable, hub_hashtable)
        if time_of_day <= time(10, 30):
            load_together(truck_hashtable, hub_hashtable)
            expedite_package(truck_hashtable, hub_hashtable)
            while(route_trucks(truck_hashtable)):
                next_location = next_delivery(truck_hashtable)
                time_to_deliver = delivery_time(next_location)
                in_delivery = True
                while in_delivery:
                    arrived_packages(hub_hashtable)
                    if time_of_day >= end_of_day:
                        return False
                    if time_of_day >= time_to_deliver:
                        deliver_package(next_location, truck_hashtable)
                        in_delivery = False
                    else:
                        with truck_hashtable._lock:
                            update_time()
                            update_package(hub_hashtable)
        else:
            load_truck2_only(truck_hashtable, hub_hashtable)
            load_trucks(truck_hashtable, hub_hashtable)
            while(route_trucks(truck_hashtable)):
                next_location = next_delivery(truck_hashtable)
                time_to_deliver = delivery_time(next_location)
                in_delivery = True
                while in_delivery:
                    arrived_packages(hub_hashtable)
                    if time_of_day >= end_of_day:
                        return False
                    if time_of_day >= time_to_deliver:
                        deliver_package(next_location, truck_hashtable)
                        in_delivery = False
                    else:
                        with truck_hashtable._lock:
                            update_time()
                            update_package(hub_hashtable)


def look_up(hour=17, minute=0, attribute=None, element=None) -> str:
    """Look-up function that runs the program and returns the results.
    Runtime complexity of O(n)."""

    global end_of_day

    end_of_day = time(hour, minute)
    # Location of the package storage facility.
    hub_storage = HashTable(40)

    # A truck that can deliver, tow and talk. What more can you ask??
    mater_tow_truck = HashTable(16)
    mater_tow_truck.id = 1

    # 2scary4me
    maximum_overdrive_truck = HashTable(16)
    maximum_overdrive_truck.id = 2

    # I tried moving this truck but it won't budge. I wonder what's below...
    mew_truck = HashTable(151)
    mew_truck.id = 151

    load_packages()
    for package in package_ready:
        hub_storage.insert(package)

    # Initialize the trucks to be used concurrently.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_algorithm, mater_tow_truck, hub_storage)
        executor.submit(run_algorithm, maximum_overdrive_truck, hub_storage)

    hub_storage.distance = (mater_tow_truck.distance +
                            maximum_overdrive_truck.distance)

    print(hub_storage.search(attribute, element))
    print("First truck stopped with %s miles at %s." %
          (mater_tow_truck.distance, mater_tow_truck.location))
    print("Second truck stopped with %s miles at %s." %
          (maximum_overdrive_truck.distance, maximum_overdrive_truck.location))
    print("The time is %s." %
          datetime.strptime(
              time_of_day.strftime('%H:%M'), '%H:%M').strftime('%I:%M%p'))
    print("The total milage is %s" % (hub_storage.distance))
