import threading
import operator
from datetime import datetime, time


class Package:
    def __init__(self,
                 id: int = 0,
                 address: str = ' ',
                 city: str = ' ',
                 zipcode: int = 0,
                 deadline: str = ' ',
                 weight: int = 0,
                 notes: str = ' ') -> None:
        """Initializes Package object."""
        self.id = id
        self.address = address
        self.zipcode = zipcode
        self.city = city
        self.weight = weight
        self.status = None
        self.notes = notes

        if deadline == 'EOD' or deadline == ' ':
            self.deadline = time(17, 0)
        else:
            hour, minute = deadline[0:-3].split(':')
            self.deadline = time(int(hour), int(minute))

    def __str__(self) -> str:
        """Return string of the object's attributes when object is called."""
        return ('ID: %s '
                'Address: %s '
                'City: %s '
                'Zipcode: %s '
                'Weight: %s '
                'Deadline: %s '
                'Status: %s '
                'Notes: %s ') % (self.id,
                                 self.address,
                                 self.city,
                                 self.zipcode,
                                 self.weight,
                                 datetime.strptime(
                                    self.deadline.strftime('%H:%M'),
                                    '%H:%M').strftime('%I:%M%p'),
                                 self.status,
                                 self.notes)


class HashTable:

    def __init__(self,
                 initial_capacity=16,
                 location='4001 South 700 East') -> None:
        """Initializes HashTable object."""
        self.EMPTY_SINCE_START = Package("Empty")
        self.EMPTY_SINCE_REMOVED = Package("Removed")

        # Initialize table buckets to EMPTY_SINCE_START Package object.
        self.table = [self.EMPTY_SINCE_START] * initial_capacity

        # Initialize the location of the current hashtable.
        self.location = location

        # Initialize the total distance of the current hashtable.
        self.distance = 0

        self._lock = threading.Lock()

        self.id = 0

    def insert(self, item) -> bool:
        """Insert a new item into the hash table.
        Runtime complexity of O(1)."""

        package = hash(item) % len(self.table)
        packages_probed = 0
        # if package is empty, the item can be inserted at that index.
        while(packages_probed < len(self.table)):

            if self.table[package] is self.EMPTY_SINCE_START:
                self.table[package] = item
                return True

            # the package was occupied, continue probing to next index in table
            package = (package + 1) % len(self.table)
            packages_probed += 1

        return False

    def remove(self) -> None:
        """Removes a package from the hash table.
        Runtime complexity of O(n)."""
        for i, item in enumerate(self.table):
            if item.status == "Delivered":
                self.table[i] = self.EMPTY_SINCE_START

    def search(self, package_filter, data_input) -> 'package':
        """Searches the hashtable's packages based on data_input filter.
        Runtime complexity of O(n)."""
        if package_filter is None and data_input is None:
            return self
        else:
            for package in self.table:
                if (package is not self.EMPTY_SINCE_START and
                        getattr(package, package_filter) == data_input):
                    print(package)
        return '---------'

    def __str__(self):
        """Return all packages in table when object is called.
        Runtime complexity of of O(n)."""
        s = "    ---------\n"
        index = 0
        for package in self.table:
            value = str(package)
            if package is self.EMPTY_SINCE_START:
                value = 'E/S'
            s += '{:2}:|{:^6}\n'.format(index, value)
            index += 1
        s += "    ---------\n"
        return s
