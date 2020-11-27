from package_classes import package_hash, package
import math

class truck:
    """A class that simulates the working of a delivery truck"""
    def __init__(self, id):
        self.truck_id = id
        self.capacity = 0
        self.package_manifest = package_hash(10)
        self.trip_odometer = 0.0
        self.current_location = '4001 South 700 East'
        self.last_loaded = package(1, '4001 South 700 East', 'Salt Lake City', 'UT', '84115', 'EOD', '0', 'dummy')
        self.best_package = None
        self.hour_offset = 8
        self.minute_offset = 0

    def load(self, package_to_load: package):
        if self.capacity >= 16:
            return
        hour_picked_up = str(math.floor(self.trip_odometer / 18) + self.hour_offset)
        minute_picked_up = str(round(((self.trip_odometer / 18) % 1) * 60) + self.minute_offset)
        package_to_load.picked_up = hour_picked_up + ':' + minute_picked_up
        self.last_loaded = package_to_load
        self.package_manifest.insert(package_to_load)
        print('truck id', self.truck_id, 'loaded package', package_to_load.package_id)
        self.capacity += 1

    def deliver(self, package_to_deliver):
        hour_delivered = str(math.floor(self.trip_odometer/18) + self.hour_offset)
        minute_delivered = str(round(((self.trip_odometer/18) % 1)*60) + self.minute_offset)
        if int(minute_delivered) > 60:
            minute_delivered = str(int(minute_delivered) % 60)
            hour_delivered = str(int(hour_delivered) + 1)
        package_to_deliver.delivered = hour_delivered + ':' + minute_delivered
        package_to_deliver.status = 'delivered'
        print('truck id', self.truck_id, 'delivered package', package_to_deliver.package_id)
        self.package_manifest.delete(package_to_deliver.package_id)
        self.capacity -= 1


    def travel(self, travel_distance, destination):
        self.trip_odometer += float(travel_distance)
        self.current_location = destination