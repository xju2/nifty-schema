[![Generate Proto Code](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml/badge.svg?branch=main)](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml)
# nifty-schema
NIFTY Board Game Schema


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
