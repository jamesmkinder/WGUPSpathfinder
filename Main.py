# James Kinder, Student ID: 001481730
import csv

from package_classes import package, package_hash
from distance_classes import distance, distance_info_table
from truck import truck

hub = '4001 South 700 East'

#Open CSV files and place them into their respective data structures
with open('WGUPS Package File.csv') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    packages = package_hash(10)
    next(filereader)
    for id, ad, city, state, zip, dd, weight, notes in filereader:
        new_package = package(id, ad, city, state, zip, dd, weight, notes)
        packages.insert(new_package)

with open('WGUPS Distance Table.csv') as csvfile:
    filereader = csv.reader(csvfile)
    distance_table = []
    for row in filereader:
        distance_table.append(row)

#data cleanup operations

distance_table = str(distance_table).replace('[', ' ').replace(']', ' ').replace('\\n', ' ')

distance_table = str(distance_table).split(',')

for i in range(len(distance_table)):
    distance_table[i] = distance_table[i].strip('\'').strip().strip('\'')

#hash the distance table into 28 rows to create a two dimensional matrix

distance_table_hash = []
for i in range(28):
    distance_table_hash.append([])

for i in range(len(distance_table)):
    hash_value = i % 28
    distance_table_hash[hash_value].append(distance_table[i])

distances = distance_info_table()
#insert the matrix values into the distances object
for i in range(27):
    for j in range(27):
        distances.insert(
            distance(distance_table_hash[i + 1][0], distance_table_hash[0][j + 1], distance_table_hash[i + 1][j + 1]))

#initialize the trucks and manually load the first packages
truck1 = truck(1)
truck2 = truck(2)
truck1.load(packages.search(15))
truck1.load(packages.search(19))
truck1.load(packages.search(16))
truck1.load(packages.search(13))
truck1.load(packages.search(20))
truck1.load(packages.search(14))
#nearest neighbor algorithm to load the packages
for j in range(10):
    closest = 100
    for i in range(40):
        if round(distances.search(int(truck1.last_loaded.package_id), int(i + 1), packages), 1) < round(closest, 1):
            if distances.search(int(truck1.last_loaded.package_id), int(i + 1), packages) == 0:
                continue
            elif packages.search(i + 1).picked_up is not None:
                continue
            elif str(packages.search(i + 1).notes).__contains__('Delayed') or str(
                    packages.search(i + 1).notes).__contains__(
                'Wrong'):
                continue
            elif str(packages.search(i + 1).notes).__contains__('truck 2'):
                continue
            else:
                closest = distances.search(int(truck1.last_loaded.package_id), int(i + 1), packages)
                truck1.best_package = packages.search(i + 1)
    truck1.load(truck1.best_package)
#nearest neighbor for truck 2
for j in range(16):
    closest = 100
    for i in range(40):
        if round(distances.search(int(truck2.last_loaded.package_id), int(i + 1), packages), 1) < round(closest, 1):
            if distances.search(int(truck2.last_loaded.package_id), int(i + 1), packages) == 0:
                continue
            elif packages.search(i + 1).picked_up is not None:
                continue
            elif str(packages.search(i + 1).notes).__contains__('Delayed') or str(
                    packages.search(i + 1).notes).__contains__(
                'Wrong'):
                continue
            else:
                closest = distances.search(int(truck2.last_loaded.package_id), int(i + 1), packages)
                truck2.best_package = packages.search(i + 1)
    truck2.load(truck2.best_package)

#generate an array of package ids and addresses for convenience in the next section
package_ids = []
package_addresses = []
for i in range(40):
    if truck1.package_manifest.search(i + 1):
        package_ids.append(truck1.package_manifest.search(i + 1).package_id)
        package_addresses.append(truck1.package_manifest.search(i + 1).address)

#nearest neighbor algorithm to determine delivery order
for j in range(len(package_ids)):
    closest = 100
    for i in range(len(package_ids)):
        if distances.search(truck1.current_location, int(package_ids[i]), packages) < closest:
            if packages.search(int(package_ids[i])).delivered is None:
                closest = distances.search(truck1.current_location, int(package_ids[i]), packages)
                truck1.best_package = packages.search(int(package_ids[i]))
    truck1.travel(distances.search(truck1.current_location, int(truck1.best_package.package_id), packages), truck1.best_package.address)
    truck1.deliver(truck1.package_manifest.search(int(truck1.best_package.package_id)))

#repeated for truck 2
package_ids.clear()
package_addresses.clear()
for i in range(40):
    if truck2.package_manifest.search(i + 1):
        package_ids.append(truck2.package_manifest.search(i + 1).package_id)
        package_addresses.append(truck2.package_manifest.search(i + 1).address)

for j in range(len(package_ids)):
    closest = 100
    for i in range(len(package_ids)):
        if distances.search(truck2.current_location, int(package_ids[i]), packages) < closest:
            if packages.search(int(package_ids[i])).delivered is None:
                closest = distances.search(truck2.current_location, int(package_ids[i]), packages)
                truck2.best_package = packages.search(int(package_ids[i]))
    truck2.travel(distances.search(truck2.current_location, int(truck2.best_package.package_id), packages), truck2.best_package.address)
    truck2.deliver(truck2.package_manifest.search(int(truck2.best_package.package_id)))



#truck 2 is finished first so it is sent back to the hub to pick up remaining packages
truck2.travel(distances.search(truck1.current_location, hub, packages), hub)
for i in range(40):
    if packages.search(i + 1).status == 'delivered':
        continue
    else:
        truck2.load(packages.search(i + 1))

package_ids.clear()
package_addresses.clear()
for i in range(40):
    if truck2.package_manifest.search(i + 1):
        package_ids.append(truck2.package_manifest.search(i + 1).package_id)
        package_addresses.append(truck2.package_manifest.search(i + 1).address)

#manually deliver two packages to keep on schedule, then wait 18 minutes for the package address update.
truck2.travel(distances.search(truck2.current_location, 25, packages), packages.search(6).address)
truck2.deliver(truck2.package_manifest.search(25))
truck2.travel(distances.search(truck2.current_location, 6, packages), packages.search(6).address)
truck2.deliver(truck2.package_manifest.search(6))
truck2.minute_offset = 18
#nearest neighbor algorithm for the last packages
for j in range(6):
    closest = 100
    for i in range(len(package_ids)):
        if distances.search(truck2.current_location, int(package_ids[i]), packages) < closest:
            if packages.search(int(package_ids[i])).delivered is None:
                closest = distances.search(truck2.current_location, int(package_ids[i]), packages)
                truck2.best_package = packages.search(int(package_ids[i]))
    truck2.travel(distances.search(truck2.current_location, int(truck2.best_package.package_id), packages), truck2.best_package.address)
    truck2.deliver(truck2.package_manifest.search(int(truck2.best_package.package_id)))

#command line interface
print('WGUPS program\n', 'truck 1 miles: ', round(truck1.trip_odometer,1), '\n', 'truck 2 miles: ', round(truck2.trip_odometer,1),
      '\ntotal miles: ', round(float(truck1.trip_odometer) + float(truck2.trip_odometer), 2))
selected_time = input('please select a time in format hh24:mm')
while True:
    print('\nwhat would you like to do? \n', '1: look up a package\n2: print all packages\n3: change the time\n4: exit')
    prompt = input()
    if prompt == '1':
        lookup_id = int(input("please enter a package ID: "))
        packages.print(lookup_id, selected_time)
    elif prompt == '2':
        packages.print_all(selected_time)
    elif prompt == '3':
        selected_time = input('please select a new time in format hh24:mm: ')
    elif prompt == '4':
        break
