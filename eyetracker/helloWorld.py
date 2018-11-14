# An demonstration file and function for documentation purpose
def helloName(msg):
    name = msg["message"]
    msg["message"] = "Hello {}".format(name)
    return msg
