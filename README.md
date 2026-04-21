[![Generate Proto Code](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml/badge.svg?branch=main)](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml)
# nifty-schema
NIFTY Board Game Schema

## A graph-based schema for representing board game state and rules
This repository defines a schema for representing the state of a board game using Protocol Buffers (protobuf) that supports
 1) data serialization, and
 2) interoperability between Python and C++.


We choose a graph-based representation of board state where nodes represent cells on the board and edges represent possible moves or connections between cells. This flexible representation can capture a wide variety of board designs.

In addition to the graph tensors, we store schema metadata (`version`, `creator_id`), simulation progression (`sequence_number`, `timestamp`), and extensible maps (`auxiliary_data`, `metadata`). Feature ordering is standardized through `GraphConstants` so `nodes`, `edge_attributes`, and `global_context` follow fixed column indices and shapes.

Details of the graph representation are described below.

### Nodes and node features
`nodes` is a 2D tensor of shape [num_nodes, num_node_features] where each row corresponds to a node in the graph. The row index is automatically assigned as the node index, which may be different from the `NODE_ID` feature described below.

Each `node` represents a cell on the board game with features ordered as follows (order matters!):
* `NODE_ID`: Unique identifier for the node.
* `NODE_KIND`: Categorical feature indicating the type of node. Three possible values: `UNKNOWN`, `SOURCE`, `SINK`.
* `NODE_PACKET`: Number of pieces at the node. Each piece presents a data packet.
* `NODE_HOPS`: Number of hops the cell away from the SINK node (For example, that's the Manhattan distance in a grid).

The total number of nodes determines the board size.

### Edges
`edge_index` is a 2D tensor of shape [2, num_edges] where each column corresponds to an edge in the graph. The first row contains the source node indices and the second row contains the target node indices for each edge. The column index is automatically assigned as the edge index.

Each `edge` represents a directional connection between two nodes: [`source_node_index`, `target_node_index`].

The `edge_index` determines the graph connectivity, that is the topology information of the board game. For example, for a grid-like board game, the `edge_index` would be constructed to connect adjacent cells.

We expect the `edge_index` to be static across time steps, but it can be dynamic in principle to support dynamic graph structures.

### Edge attributes
Each `edge` has the following ordered features stored in `edge_attributes` (order matters!):
* `EDGE_CAPACITY`: Maximum number of packets that can traverse this edge per time step.
* `EDGE_CONGESTION`: Congestion level of the edge (0.0 to 1.0), the ratio of `NODE_PACKET` at the destination node to `EDGE_CAPACITY`.

### Global context
`global_context` is a 1D tensor of shape [num_global_features] that contains global features relevant to game rules, board state, etc. The features are ordered as follows (order matters!):
* `MAX_NEW_PIECES_ALLOWED_PER_CELL`: Maximum number of new pieces that can be added to any cell per time step.
* `CELL_OVERFLOW_ALLOWED`: Flag if cell overflow is allowed (1 if allowed, 0 if not).
* `ZERO_MOVE_ALLOWED`: Flag if zero-move is allowed for all pieces (1 if allowed, 0 if not).


## Common Interface for Board Game

### Routing policy

```c++
#include "nifty_common.pb.h"
// C++ interface for routing policy
class RoutingPolicy {
public:
    // Given the current board state, compute the next move for each piece.
    // The move is represented as a list of edges that the piece will traverse.
    // Note that the move can be empty (zero-move) for some cells if allowed by the rules.
    // Each source node should have at most one outgoing edge in the route.
    virtual std::vector<std::vector<int>> route(const BoardState& board_state) = 0;
};
```

```python
# Python interface for routing policy
from abc import ABC, abstractmethod
import numpy as np
from nifty_common.v1 import nifty_common_pb2 as schema
class RoutingPolicy(ABC):
    @abstractmethod
    def route(self, board_state: schema.BoardState) -> np.ndarray:
        """
        Given the current board state, compute the next move for each piece.
        The move is represented as a list of edges that the piece will traverse.
        Note that the move can be empty (zero-move) for some cells if allowed by the rules.
        Each source node should have at most one outgoing edge in the route.
        """
        pass
```

## Instructions

### Run C++ examples

Build the repository and C++ examples:
```bash
make build_cpp
cmake --build build --target example_create_cpp example_read_cpp
```

Create and read a sample `BoardState` file:
```bash
./build/example_create_cpp examples/nifty_common.bin
./build/example_read_cpp examples/nifty_common.bin
```

### Run Python examples

Install Python dependencies and the local package:
```bash
make install
```

Create and read the same `BoardState` file in Python:
```bash
uv run python examples/create.py examples/nifty_common.bin
uv run python examples/read.py examples/nifty_common.bin
```
