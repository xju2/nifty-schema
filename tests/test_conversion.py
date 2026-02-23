import pytest
import numpy as np
from nifty_common.v1 import nifty_common_pb2 as schema
from nifty_common.conversion import NiftyConverter

# Helper to check for optional PyG dependencies
def has_pyg():
    try:
        import torch
        from torch_geometric.data import Data
        return True
    except ImportError:
        return False

def test_to_numpy_conversion():
    """Verify that NDArray messages are correctly converted to NumPy arrays."""
    # 1. Create a sample 2D float32 array
    original_data = np.array([[1.5, 2.5, 3.5], [4.5, 5.5, 6.5]], dtype=np.float32)

    msg = schema.NDArray()
    msg.dtype = schema.NDArray.DataType.FLOAT32
    msg.shape.extend(original_data.shape)
    msg.raw_data = original_data.tobytes()

    # 2. Convert to numpy
    converted = NiftyConverter.to_numpy(msg)

    # 3. Assertions
    assert converted.dtype == np.float32
    assert converted.shape == (2, 3)
    assert np.allclose(converted, original_data)
    # Ensure it's a read-only view by default (frombuffer on bytes)
    assert not converted.flags.writeable

def test_to_numpy_writable_copy():
    """Verify that the writable flag triggers a copy when necessary."""
    original_data = np.array([1, 2, 3], dtype=np.int64)
    msg = schema.NDArray(
        dtype=schema.NDArray.DataType.INT64,
        shape=[3],
        raw_data=original_data.tobytes()
    )

    # Convert with writable=True
    converted = NiftyConverter.to_numpy(msg, writable=True)

    assert converted.flags.writeable
    converted[0] = 99  # Should not raise error
    assert converted[0] == 99

@pytest.mark.skipif(not has_pyg(), reason="torch or torch_geometric not installed")
def test_to_pyg_conversion():
    """Verify conversion from BoardState to PyTorch Geometric Data object."""
    import torch

    state = schema.BoardState()

    # Setup Nodes [2 nodes, 2 features]
    nodes_arr = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    state.nodes.dtype = schema.NDArray.DataType.FLOAT32
    state.nodes.shape.extend(nodes_arr.shape)
    state.nodes.raw_data = nodes_arr.tobytes()

    # Setup Edge Index [2, 1] (one edge from 0 to 1)
    edge_idx_arr = np.array([[0], [1]], dtype=np.int64)
    state.edge_index.dtype = schema.NDArray.DataType.INT64
    state.edge_index.shape.extend(edge_idx_arr.shape)
    state.edge_index.raw_data = edge_idx_arr.tobytes()

    # Setup Edge Attributes [1 edge, 1 feature]
    edge_attr_arr = np.array([[0.5]], dtype=np.float32)
    state.edge_attributes.dtype = schema.NDArray.DataType.FLOAT32
    state.edge_attributes.shape.extend(edge_attr_arr.shape)
    state.edge_attributes.raw_data = edge_attr_arr.tobytes()

    # Setup Auxiliary Data (e.g., simulation labels)
    aux_arr = np.array([42], dtype=np.int32)
    aux_msg = schema.NDArray(dtype=schema.NDArray.INT32, shape=[1], raw_data=aux_arr.tobytes())
    state.auxiliary_data["sim_id"] = aux_msg

    # Execute conversion
    data = NiftyConverter.to_pyg(state)

    # Assertions
    assert torch.is_tensor(data.x)
    assert data.x.shape == (2, 2)
    assert data.edge_index.shape == (2, 1)
    assert torch.equal(data.edge_attr, torch.tensor([[0.5]], dtype=torch.float32))
    assert torch.equal(data.sim_id, torch.tensor([42], dtype=torch.int32))

def test_unsupported_dtype():
    """Verify that an undefined dtype in the message raises a KeyError."""
    msg = schema.NDArray()
    msg.dtype = 999  # Invalid enum value
    msg.shape.append(1)
    msg.raw_data = b'\x00'

    with pytest.raises(KeyError):
        NiftyConverter.to_numpy(msg)
