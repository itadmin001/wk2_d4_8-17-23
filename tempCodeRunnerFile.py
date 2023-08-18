class get_print():
    def __init__(self):
        self.str_in = ""
        self.get_String()

    def get_String(self):
        self.str_in = input("Enter your string: ")
        self.print_String()
    
    def print_String(self):
        print(self.str_in+" Returned")


my_string = get_print()