import re

def sanitize(input):
    input = str(input)
    return re.sub("[^\w '-]", "", input)