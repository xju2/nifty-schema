cmake_minimum_required(VERSION 3.10)
project(nifty_common_schema LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)

# 2. If not found, download and build it automatically
if(NOT Protobuf_FOUND)
    message(STATUS "Protobuf not found. Downloading and building from source...")
    include(FetchContent)
    FetchContent_Declare(
        protobuf
        GIT_REPOSITORY https://github.com/protocolbuffers/protobuf.git
        GIT_TAG        v33.5  # Matches your intended versioning
        GIT_SUBMODULES ""     # Faster download
    )
    set(protobuf_BUILD_TESTS OFF CACHE BOOL "Disable tests" FORCE)
    set(protobuf_INSTALL OFF CACHE BOOL "Disable install" FORCE)

    FetchContent_MakeAvailable(protobuf)

    # Map the FetchContent targets to the standard names used by find_package
    add_library(protobuf::libprotobuf ALIAS libprotobuf)
    set(Protobuf_PROTOC_EXECUTABLE protoc)
endif()

# Define the proto source
set(PROTO_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/proto")
set(PROTO_FILE "${PROTO_ROOT}/nifty_common/v1/nifty_common.proto")

# Generate C++ files
# --proto_path points to the root so that 'import "nifty_common/v1/..."' works
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS
    APPEND_PATH "${PROTO_ROOT}"
    PROTOS "${PROTO_FILE}")

add_library(nifty_schema ${PROTO_SRCS} ${PROTO_HDRS})

# Allow users to #include "nifty_common/v1/nifty_common.pb.h"
target_include_directories(nifty_schema PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
    $<INSTALL_INTERFACE:include>)

target_link_libraries(nifty_schema PUBLIC protobuf::libprotobuf)
