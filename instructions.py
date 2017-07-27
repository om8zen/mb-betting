from utils.files import file_read

class Instructions:
    FORMAT = file_read("instructions.txt")

    def __init__(self):
        pass

    def __repr__(self):
        return self.FORMAT

    def interpret(self, arguments):
        if len(arguments) == 0:
            print(self)
