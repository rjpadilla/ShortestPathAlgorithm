# Shortest Path Application
A package delivery program written in Python that solves the traveling salesman problem in which it finds the optimal shortest path in making package deliveries while having deadlines, wrong addresses, delays, and conditions used against it.

# Algorithms
There are two algorithms that will be used to perform the task of delivering packages in the routing program. The first algorithm is the Dijkstra Shortest Path algorithm. The Dijkstra shortest path algorithm allows the program to select a "shortcut" from the starting location to the ending location. Instead of using the conventional path of a delivery, the program uses the shortcut provided by the Dijkstra Shortest Path algorithm to not only cut the distance  traveled but also time.

There is one weakness of using Dijkstra shortest path algorithm and that is it set on two locations and does not allow the program to be dynamic. This is solved with using the second algorithm that aids in delivering packages, a greedy algorithm. A greedy algorithm is an algorithm that selects from a list of options and chooses the option that is most optimal. 

# Industry Standards
To comply to industry standards, Pytest was used to test if the Python modules are PEP 8 compliant.

# Installation
The routing program runs on the client's host computer either on Windows, MacOS, or Linux operating system. The program consists of the hashtable.py module which contains the package and hash table class definitions, routing.py with Graph and Vertex classes named Map and Location respectively, the algorith.py which contains the algorithms and functions that connects the program together, and the main.py which holds program initializer and the user interface.

In order for the routing program to function correctly, the user must have all these files within the same directory. The directory must also have two comma-separated value(CSV) files, one that contains the location and its adjacent location's distance and the other csv file with individual package information. A command-line interface is used to interact with the program which can be started by running it in the terminal with the commands "py -3 main.py" on Windows or "python3 main.py" on Linux/MaxOS. The routing program can also be run on an IDE, like PyCharm or VSCode as long as the configurations points to the Python path.

# Maintainability
The effiency and maintainabilty of this application is met with the use of PEP 8 documentation. Each function definition has an annotation, called type hints, which helps programmers differentiate the return value of the function. The function annotations are placed at the end of the function parameter's parentheses with the expected value that the program author had designed. These function annotations help code maintenance easier to read for a programmer especially if they come from a static-typed language, like Java or C, where return type is declared in the function name.

Another feature of software maintenance in the routing program is the use of Python docstrings. Docstrings is a comment convention style when you add a triple quoted comment in the first line of the function block. These docstring comments will tell the user the purpose of that function. This helps programmers immensely with saving time in reading lines of code and trying to figure out what a particular function does and ins place create an easier time reading the program flow.

## Technologies used
* Python
* Pytest framework
