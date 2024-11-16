import subprocess
import os
import shutil
import platform

# Paths to necessary libraries
CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6"
GLEW_PATH = "C:/C_LIBRERIAS/glew-2.1.0"
SDL2_PATH = "C:/C_LIBRERIAS/SDL2-2.30.9"

def build_cuda_dll():
    # Define paths and filenames
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cuda_source = os.path.join(current_dir, "cuda_render.cpp")
    output_dll = os.path.join(current_dir, "cuda_render.dll")
    package_dir = os.path.join(current_dir, "../cuda_render")

    # Ensure output directory exists
    os.makedirs(package_dir, exist_ok=True)

    # Define NVCC command
    nvcc_cmd = [
        "nvcc",
        "-O3",
        "--shared",
        "-Xcompiler", "/MD",  # Use the multithreaded DLL runtime
        "-Xcompiler", "/LD",  # Output a DLL
        "-Xlinker", "/NODEFAULTLIB:libcmt.lib",
        "-Xlinker", "/DLL",
        cuda_source,
        "-o", output_dll,
        # CUDA
        "-I", f"{CUDA_PATH}/include",
        "-L", f"{CUDA_PATH}/lib/x64",
        "-lcudart",
        # OpenGL and GLEW
        "-I", f"{GLEW_PATH}/include",
        "-L", f"{GLEW_PATH}/lib/Release/x64",
        "-DGLEW_STATIC",
        f"{GLEW_PATH}/lib/Release/x64/glew32s.lib",
        "opengl32.lib",
        # SDL2
        "-I", f"{SDL2_PATH}/include",
        "-L", f"{SDL2_PATH}/lib/x64",
        f"{SDL2_PATH}/lib/x64/SDL2.lib",
        # Additional compiler options
        "-Xcompiler", "/DWIN32",
        "-Xcompiler", "/D_WINDOWS",
        "-Xcompiler", "/DBUILDING_DLL"
    ]

    # Compile the CUDA source into a DLL
    try:
        print("Compiling CUDA source...")
        subprocess.check_call(nvcc_cmd)
        print(f"DLL created successfully: {output_dll}")

        # Copy necessary DLLs to the package directory
        for dll in ["SDL2.dll"]:
            src = os.path.join(SDL2_PATH, "lib/x64", dll)
            dst = os.path.join(package_dir, dll)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copied {dll} to {package_dir}")

        shutil.copy2(output_dll, os.path.join(package_dir, "cuda_render.dll"))
        print("All files copied successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")
        raise

def setup_vs_environment():
    # Only needed for Windows
    if platform.system() != "Windows":
        return

    # Locate Visual Studio installation
    possible_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community"
    ]

    vs_path = next((path for path in possible_paths if os.path.exists(path)), None)
    if not vs_path:
        print("Visual Studio not found!")
        return

    # Set up the environment for MSVC
    vcvars_path = os.path.join(vs_path, "VC\\Auxiliary\\Build\\vcvars64.bat")
    if os.path.exists(vcvars_path):
        print(f"Setting up Visual Studio environment using {vcvars_path}...")
        cmd = f'"{vcvars_path}" && set'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in proc.stdout:
            line = line.decode("cp1252").strip()
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

if __name__ == "__main__":
    setup_vs_environment()
    build_cuda_dll()
