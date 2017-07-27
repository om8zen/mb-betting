def file_read(file_name):
    file_ = open(file_name, "r")
    contents = file_.read()
    file_.close()
    return contents

def file_write(file_name, string):
    file_ = open(file_name, "w")
    file_.write(string)
    file_.close()

def file_append(file_name, string):
    file_ = open(file_name, "a")
    file_.write(string)
    file_.close()
