from __future__ import annotations

import argparse

from nifty_common.v1 import nifty_common_pb2 as schema

from utils import numpy_from_ndarray


def main() -> None:
    parser = argparse.ArgumentParser(description="Read a BoardState protobuf file.")
    parser.add_argument("path", nargs="?", default="examples/nifty_common.bin")
    args = parser.parse_args()

    state = schema.BoardState()
    with open(args.path, "rb") as f:
        state.ParseFromString(f.read())

    nodes = numpy_from_ndarray(state.nodes)
    edge_index = numpy_from_ndarray(state.edge_index)
    edge_attributes = numpy_from_ndarray(state.edge_attributes)
    global_context = numpy_from_ndarray(state.global_context)

    print(f"Version: {state.version}")
    print(f"Creator ID: {state.creator_id}")
    print(f"Sequence number: {state.sequence_number}")
    print(f"Timestamp: {state.timestamp}")
    print(f"Nodes shape: {nodes.shape}")
    print(f"Edge index shape: {edge_index.shape}")
    print(f"Edge attributes shape: {edge_attributes.shape}")
    print(f"Global context: {global_context.tolist()}")
    print(f"First node row: {nodes[0].tolist()}")

    owner_ids = numpy_from_ndarray(state.auxiliary_data["owner_ids"])
    print(f"Aux owner_ids: {owner_ids.tolist()}")
    print(f"Metadata keys: {sorted(state.metadata.keys())}")


if __name__ == "__main__":
    main()
