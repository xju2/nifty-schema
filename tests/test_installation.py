import pytest
import numpy as np
from nifty_common.v1 import nifty_common_pb2 as schema
from nifty_common.validation import validate_board_state

def test_protobuf_generation():
    """Verify that the Protobuf classes were generated and are importable."""
    state = schema.BoardState()
    state.version = "0.1.0"
    state.creator_id = "test_suite"

    assert state.version == "0.1.0"
    assert state.creator_id == "test_suite"

def test_ndarray_structure():
    """Verify the NDArray message structure matches the schema definition."""
    array = schema.NDArray()
    array.dtype = schema.NDArray.DataType.FLOAT32
    array.shape.extend([2, 2])

    # Simulate raw data (4 floats * 4 bytes = 16 bytes)
    data = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
    array.raw_data = data.tobytes()

    assert array.dtype == schema.NDArray.DataType.FLOAT32
    assert list(array.shape) == [2, 2]
    assert len(array.raw_data) == 16

def test_validation_logic():
    """Test that the validation utility correctly identifies schema-compliant data."""
    state = schema.BoardState()

    # Setup valid Nodes [N, 4] based on GraphConstants (NODE_ID, KIND, PACKET, HOPS)
    state.nodes.shape.extend([10, 4])

    # Setup valid Edges [E, 3] based on GraphConstants (CAPACITY, CONGESTION)
    state.edge_attributes.shape.extend([20, 2])

    # This should not raise an exception
    try:
        validate_board_state(state)
    except ValueError as e:
        pytest.fail(f"Validation failed unexpectedly: {e}")

def test_invalid_data_fails():
    """Test that validation fails when the array shapes do not match GraphConstants."""
    state = schema.BoardState()

    # Provide incorrect number of columns for nodes (e.g., 2 instead of 4)
    state.nodes.shape.extend([10, 2])

    with pytest.raises(ValueError, match="Node feature mismatch"):
        validate_board_state(state)
