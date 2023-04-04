from stop import Stop
from csv_reader import CSVReader
from datetime import datetime, timedelta


class StopGraph:
    def __init__(self):
        self.graph = {}
        self.counter = 0
        self.stop_info = {}

    def add_stop(self, stop):
        if stop.name not in self.graph:
            self.graph[stop.name] = []
            self.stop_info[stop.name] = [stop.lat, stop.lon]

    def add_connection(self, start_stop_name, end_stop_name, departure_time, arrival_time, line):
        if start_stop_name in self.graph:
            self.graph[start_stop_name].append([end_stop_name, departure_time, arrival_time, line])

    def get_adjacent_vertices(self, stop_name):
        if stop_name in self.graph:
            return self.graph[stop_name]
        else:
            return []

    def find_shortest_path(self, start_stop, end_stop, start_time):
        start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        #infinite distance for all stops in the beginning
        distances = {stop: float('inf') for stop in self.graph}
        distances[start_stop] = 0
        best_connections = {stop: [] for stop in self.graph}

        visited = set()

        queue = [(start_stop, start_time)]
        while queue:
            current_stop, current_time = queue.pop(0)
            #if current_stop == end_stop:
            #    break
            visited.add(current_stop)

            adjacent_stops = self.get_adjacent_vertices(current_stop)
            for adjacent_stop, departure_time, arrival_time, line in adjacent_stops:
                if adjacent_stop not in self.graph:
                    continue
                departure_time = datetime.strptime(departure_time, "%H:%M:%S").time()
                arrival_time = datetime.strptime(arrival_time, "%H:%M:%S").time()
                #TODO naprawic obliczenia czasu
                if departure_time >= current_time:
                    waiting_time = datetime.combine(datetime.today(), arrival_time) - datetime.combine(datetime.today(), current_time)
                else:
                    waiting_time = timedelta(hours=24) - (datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), arrival_time))
                #calculate cost (time)
                if arrival_time >= departure_time:
                    duration = datetime.combine(datetime.today(), arrival_time) - datetime.combine(datetime.today(), departure_time)
                else:
                    duration = timedelta(hours=24) - (datetime.combine(datetime.today(), departure_time) - datetime.combine(datetime.today(), arrival_time))

                total_time = (waiting_time + duration).total_seconds()
                #new cost to get to stop
                new_distance = distances[current_stop] + total_time
                #arrival_time = (datetime.combine(datetime.today(), departure_time) + duration).time()

                #update cost dictionary and add stop to queue
                if new_distance < distances[adjacent_stop]: #and arrival_time >= current_time
                    distances[adjacent_stop] = new_distance
                    best_connections[adjacent_stop] = [str(departure_time), str(arrival_time), line]
                    if adjacent_stop == 'ogród botaniczny' and distances[adjacent_stop] == 840.0:
                        print(current_stop)
                        print(waiting_time)
                        print(total_time)
                        print(arrival_time)
                    if adjacent_stop not in visited:
                        queue.append((adjacent_stop, arrival_time))

        print((datetime.combine(datetime.today(), start_time) + timedelta(seconds=distances[end_stop])).time())
        print(distances[end_stop])
        #generate path
        path = [end_stop, best_connections[end_stop], distances[end_stop]]
        current_stop = end_stop
        visited = set()
        #TODO naprawic skladanie sciezki
        while current_stop != start_stop:
            shortest_distance = float('inf')
            next_stop = None
            for adjacent_stop, departure_time, arrival_time, line in self.get_adjacent_vertices(current_stop):
                if distances[adjacent_stop] < shortest_distance and adjacent_stop not in visited:
                    visited.add(current_stop)
                    shortest_distance = distances[adjacent_stop]
                    next_stop = adjacent_stop
            if current_stop == end_stop:
                arrival_time = (datetime.combine(datetime.today(), start_time) + timedelta(seconds=shortest_distance)).time() # to jest do przedostatniego
                print("Arrival time at end stop:", arrival_time)
            path.insert(0, (next_stop, best_connections[next_stop], shortest_distance))
            current_stop = next_stop

        print("Shortest path:", path)

        '''
        for stop in path:
            if len(stop) == 2:
                print(stop[0] + ' Line: ' + stop[1])
            else:
                print(stop)
                '''

    def __str__(self):
        return str(self.graph)


if __name__ == '__main__':
    connections_graph = StopGraph()
    csv_reader = CSVReader("connection_graph.csv")
    records = csv_reader.read_records()

    for record in records:
        name = record["start_stop"]
        lat = record["start_stop_lat"]
        lon = record["start_stop_lon"]
        connections_graph.add_stop(Stop(name.lower(), lat, lon))

    for record in records:
        start_name = record["start_stop"]
        end_name = record["end_stop"]
        departure = record["departure_time"]
        arrival = record["arrival_time"]
        line = record["line"]
        connections_graph.add_connection(start_name.lower(), end_name.lower(), departure, arrival, line)

    #start_stop = input("Enter start stop: ").lower()
    #end_stop = input("Enter end stop: ").lower()
    #start_time = input("Enter start time (in format HH:MM:SS): ")

    #connections_graph.find_shortest_path(start_stop, end_stop, start_time)
    connections_graph.find_shortest_path('galeria dominikańska', 'ogród botaniczny', '18:29:00')
