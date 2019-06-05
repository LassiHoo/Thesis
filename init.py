import os
import json

f = open('init.jso', 'r+')
data = json.load(f)
f.close()

data['transmit_parameters'][0]['status'] = u"waiting_to_start"

f = open('init.jso', 'w')
json.dump(data, f)
f.close()
