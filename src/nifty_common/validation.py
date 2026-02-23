
def validate_board_state(state):
    """
    Validates that the NDArray shapes match the constants defined in the proto.
    """
    # Validate Nodes: Expected shape [N, NUM_NODE_FEATURES]
    node_features = state.nodes.shape[1]
    if node_features != GraphConstants.NUM_NODE_FEATURES:
        raise ValueError(f"Node feature mismatch. Expected {GraphConstants.NUM_NODE_FEATURES}, got {node_features}")

    # Validate Edges: Expected shape [E, NUM_EDGE_FEATURES]
    edge_features = state.edge_attributes.shape[1]
    if edge_features != GraphConstants.NUM_EDGE_FEATURES:
        raise ValueError(f"Edge feature mismatch. Expected {GraphConstants.NUM_EDGE_FEATURES}, got {edge_features}")
