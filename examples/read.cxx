#include <fstream>
#include <iostream>
#include "nifty_common.pb.h"

int main() {
    nifty_common::v1::BoardState batch;

    std::string in_filename = "nifty_common.bin";
    std::ifstream in(in_filename, std::ios::binary);
    batch.ParseFromIstream(&in);

    std::cout << "Reading from file: " << in_filename << "\n";
    std::cout << "Version: " << batch.version() << "\n";
    std::cout << "Creator ID: " << batch.creator_id() << "\n";
    std::cout << "Number of nodes: " << batch.nodes().shape(0) << "\n";
    std::cout << "Node feature dimension: " << batch.nodes().shape(1) << "\n";
    std::cout << "Number of edges: " << batch.edge_index().shape(1) << "\n";


    return 0;
}
