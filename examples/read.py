import nifty_common_pb2 as pb
from utils import NiftyConverter

with open("nifty_common.bin", "rb") as f:
    batch = pb.BoardState()
    batch.ParseFromString(f.read())
    print("Nodes:", batch.nodes.shape, batch.nodes.dtype)
    print("Edge Index:", batch.edge_index.shape, batch.edge_index.dtype)
    print("Edge Attributes:", batch.edge_attributes.shape, batch.edge_attributes.dtype)

    converter = NiftyConverter()
    data = converter.to_pyg(batch)
    print("BoardState converted to PyTorch Geometric Data object:", data)
