from thread import Thread
from utils.files import file_append

thread = Thread()
thread.load()

while True:
    line = input("> ")
    if line == "exit":
        break

    if thread.interpret(line.split(" ")) != None:
        file_append("betting_history.txt", line + "\n")
        thread.save()
