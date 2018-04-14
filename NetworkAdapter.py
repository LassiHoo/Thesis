import codecs
from iotticket.models import device
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client
from file_handler import file_hander

import datetime
from time import time
import json
import string
from ResultCalculator import result_calculator


class network_adapter:

    username = "LassiPee"
    password = "Lorawandemo1234"
    baseurl = "https://my.iot-ticket.com/api/v1/"
    deviceId = "testi"
    MEASUREMENT_INTERVAL = 5
    dev1 ="0004A30B001F3A96"
    dev_iot_id = "610ffa1e14b94b8b8bc8079344ab9fae"
    dev2 ="BE7A000000001FF8"
    dev3 ="0004A30B001F3A95"



    def __init__(self):
        self.c = Client(self.baseurl, self.username, self.password)
        print ("network adapter initialized: " + str(self.c))
        self.dev= self.create_device()
        self.dev1 = "0004A30B001F3A96"
        self.dev2 = "BE7A000000001FF8"
        self.dev3 = "0004A30B001F3A95"
        self.dev1_result_calculator = result_calculator(self.dev1)
        self.dev2_result_calculator = result_calculator(self.dev2)
        self.dev3_result_calculator = result_calculator(self.dev3)
        self.dev1 = "0004A30B001F3A96"
        self.dev2 = "BE7A000000001FF8"
        self.dev3 = "0004A30B001F3A95"
        self.coding_rates = {  '4/5': 1,'4/6': 2,'4/7': 3, '4/8': 4}


    def create_device(self):

        d = device()
        d.set_name("Lorawan end node")
        d.set_manufacturer("Wapice")
        d.set_type("sensor")
        d.set_description("LoRaWAN test network end node")
        d.set_attributes(deviceattribute("packet", "counter"))

        c = Client(self.baseurl, self.username, self.password)

        c.registerdevice(d)
        return c


    def end_node_parser(self,data):

        end_node_address = data["EUI"]
        print("end node address", data["EUI"])
        fingernumber = "EUI" + end_node_address
        print("fingernumber", data["EUI"])
        result = self.parse(end_node_address, data)
        self.write_to_iot_ticket(data, fingernumber,result)

    def parse(self, end_node, data):

        timetost = data["gws"][0]
        print("time",timetost)
        end_node_delay_stringhex = data["data"]
        payload_lengt_in_bytes = len(end_node_delay_stringhex)
        print("data in hex",end_node_delay_stringhex)
        str_time = timetost["time"]
        e = codecs.decode(end_node_delay_stringhex, "hex")
        ascii = codecs.decode(e, "ascii")
        print("data in ascii", ascii)
        delay, counter, transmission = ascii.split(':')
        datarate = data["dr"]
        print("data rate values", datarate)
        integer_datarate_values = self.return_datarate_int_val(datarate)

        input = int(delay), str_time, int(counter), float(transmission), integer_datarate_values[0], integer_datarate_values[1], integer_datarate_values[2],payload_lengt_in_bytes

        if end_node == self.dev1:
            output = self.dev1_result_calculator.calc_result(input)
        if end_node == self.dev2:
            output = self.dev2_result_calculator.calc_result(input)
        if end_node == self.dev3:
            output = self.dev3_result_calculator.calc_result(input)

        return output

    def return_datarate_int_val(self,input):

        sf, bw, cr = input.split(' ')
        print("string sf: ",sf)
        print("string bw: ", bw)
        print("string cr: ", cr)
        int_sf =self.string_to_int(sf)
        int_bw = self.string_to_int(bw) * 1000
        int_cr = self.coding_rates[cr]
        print("int sf: ", int_sf)
        print("int bw: ", int_bw)
        print("int cr: ", int_cr)

        return  int_sf, int_bw, int_cr


    def string_to_int(self,string):
        string_sf = ''
        for s in string:
            if s.isdigit():
                string_sf = s + string_sf
        string_sf = string_sf[::-1]
        int_sf = int(string_sf)
        return int_sf

    def write_to_iot_ticket(self,data,iot_id,result):

        timeStamp = time()

        rssi = data["gws"][0]
        float_rssi = float(rssi["rssi"])
        nv = datanodesvalue()
        nv.set_name("RSSI")
        nv.set_path(iot_id)
        nv.set_dataType("double")
        nv.set_value(float_rssi)
        nv.set_timestamp(timeStamp)

        gateway_delay = result['gatewaydelay']
        float_gvd = float(gateway_delay)
        nv1 = datanodesvalue()
        nv1.set_name("Gateway delay")
        nv1.set_path(iot_id)
        nv1.set_dataType("double")
        nv1.set_value(float_gvd)

        nv1.set_timestamp(timeStamp)

        network_delay = result['networkdelay']
        float_nvd = float(network_delay)
        nv2 = datanodesvalue()
        nv2.set_name("Network delay")
        nv2.set_path(iot_id)
        nv2.set_dataType("double")
        nv2.set_value(float_nvd)
        nv2.set_timestamp(timeStamp)

        per = result['per']
        float_per = float(per)
        nv3 = datanodesvalue()
        nv3.set_name("PER")
        nv3.set_path(iot_id)
        nv3.set_dataType("double")
        nv3.set_value(float_per)
        nv3.set_timestamp(timeStamp)

        interval = result['interval']
        float_interval = float(interval)
        nv4 = datanodesvalue()
        nv4.set_name("Measurement interval")
        nv4.set_path(iot_id)
        nv4.set_dataType("double")
        nv4.set_value(float_interval)
        nv4.set_timestamp(timeStamp)

        measinterval = result['measinterval']
        float_measinterval = float(measinterval)
        nv5 = datanodesvalue()
        nv5.set_name("Measured interval")
        nv5.set_path(iot_id)
        nv5.set_dataType("double")
        nv5.set_value(float_measinterval)
        nv5.set_timestamp(timeStamp)

        interval_ms = result['interval_ms']
        float_interval_ms = float(interval_ms)
        nv6 = datanodesvalue()
        nv6.set_name("Measurement interval (ms)")
        nv6.set_path(iot_id)
        nv6.set_dataType("double")
        nv6.set_value(float_interval_ms)
        nv6.set_timestamp(timeStamp)

        snr = data["gws"][0]
        float_snr = float(snr["snr"])
        nv7 = datanodesvalue()
        nv7.set_name("snr")
        nv7.set_path(iot_id)
        nv7.set_dataType("double")
        nv7.set_value(float_snr)
        nv7.set_timestamp(timeStamp)

        reference_delay = result['calculated_delay']
        float_reference_delay = float(reference_delay)
        nv8 = datanodesvalue()
        nv8.set_name("Reference delay")
        nv8.set_path(iot_id)
        nv8.set_dataType("double")
        nv8.set_value(float_reference_delay)
        nv8.set_timestamp(timeStamp)

        time_off_calculated = result['calculated_minimum_off_period']
        float_time_off_calculated = float(time_off_calculated )
        nv9 = datanodesvalue()
        nv9.set_name("Calculated minimum time off delay")
        nv9.set_path(iot_id)
        nv9.set_dataType("double")
        nv9.set_value(float_time_off_calculated)
        nv9.set_timestamp(timeStamp)

        time_off_calculated_from_meas = result['calculated_minimum_off_period_from_measured_delay']
        float_time_off_calculated_from_meas = float(time_off_calculated_from_meas)
        nv10 = datanodesvalue()
        nv10.set_name("Calculated minimum time off delay from measurement result")
        nv10.set_path(iot_id)
        nv10.set_dataType("double")
        nv10.set_value(float_time_off_calculated_from_meas)
        nv10.set_timestamp(timeStamp)

        c = Client(self.baseurl, self.username, self.password)

        print(c.writedata(self.dev_iot_id, nv, nv1,nv2, nv3, nv4, nv5, nv6, nv7, nv8, nv9, nv10 ))
