from thread import Thread

thread = Thread()
thread.load()

while True:
    line = input("> ")
    if line == "exit":
        break

    if thread.interpret(line.split(" ")) != None:
        file_append("betting_history.txt", line + "\n")
        thread.save()
