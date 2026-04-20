from __future__ import annotations

import argparse

import numpy as np
from nifty_common.v1 import nifty_common_pb2 as schema

from utils import ndarray_from_numpy


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a BoardState protobuf file.")
    parser.add_argument("path", nargs="?", default="examples/nifty_common.bin")
    args = parser.parse_args()

    state = schema.BoardState(
        version="1.0.0",
        creator_id="python_example",
        sequence_number=7,
        timestamp=987.65,
    )

    nodes = np.array(
        [
            [0.0, 1.0, 12.0, 0.0],
            [1.0, 1.0, 8.0, 1.0],
            [2.0, 2.0, 0.0, 2.0],
        ],
        dtype=np.float32,
    )
    edge_index = np.array(
        [
            [0, 1, 0],
            [1, 2, 2],
        ],
        dtype=np.int64,
    )
    edge_attributes = np.array(
        [
            [15.0, 0.20],
            [10.0, 0.75],
            [9.0, 0.10],
        ],
        dtype=np.float32,
    )
    global_context = np.array([5.0, 1.0, 0.0], dtype=np.float32)
    owner_ids = np.array([100, 200, 300], dtype=np.int32)

    state.nodes.CopyFrom(ndarray_from_numpy(nodes))
    state.edge_index.CopyFrom(ndarray_from_numpy(edge_index))
    state.edge_attributes.CopyFrom(ndarray_from_numpy(edge_attributes))
    state.global_context.CopyFrom(ndarray_from_numpy(global_context))
    state.auxiliary_data["owner_ids"].CopyFrom(ndarray_from_numpy(owner_ids))
    state.metadata["map_name"] = "sample_arena"
    state.metadata["build"] = "demo"

    with open(args.path, "wb") as f:
        f.write(state.SerializeToString())
    print(f"Wrote {state.ByteSize()} bytes to {args.path}")


if __name__ == "__main__":
    main()
