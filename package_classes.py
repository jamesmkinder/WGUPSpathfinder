class package:
    """A class that stores the information about an individual package"""

    def __init__(self, id, ad, city, state, zip, dd, kilo, notes):
        self.package_id = id
        self.address = ad
        self.city = city
        self.zip = zip
        self.delivery_deadline = dd
        self.weight = kilo
        self.notes = notes
        self.picked_up = None
        self.delivered = None
        self.status = 'not delivered'


    def __eq__(self, other):
        return int(self.package_id) == other

    def __hash__(self):
        return hash(int(self.package_id))


class package_hash:
    """A class that stores the hash table for all packages"""

    def __init__(self, hash_size):
        self.packages = []
        for i in range(hash_size):
            self.packages.append([])

    def insert(self, new_package):
        hash_value = hash(new_package) % len(self.packages)
        packages = self.packages[hash_value]
        packages.append(new_package)

    def delete(self, package_id):
        hash_value = hash(package_id) % len(self.packages)
        packages = self.packages[hash_value]

        if package_id in packages:
            package_index = packages.index(package_id)
            packages.remove(package_index)
        else:
            return None

    def search(self, searched_package_id):
        hash_value = hash(searched_package_id) % len(self.packages)
        packages = self.packages[hash_value]
        if searched_package_id in packages:
            package_index = packages.index(searched_package_id)
            return packages[package_index]
        else:
            return None

    def print(self, id, time_input):
        hash_value = hash(id) % len(self.packages)
        packages = self.packages[hash_value]
        if id in packages:
            package_index = packages.index(id)
            found_package = packages[package_index]
            print('ID:', found_package.package_id, '\taddress: ', found_package.address, '\tdeadline: ', found_package.delivery_deadline, '\ncity: ', found_package.city, '\tzip: ', found_package.zip, '\tweight: ',
                  found_package.weight)
            time_picked_up = self.search(id).picked_up
            time_picked_up = time_picked_up.split(':')
            time_delivered = self.search(id).delivered
            time_delivered = time_delivered.split(':')
            time_input = time_input.split(':')
            if int(time_input[0]) > int(time_delivered[0]):
                if int(time_delivered[1]) < 10:
                    print('status: delivered at ', time_delivered[0], ':0', time_delivered[1], sep='')
                else:
                    print('status: delivered at ', self.search(id).delivered)
            elif int(time_input[0]) < int(time_delivered[0]):
                if int(time_input[0]) > int(time_picked_up[0]):
                    print('status: en route')
                elif int(time_input[0]) < int(time_picked_up[0]):
                    print('status: at the hub')
                else:
                    if int(time_input[1]) >= int(time_picked_up[1]):
                        print('status: en route')
                    else:
                        print('status: at the hub')
            elif int(time_input[0]) == int(time_delivered[0]):
                if int(time_input[1]) >= int(time_delivered[1]):
                    if int(time_delivered[1]) < 10:
                        print('status: delivered at ', time_delivered[0], ':0', time_delivered[1], sep='')
                    else:
                        print('status: delivered at ', self.search(id).delivered)
                else:
                    if int(time_input[0]) > int(time_picked_up[0]):
                        print('status: en route')
                    elif int(time_input[0]) < int(time_picked_up[0]):
                        print('status: at the hub')
                    else:
                        if int(time_input[1]) >= int(time_picked_up[1]):
                            print('status: en route')
                        else:
                            print('status: at the hub')
            return
        else:
            return None

    def print_all(self, time_delivered):
        for i in range(40):
            self.print(i + 1, time_delivered)
