from algorithm import look_up


def print_interface() -> None:
    """Prints out the user interface."""

    print()
    print("1 - Load routing program to end of the day(5:00PM)")
    print("2 - Load routing program to a certain point of the day")
    print("3 - Exit program")
    print()

    while True:
        choice = input('Enter choice (1-3): ')
        if choice == '1':
            filter_interface()
            break
        elif choice == '2':
            print("What time would you like the program to run to?")
            print("Use 24-hour formating")
            hour = input("Hour: ")
            minute = input("Minute: ")
            filter_interface(hour, minute)
            break
        elif choice == '3':
            print('Goodbye.')
            sys.exit(0)
        else:
            print("Invalid choice! Enter an integer from 1-3!")
            break


def filter_interface(input_hour='17', input_minute='0') -> None:
    """Give's the option for the user if they would like to
    view the results based on a package's attribute."""

    while True:
        choice = input("Would you like to filter the result's based" +
                       " on a package's attribute?" +
                       "Yes or No?\n" +
                       "If no, the program will return ALL packages. ")

        if choice in ['Yes', 'yes', 'Y', 'y']:
            components_interface(input_hour, input_minute)
            break
        elif choice in ['No', 'no', 'N', 'N']:
            look_up(int(input_hour), int(input_minute))
            break
        else:
            print("Invalid choice! Try again.")
            break


def components_interface(input_hour='17', input_minute='0') -> None:
    """Get's the corresponding components from user input."""

    while True:
        component = input("What attribute would you like to filter by?\n\t" +
                          "ID, Address, Deadline, City," +
                          "Zipcode, Weight, Status? ")

        if component in ['ID', 'id', 'Id']:
            component = 'id'
            element = input("What is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    int(element))
            break
        elif component in ['Address', 'address']:
            component = 'address'
            element = input("\tWhat is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    element)
            break
        elif component in ['Zipcode', 'zipcode']:
            component = 'zipcode'
            element = input("What is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    int(element))
            break
        elif component in ['City', 'city']:
            component = 'city'
            element = input("What is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    element)
            break
        elif component in ['Weight', 'weight']:
            component = 'weight'
            element = input("What is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    int(element))
            break
        elif component in ['Deadline', 'deadline']:
            component = 'deadline'
            element = input("What is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    element)
            break
        elif component in ['Status', 'status']:
            component = 'status'
            element = input("tWhat is the value of %s? " % component)
            look_up(int(input_hour),
                    int(input_minute),
                    component,
                    element)
            break
        else:
            print("Invalid choice! Try again.")
            break

if __name__ == "__main__":
    print_interface()
