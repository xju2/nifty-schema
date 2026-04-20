#include <fstream>
#include <vector>
#include "nifty_common.pb.h" // Generated from protoc

using namespace nifty_common::v1;

void serialize_simulation_to_proto() {
    int num_node_features = GraphConstants::NUM_NODE_FEATURES;
    // int num_edge_features = GraphConstants::NUM_EDGE_FEATURES;

    int num_cells = 100;
    // 1. Mock Simulation Data (e.g., 100 nodes with 3 features each)
    std::vector<float> node_data(num_cells * num_node_features, 0.5f);
    std::vector<int64_t> edges = {0, 1, 1, 2, 2, 0}; // 3 edges (source/target)

    BoardState batch;
    batch.set_version("1.0");
    batch.set_creator_id("Fluid_Sim_v4");

    // 2. Map Node Features
    NDArray* nodes = batch.mutable_nodes();

    nodes->set_dtype(NDArray::FLOAT32);
    nodes->add_shape(num_cells); // Num nodes
    nodes->add_shape(num_node_features);   // Feature dim
    // Efficiently copy the raw memory block
    nodes->set_raw_data(node_data.data(), node_data.size() * sizeof(float));

    // 3. Map Edge Index
    NDArray* edge_idx = batch.mutable_edge_index();
    edge_idx->set_dtype(NDArray::INT64);
    edge_idx->add_shape(2);
    edge_idx->add_shape(edges.size() / 2); // Number of edges
    edge_idx->set_raw_data(edges.data(), edges.size() * sizeof(int64_t));

    // 4. Serialize to disk
    std::string out_filename = "nifty_common.bin";
    std::ofstream out(out_filename, std::ios::binary);
    batch.SerializeToOstream(&out);
    std::cout << "Serialized graph size: " << batch.ByteSizeLong() << " bytes to file: " << out_filename << std::endl;
}

int main() {
    serialize_simulation_to_proto();
    return 0;
}
