cmake_minimum_required(VERSION 3.10)
project(nifty_common_schema LANGUAGES CXX)

find_package(Protobuf REQUIRED)

# Generate C++ code from proto
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS proto/nifty_common.proto)

add_library(nifty_schema_cpp ${PROTO_SRCS} ${PROTO_HDRS})
target_include_directories(nifty_schema_cpp PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(nifty_schema_cpp PUBLIC protobuf::libprotobuf)
