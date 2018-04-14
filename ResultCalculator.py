#import numpy as np
import datetime
import math
from file_handler import file_hander

class result_calculator:


    def __init__(self, id):
        gateway_filename = "gateway_delay_" + id + ".dat"
        network_filename = "network_delay_" + id + ".dat"
        availability_filename = "availability_delay_" + id + ".dat"
        availability_reference_filename = "availability_delay_reference_" + id + ".dat"
        self.gateway_delay_logfile=file_hander(gateway_filename, 100)
        self.network_delay_logfile = file_hander(network_filename, 100)
        self.availability_delay_logfile = file_hander(availability_filename, 100)
        self.availability_delay_reference_logfile = file_hander(availability_reference_filename, 100)
        self.per_counter = 0
        self.error_counter = 0
        self.meas_counter = 0
        self.packet_counter = 0
        self.gateway_cdf_buffer=[]
        self.network_cdf_buffer = []
        self.previous_time_stamp=0
        self.MEASUREMENT_INTERVAL = 2
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
            'interval_ms': 0,
            'calculated_delay':0,
            'calculated_minimum_off_period':0,
            'calculated_minimum_off_period_from_measured_delay': 0
        }

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
        rest, millisecond = string.split(".")
        r = ''.join(c for c in millisecond if c != 'Z')
        restr, minute, second = rest.split(":")
        second_to_millisecond = 1000.0 * int(second)
        minute_to_millisecond = 60.0 * int(minute) * 1000
        total_milliseconds = int(r)/1000 + minute_to_millisecond + second_to_millisecond
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
        if not self.availability_delay_logfile.addTxData(input[3]*1000):
            self.availability_delay_logfile.strore_data()
        if not self.availability_delay_reference_logfile.addTxData(measured_time_interval):
            self.availability_delay_reference_logfile.strore_data()
        self.data['per'] = self.per_calculator(input[2])
        self.data['interval'] = input[3]
        self.data['measinterval'] = measured_time_interval
        self.data['interval_ms'] = input[3] * 1000
        self.data['calculated_delay']=self.calc_ref_delay(input)
        self.data['calculated_minimum_off_period']=self.minumum_off_period_time(self.data['calculated_delay']/1000)
        self.data['calculated_minimum_off_period_from_measured_delay'] = self.minumum_off_period_time(self.data['gatewaydelay']/1000)

        return self.data

    def calc_ref_delay(self,input):
       # input = int(delay), str_time, int(counter), float(transmission), integer_datarate_values[0], \
       #         integer_datarate_values[1], integer_datarate_values[3]
       # return int_sf, int_bw, int_cr

        sf = input[4]
        bw = input[5]
        de = 0
        CR = input[6]
        PL = input[7] + 15
        H = 1
        n_preample = 8
        tsym = math.pow(2, sf) / bw
        Tpreample = (n_preample + 4.25) * tsym
        print("symbol time in ms", tsym * 1000)
        symbolcount = 8 + max(math.ceil((8 * PL + 4 * sf + 28 + 16 - 20 * H) / (4 * sf - 2 * de)) * (CR + 4), 0)
        print("symbol count", symbolcount)
        T_payload = symbolcount * tsym
        total = 1000*(T_payload + Tpreample)
        print("Total calculated delay", total)
        return total

    def minumum_off_period_time(self,time_on_air):
        duty_cycle = 0.01
        minimum_off_period_time = time_on_air*((1/duty_cycle) - 1)
        return minimum_off_period_time