[![Generate Proto Code](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml/badge.svg?branch=main)](https://github.com/xju2/nifty-schema/actions/workflows/generate-code.yml)
# nifty-schema
NIFTY Board Game Schema


## Instructions

### For C++ Users

1. Clone the repository and navigate to the project directory.
2. Run the code generation script to generate the C++ classes from the protobuf definitions:
```bash
make build_cpp
```
3. Include the generated header files in your C++ project and link against the generated source files
```cpp
#include "nifty_common.pb.h"
```
