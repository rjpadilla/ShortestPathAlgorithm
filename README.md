# Shortest Path Application
A program written in Python that solves the traveling salesman problem in which it finds the optimal shortest path in making package deliveries while having deadlines, wrong addresses, delays, and conditions used against it.

# Algorithms
There are two algorithms that will be used to perform the task of delivering packages in the routing program. The first algorithm is the Dijkstra Shortest Path algorithm. The Dijkstra shortest path algorithm allows the program to select a "shortcut" from the starting location to the ending location. Instead of using the conventional path of a delivery, the program uses the shortcut provided by the Dijkstra Shortest Path algorithm to not only cut the distance  traveled but also time.

# Industry Standards
To comply to industry standards, Pytest was used to test if the Python modules are PEP 8 compliant.

# Installation
The routing program runs on the client's host computer either on Windows, MacOS, or Linux operating system. The program consists of the hashtable.py module which contains the package and hash table class definitions, routing.py with Graph and Vertex classes named Map and Location respectively, the algorith.py which contains the algorithms and functions that connects the program together, and the main.py which holds program initializer and the user interface.

In order for the routing program to function correctly, the user must have all these files with the same directory. The directory must also have two comma-separated value(CSV) files, one that contains the location and its adjacent location's distance and the other csv file with individual package information. A command-line interface is used to interact with the program which can be started by running it in the terminal with the commans "py -3 main.py" on Windows or "python3 main.py" on Linux/MaxOS. The routing program can also be run on an IDE, like PyCharm or VSCode as long as the configurations points to the Python path.
