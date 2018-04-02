import os
import pickle
import json

class basePlatform:

    transmitterList = []
    initList=[]
    commandIndex=[]
    _number_of_transmitters = 0
    _transmitter_id = 0
    initialization_json = "init.jso"
    def __init__(self):

        if not os.path.exists(self.initialization_json):
            #if file does not exists create a one
            self.data = {}
            self.data['transmit_parameters'] = []
            self.data['transmit_parameters1'] = []
            self.data['transmit_parameters'].append({
                'start_time': 'none',
                'send_interval_milliseconds': 8000,
                'send_count': 10000,
                'send_forever': 'true',
                'status': 'waitin_to_start',
                'interval_decrement_milliseconds': 100,
                'data_content': 'from_diagnostic_frame'
            })
            self.data['transmit_parameters1'].append({
                'start_time': 'dummy',
                'send_interval_milliseconds': 8000,
                'send_count': 10000,
                'send_forever': 'true',
                'status': 'waitin_to_start',
                'interval_decrement_milliseconds': 100,
                'data_content': 'from_diagnostic_frame'
            })
            with open(self.initialization_json, 'w') as outfile:
                json.dump(self.data, outfile)
        else:
            with open(self.initialization_json, 'r') as infile:
                self.data = json.load(infile)

    def reload_Json_data(self):
        with open(self.initialization_json, 'r') as infile:
            self.data = json.load(infile)

    def store_Json_data(self):
        with open(self.initialization_json, 'r') as outfile:
            self.data = json.dump(outfile)

    def dutyCycleOn():
        #create dutyCycle calculation here
        return False
