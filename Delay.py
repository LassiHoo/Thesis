import math

test_string = "SF7 BW125 4/5"
coding_rates = { '4/5': 1,'4/6': 2,'4/7': 3, '4/8': 4}


def calc_ref_delay():

    sf, bw, CR = return_datarate_int_val(test_string)
    de = 0
    PL = 13
    H = 1
    n_preample = 18
    tsym = math.pow(2,sf) / bw
    print("symbol time in ms",tsym*1000)

    Tpreample = (n_preample + 4.25) * tsym
    symbolcount = 8 + max(math.ceil((8 * PL + 4 * sf + 28 + 16 - 20 * H) / (4 * sf - 2 * de)) * (CR + 4), 0)
    print("symbol count",symbolcount)
    T_payload = symbolcount * tsym
    total = T_payload + Tpreample
    return total

def return_datarate_int_val(input):

    sf, bw, cr = input.split(' ')
    int_sf = string_to_int(sf)
    int_bw = string_to_int(bw) * 1000
    int_cr = coding_rates[cr]
    print("int sf: ", int_sf)
    print("int bw: ", int_bw)
    print("int cr: ", int_cr)

    return int_sf, int_bw, int_cr

def string_to_int(string):
    string_sf=''
    for s in string:
        if s.isdigit():
            string_sf = s + string_sf
    string_sf = string_sf[::-1]
    int_sf = int(string_sf)
    return int_sf

print("delay result",calc_ref_delay())
