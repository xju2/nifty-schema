import numpy as np
import torch
from torch_geometric.data import Data
import nifty_common_pb2 as pb


class NiftyConverter:
    @staticmethod
    def to_numpy(ndarray_msg: pb.NDArray, writable: bool = False) -> np.ndarray:
        """Zero-copy view of the protobuf byte buffer."""
        dtype_map = {
            pb.NDArray.FLOAT32: np.float32,
            pb.NDArray.FLOAT64: np.float64,
            pb.NDArray.INT64: np.int64,
            pb.NDArray.INT32: np.int32,
            pb.NDArray.UINT8: np.uint8,
        }
        # Default: use frombuffer for speed; it creates a view rather than a copy
        # If the resulting array is not writable but we need it to be, make a copy.
        arr = np.frombuffer(ndarray_msg.raw_data, dtype=dtype_map[ndarray_msg.dtype])
        arr = arr.reshape(ndarray_msg.shape)
        if not arr.flags.writeable and writable:
            arr = arr.copy()
        return arr

    @classmethod
    def to_pyg(cls, proto_msg: pb.BoardState, writable: bool = True) -> Data:
        """Converts BoardState to PyTorch Geometric Data object."""

        def to_numpy_fn(ndarray_msg):
            return cls.to_numpy(ndarray_msg, writable=writable)

        # Extract core graph tensors
        x = torch.from_numpy(to_numpy_fn(proto_msg.nodes))
        edge_index = torch.from_numpy(to_numpy_fn(proto_msg.edge_index))

        # Optional attributes
        edge_attr = None
        if proto_msg.edge_attributes.raw_data:
            edge_attr = torch.from_numpy(to_numpy_fn(proto_msg.edge_attributes))

        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

        # Merge auxiliary data (sim results, etc.)
        for key, ndarray in proto_msg.auxiliary_data.items():
            data[key] = torch.from_numpy(to_numpy_fn(ndarray))

        return data
