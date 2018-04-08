from file_handler import file_hander
from Graph import graph
import sys

def main():

    cdf_graph = graph()
    print("*** CDF tool *** usage cdf filename1 cdfname1 filename2 cdfname2 \n")
    for arg in sys.argv:
        print("args: ",arg)
    file_name = sys.argv[1]
    file_name1 = sys.argv[3]
    handler = file_hander(file_name,0)
    handler1 = file_hander(file_name1,0)
    data=handler.read_file()
    data1 = handler1.read_file()
    print("data 1: ",data)
    print("name 1: ", sys.argv[2])
    print("data 2: ", data1)
    print("name 2: ", sys.argv[4])

    cdf_graph.cdf(data, data1, sys.argv[2], sys.argv[4])


if __name__ == "__main__":
    main()