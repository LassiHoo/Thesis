#import numpy as np
import datetime
import math
from file_handler import file_hander

class result_calculator:


    def __init__(self, id):
        gateway_filename = "gateway_delay" + id + ".dat"
        network_filename = "network_delay" + id + ".dat"
        self.gateway_delay_logfile=file_hander(gateway_filename, 200)
        self.network_delay_logfile = file_hander(network_filename, 200)
        self.per_counter = 0
        self.error_counter = 0
        self.meas_counter = 0
        self.packet_counter = 0
        self.gateway_cdf_buffer=[]
        self.network_cdf_buffer = []
        self.previous_time_stamp=0
        self.MEASUREMENT_INTERVAL = 10
        self.CDF_MEASUREMENT_INTERVAL = 100
        self.network_delay=0
        self.gateway_delay=0
        self.gateway_cdf_result_buffer = {}
        self.network_cdf_result_buffer = {}
        self.data={
            'per': self.per_counter,
            'gatewaydelay': self.gateway_delay,
            'networkdelay': self.network_delay,
            'measinterval': 0,
            'interval':0,
            'interval_ms': 0
        }

    # def cdf_calculation(self, samplebuffer):
    #     if len(samplebuffer)==self.CDF_MEASUREMENT_INTERVAL:
    #         del samplebuffer[:]
    #     cdfx = np.sort(samplebuffer)
    #     cdfy = np.linspace(1 / len(samplebuffer), 1.0, len(samplebuffer))
    #     return cdfx, cdfy


    def per_calculator(self, end_nodecounter):
        if ( end_nodecounter != 0):
            if end_nodecounter != (self.packet_counter + 1):
                self.error_counter= self.error_counter + 1.0
            self.meas_counter = self.meas_counter + 1
            if self.meas_counter == self.MEASUREMENT_INTERVAL:
                self.per_counter = ( self.error_counter / self.meas_counter )
                self.error_counter = 0
                self.meas_counter = 0
        self.packet_counter = end_nodecounter
        return self.per_counter

    def calc_ms(self,string):
        #print("calc_millisecond string",string)
        rest, millisecond = string.split(".")
        r = ''.join(c for c in millisecond if c != 'Z')
        restr, minute, second = rest.split(":")
        #print("second string", second)
        second_to_millisecond = 1000.0 * int(second)
        #print("second to millisecond", second_to_millisecond)
        #print("minute string", minute)
        minute_to_millisecond = 60.0 * int(minute) * 1000
        #print("minute to millisecond", minute_to_millisecond)
        total_milliseconds = int(r)/1000 + minute_to_millisecond + second_to_millisecond
        #print("total millisecond", total_milliseconds)
        self.delay = total_milliseconds
        return total_milliseconds

    def calc_result(self,input):
        print("calc result input: ", input)
        Ts = datetime.datetime.now()
        print("end node delay: ",input[0])
        end_node_delay = input[0]
        network_server_delay = (Ts.microsecond / 1000) + (Ts.minute * 60 * 1000) + (Ts.second * 1000)
        if self.previous_time_stamp != 0:
            print("Network delay: ", network_server_delay)
            print("previous delay: ",self.previous_time_stamp)
            measured_time_interval = network_server_delay - self.previous_time_stamp
            print("measured time interval: ",measured_time_interval)
        self.previous_time_stamp = network_server_delay
        print("gateway delay before calc: ", input[1])
        gateway_server_delay = self.calc_ms(input[1])
        print("gateway after calc: ", gateway_server_delay)
        # print("Network server delay milliseconds: ", network_serve_delay)
        # print("gateway server delay milliseconds: ", gateway_server_delay)
        # print("end node delay in milliseconds", end_node_delay)
        self.data['gatewaydelay'] = gateway_server_delay - end_node_delay
        self.data['networkdelay'] = network_server_delay - end_node_delay
        if not self.network_delay_logfile.addTxData(self.data['networkdelay']):
            self.network_delay_logfile.strore_data()
        if not self.gateway_delay_logfile.addTxData(self.data['gatewaydelay']):
            self.gateway_delay_logfile.strore_data()
        self.data['per'] = self.per_calculator(input[2])
        self.data['interval'] = input[3]
        self.data['measinterval'] = measured_time_interval
        self.data['interval_ms'] = input[3] * 1000
        #self.gateway_cdf_buffer.append(self.data['result']['gatewaydelay'])
        #self.gateway_cdf_result_buffer=self.cdf_calculation(self.gateway_cdf_buffer)
        #self.network_cdf_buffer.append(self.data['result']['networkdelay'])
        #self.network_cdf_result_buffer=self.cdf_calculation( self.network_cdf_buffer )
        return self.data

    def calc_ref_delay(self):

        sf = 1
        bw = 1
        de = 1
        CR = 1
        PL = 1
        H=1
        n_preample = 1
        tsym=(2*sf)/bw
        Tpreample = (n_preample + 4.25)*tsym
        symbolcount = 8 + max(math.ceil((8 * PL + 4*sf + 28 + 16 - 20*H)/(4*sf - 2*de))*(CR + 4),0)
        T_payload = symbolcount * tsym
        total = T_payload + Tpreample
        return total