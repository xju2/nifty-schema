from __future__ import annotations

from math import prod

import numpy as np
from nifty_common.v1 import nifty_common_pb2 as schema


_ENUM_TO_DTYPE = {
    schema.NDArray.FLOAT32: np.float32,
    schema.NDArray.FLOAT64: np.float64,
    schema.NDArray.INT64: np.int64,
    schema.NDArray.INT32: np.int32,
    schema.NDArray.UINT8: np.uint8,
}
_DTYPE_TO_ENUM = {np.dtype(v): k for k, v in _ENUM_TO_DTYPE.items()}


def ndarray_from_numpy(array: np.ndarray) -> schema.NDArray:
    """Convert a NumPy array to the NDArray schema message."""
    contiguous = np.ascontiguousarray(array)
    dtype = _DTYPE_TO_ENUM.get(contiguous.dtype)
    if dtype is None:
        raise ValueError(f"Unsupported dtype: {contiguous.dtype}")

    return schema.NDArray(
        dtype=dtype,
        shape=list(contiguous.shape),
        raw_data=contiguous.tobytes(),
    )


def numpy_from_ndarray(array_msg: schema.NDArray) -> np.ndarray:
    """Create a NumPy view from the NDArray schema message."""
    dtype = _ENUM_TO_DTYPE.get(array_msg.dtype)
    if dtype is None:
        raise ValueError(f"Unsupported NDArray dtype enum: {array_msg.dtype}")

    shape = tuple(array_msg.shape)
    expected_bytes = prod(shape) * np.dtype(dtype).itemsize
    if expected_bytes != len(array_msg.raw_data):
        raise ValueError(
            f"raw_data size mismatch. expected={expected_bytes}, got={len(array_msg.raw_data)}"
        )

    return np.frombuffer(array_msg.raw_data, dtype=dtype).reshape(shape)
