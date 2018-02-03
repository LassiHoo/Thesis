import os
import pickle
import json

class basePlatform:

    transmitterList = []
    initList=[]
    commandIndex=[]
    _number_of_transmitters = 0
    _transmitter_id = 0
    initialization_json = "init.json"

    def __init__(self):

        if not os.path.exists(self.initialization_json):
            #if file does not exists create a one
            self.data = {}
            self.data['transmit_parameters'] = []
            self.data['transmit_parameters'].append({
                'start_time': 'none',
                'send_interval_milliseconds': 8000,
                'send_count': 10000,
                'send_forever': 'true',
                'status': 'waitin_to_start',
                'interval_decrement_milliseconds': 100,
                'data_content': 'from_diagnostic_frame'
            })
            with open('data.txt', 'w') as self.initialization_json:
                json.dump(self.data, self.initialization_json)
        else:
            self.data = json.load(self.intialization_json)
        #scan transmitters
        for p in self.data['transmit_parameters']:
            self.number_of_transmitters = p

    def return_transmit_settings(self, setting):
        # try mechanism is missing
        return self.data['transmit_parameters'][setting]

    def dutyCycleOn():
        #create dutyCycle calculation here
        return False

    def readfile(self,filename):
        try:
            file = open(filename, "rb")
            read = pickle.load(file)
            return read
        except IOError:
            print("Could not open the file")
            return False

    def fileHandleOpen(name):
        #opens a transmitter or initialization file
        try:
            source = open(name, "rw")
            return source
        except IOError:
            print("Could not open the file")
            return False



#class NBiotTransmitterList