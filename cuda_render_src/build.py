import os
import subprocess

# Paths
CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6"
GLEW_PATH = "C:/C_LIBRERIAS/glew-2.1.0"
SDL2_PATH = "C:/C_LIBRERIAS/SDL2-2.30.9"
BUILD_DIR = "build"

# Compiler and linker settings
compiler = "nvcc"
flags = [
    "-std=c++11",  # C++11 standard
    "-I", f"{GLEW_PATH}/include",
    "-I", f"{SDL2_PATH}/include",
    "-I", f"{CUDA_PATH}/include",
    "--shared",  # Build a shared library (DLL)
    "-Xcompiler", "/DLL",  # Inform the host compiler (MSVC) to build a DLL
]
linker_flags = [
    "-L", f"{GLEW_PATH}/lib/Release/x64",
    "-L", f"{SDL2_PATH}/lib/x64",
    "-L", f"{CUDA_PATH}/lib/x64",
    "-lglew32",
    "-lSDL2",
    "-lSDL2main",
    "-lcuda",
    "-lcudart",
    "-lopengl32",
]

# Create build directory if it doesn't exist
if not os.path.exists(BUILD_DIR):
    os.makedirs(BUILD_DIR)

# Source files and output
source_files = [
    "cuda_render.cpp",
]
output_file = os.path.join(BUILD_DIR, "cuda_render.dll")

# Compile command
command = [
    compiler,
    *flags,
    *source_files,
    "-o", output_file,
    *linker_flags,
]

# Execute the command
try:
    print("Compiling...")
    subprocess.check_call(command)
    print(f"Build successful: {output_file}")
except subprocess.CalledProcessError as e:
    print(f"Build failed with error: {e}")
