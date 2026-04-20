#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "nifty_common.pb.h"

using nifty_common::v1::BoardState;
using nifty_common::v1::NDArray;

template <typename T>
NDArray make_ndarray(
    NDArray::DataType dtype,
    const std::vector<std::int64_t>& shape,
    const std::vector<T>& values) {
  std::int64_t expected = 1;
  for (std::int64_t dim : shape) {
    expected *= dim;
  }
  if (expected != static_cast<std::int64_t>(values.size())) {
    throw std::runtime_error("shape does not match values length");
  }

  NDArray out;
  out.set_dtype(dtype);
  for (std::int64_t dim : shape) {
    out.add_shape(dim);
  }
  out.set_raw_data(values.data(), static_cast<int>(values.size() * sizeof(T)));
  return out;
}

int main(int argc, char** argv) {
  const std::string out_path = argc > 1 ? argv[1] : "examples/nifty_common.bin";

  BoardState state;
  state.set_version("1.0.0");
  state.set_creator_id("cpp_example");
  state.set_sequence_number(42);
  state.set_timestamp(1234.5);

  // Nodes: [N, NUM_NODE_FEATURES]
  // Columns: NODE_ID, NODE_KIND, NODE_PACKET, NODE_HOPS
  const std::vector<float> nodes = {
      0.0F, 1.0F, 12.0F, 0.0F,  // source
      1.0F, 1.0F, 8.0F, 1.0F,   // source
      2.0F, 2.0F, 0.0F, 2.0F,   // sink
  };
  *state.mutable_nodes() = make_ndarray<float>(NDArray::FLOAT32, {3, 4}, nodes);

  // Edge index: [2, E] where row 0 is source and row 1 is target.
  const std::vector<std::int64_t> edge_index = {
      0, 1, 0,  // sources
      1, 2, 2,  // targets
  };
  *state.mutable_edge_index() = make_ndarray<std::int64_t>(NDArray::INT64, {2, 3}, edge_index);

  // Edge attributes: [E, NUM_EDGE_FEATURES]
  // Columns: EDGE_CAPACITY, EDGE_CONGESTION
  const std::vector<float> edge_attr = {
      15.0F, 0.20F,
      10.0F, 0.75F,
      9.0F,  0.10F,
  };
  *state.mutable_edge_attributes() = make_ndarray<float>(NDArray::FLOAT32, {3, 2}, edge_attr);

  // Global context: [NUM_GLOBAL_FEATURES]
  const std::vector<float> globals = {5.0F, 1.0F, 0.0F};
  *state.mutable_global_context() = make_ndarray<float>(NDArray::FLOAT32, {3}, globals);

  // Arbitrary team-specific output.
  const std::vector<std::int32_t> owners = {100, 200, 300};
  (*state.mutable_auxiliary_data())["owner_ids"] =
      make_ndarray<std::int32_t>(NDArray::INT32, {3}, owners);
  (*state.mutable_metadata())["map_name"] = "sample_arena";
  (*state.mutable_metadata())["build"] = "demo";

  std::ofstream out(out_path, std::ios::binary);
  if (!out) {
    std::cerr << "Failed to open output file: " << out_path << '\n';
    return 1;
  }
  if (!state.SerializeToOstream(&out)) {
    std::cerr << "Failed to serialize BoardState to: " << out_path << '\n';
    return 1;
  }

  std::cout << "Wrote " << state.ByteSizeLong() << " bytes to " << out_path << '\n';
  return 0;
}
