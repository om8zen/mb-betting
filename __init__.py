from . import bet

thread = Thread()
thread.load()

while True:
    line = raw_input("> ")
    if line == "exit":
        break
    
    if thread.interpret(line.split(" ")) != None:
        file_append("betting_history.txt", line + "\n")
        thread.save()
