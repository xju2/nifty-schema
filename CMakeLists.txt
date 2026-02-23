cmake_minimum_required(VERSION 3.10)
project(nifty_common_schema LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)

# Define the proto source
set(PROTO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/proto")
set(PROTO_FILE "${PROTO_ROOT}/nifty_common/v1/nifty_common.proto")

# Generate C++ files
# --proto_path points to the root so that 'import "nifty_common/v1/..."' works
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
    APPEND_PATH "${PROTO_ROOT}"
    PROTOS "${PROTO_FILE}")

add_library(nifty_schema_cpp ${PROTO_SRCS} ${PROTO_HDRS})

# Allow users to #include "nifty_common/v1/nifty_common.pb.h"
target_include_directories(nifty_schema_cpp PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:include>)

target_link_libraries(nifty_schema_cpp PUBLIC protobuf::libprotobuf)
