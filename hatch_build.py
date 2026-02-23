import os
import subprocess
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # The root of all protos
        proto_root = "proto"
        # Define paths relative to the project root
        proto_file = "proto/nifty_common/v1/nifty_common.proto"
        python_out = "src"
        cpp_out = "include" # For C++ headers

        os.makedirs(python_out, exist_ok=True)
        os.makedirs(cpp_out, exist_ok=True)

        # Execute protoc for both Python and C++
        subprocess.run([
            "protoc",
            f"--proto_path={proto_root}",
            f"--python_out={python_out}",
            f"--cpp_out={cpp_out}",
            proto_file
        ], check=True)
