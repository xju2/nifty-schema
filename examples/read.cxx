#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "nifty_common.pb.h"

using nifty_common::v1::BoardState;
using nifty_common::v1::NDArray;

template <typename T>
std::vector<T> to_vector(const NDArray& array, NDArray::DataType expected_dtype) {
  if (array.dtype() != expected_dtype) {
    throw std::runtime_error("unexpected dtype");
  }
  if (array.raw_data().size() % static_cast<int>(sizeof(T)) != 0) {
    throw std::runtime_error("raw_data is not aligned to dtype size");
  }

  const std::size_t count = array.raw_data().size() / sizeof(T);
  std::vector<T> out(count);
  std::memcpy(out.data(), array.raw_data().data(), array.raw_data().size());
  return out;
}

int main(int argc, char** argv) {
  const std::string in_path = argc > 1 ? argv[1] : "examples/nifty_common.bin";

  BoardState state;
  std::ifstream in(in_path, std::ios::binary);
  if (!in) {
    std::cerr << "Failed to open input file: " << in_path << '\n';
    return 1;
  }
  if (!state.ParseFromIstream(&in)) {
    std::cerr << "Failed to parse BoardState from: " << in_path << '\n';
    return 1;
  }

  std::cout << "Version: " << state.version() << '\n';
  std::cout << "Creator ID: " << state.creator_id() << '\n';
  std::cout << "Sequence number: " << state.sequence_number() << '\n';
  std::cout << "Timestamp: " << state.timestamp() << '\n';
  std::cout << "Nodes shape: [" << state.nodes().shape(0) << ", " << state.nodes().shape(1) << "]\n";
  std::cout << "Edge count: " << state.edge_index().shape(1) << '\n';

  const std::vector<float> node_values = to_vector<float>(state.nodes(), NDArray::FLOAT32);
  if (node_values.size() < 4) {
    std::cerr << "nodes is smaller than one row of 4 features\n";
    return 1;
  }
  std::cout << "First node features: ["
            << node_values[0] << ", "
            << node_values[1] << ", "
            << node_values[2] << ", "
            << node_values[3] << "]\n";

  const std::vector<float> global_values =
      to_vector<float>(state.global_context(), NDArray::FLOAT32);
  if (global_values.size() < 3) {
    std::cerr << "global_context is smaller than expected 3 features\n";
    return 1;
  }
  std::cout << "Global context: ["
            << global_values[0] << ", "
            << global_values[1] << ", "
            << global_values[2] << "]\n";

  const auto map_name_it = state.metadata().find("map_name");
  if (map_name_it != state.metadata().end()) {
    std::cout << "Metadata.map_name: " << map_name_it->second << '\n';
  }

  return 0;
}
