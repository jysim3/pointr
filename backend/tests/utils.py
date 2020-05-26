from json import dumps

def fetch(c, method, route, queries=None, data=None, headers=None):
    if (method == 'GET'):
        return c.get(route + query(queries))
    elif (method == 'POST'):
        return c.post(route, data=dumps(data), content_type='application/json')
    elif (method == 'PATCH'):
        return c.patch(route + query(queries), data=dumps(data), content_type='application/json')
    elif (method == 'DELETE'):
        return c.delete(route)
    elif (method == 'PUT'):
        return c.put(route, data=data)
    else:
        print("INVALID METHOD")

def query(data):
    if data == None:
        return ""
    queries = []
    for (k,v) in data.items():
        queries.append(k + "=" + v)
    return "?" + "&".join(queries)