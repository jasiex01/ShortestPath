from stop import Stop
from csv_reader import CSVReader


class StopGraph:
    def __init__(self):
        self.graph = {}
        self.counter = 0

    def add_stop(self, stop):
        if stop.name not in self.graph:
            self.graph[stop.name] = []

    def add_connection(self, start_stop_name, end_stop_name, departure_time, arrival_time, line):
        if start_stop_name in self.graph:
            self.graph[start_stop_name].append([end_stop_name, departure_time, arrival_time, line])
        #else:
        #    self.graph[start_stop.name] = [end_stop]
    #not used for now
    def get_adjacent_vertices(self, vertex):
        if vertex in self.graph:
            return self.graph[vertex]
        else:
            return []

    def __str__(self):
        return str(self.graph)

if __name__ == '__main__':
    connections_graph = StopGraph()
    csv_reader = CSVReader("connection_graph.csv")
    records = csv_reader.read_records()
    #print(records)
    for record in records:
        name = record["start_stop"]
        lat = record["start_stop_lat"]
        lon = record["start_stop_lon"]
        connections_graph.add_stop(Stop(name, lat, lon))

    for record in records:
        start_name = record["start_stop"]
        end_name = record["end_stop"]
        departure = record["departure_time"]
        arrival = record["arrival_time"]
        line = record["line"]
        connections_graph.add_connection(start_name, end_name, departure, arrival, line)

    print(connections_graph.graph["Pl. Hirszfelda"])

