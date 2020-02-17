import re

def sanitize(input):
    return re.sub("[^\w '-]", "", input)