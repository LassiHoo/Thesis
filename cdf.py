from file_handler import file_hander
from Graph import graph
import sys

def main():
    ccdf_graph = graph
    file_name = sys.argv[1]
    file_name1 = sys.argv[3]
    data=file_hander.read_file(file_name)
    data1 = file_hander.read_file(file_name)
    ccdf_graph.ccdf(data,data1,sys.argv[2],sys.argv[4])


if __name__ == "__main__":
    main()