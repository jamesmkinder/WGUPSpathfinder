class distance:
    """A class that identifies the distance between two addresses"""
    def __init__(self, address_a, address_b, distance_value):
        self.address_a = address_a
        self.address_b = address_b
        self.distance_value = distance_value

class distance_info_table:
    """A class that stores the information about the distance between different addresses in a hash table"""

    def __init__(self):
        self.distances = []


    def insert(self, new_distance):
        self.distances.append(new_distance)

    def search(self, id_a, id_b, packages):
        try:
            address_a = packages.search(id_a).address
        except AttributeError:
            address_a = id_a
        try:
            address_b = packages.search(id_b).address
        except AttributeError:
            address_b = id_b
        for i in range(len(self.distances)):
            if address_a == self.distances[i].address_a:
                if address_b == self.distances[i].address_b:
                    return float(self.distances[i].distance_value)
        return None



