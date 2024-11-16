import subprocess
import os
import platform
import shutil

CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6"
GLEW_PATH = "C:/C_LIBRERIAS/glew-2.1.0"
SDL2_PATH = "C:/C_LIBRERIAS/SDL2-2.30.9"

def build_cuda_dll():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cuda_source = os.path.join(current_dir, "cuda_render.cpp")
    output_dll = "cuda_render.dll"

    nvcc_cmd = [
        "nvcc",
        "-O3",
        "--shared",
        "-Xcompiler", "/MD",
        "-Xcompiler", "/LD",  # Importante: para crear una DLL
        "-Xcompiler", "/DEF",  # Genera archivo .def
        "-Xlinker", "/NODEFAULTLIB:libcmt.lib",
        "-Xlinker", "/DLL",  # Explícitamente marca como DLL
        cuda_source,
        "-o", output_dll,
        # CUDA
        "-I", f"{CUDA_PATH}/include",
        "-L", f"{CUDA_PATH}/lib/x64",
        "-lcudart",
        # OpenGL y GLEW
        "-I", f"{GLEW_PATH}/include",
        "-L", f"{GLEW_PATH}/lib/Release/x64",
        "-DGLEW_STATIC",
        f"{GLEW_PATH}/lib/Release/x64/glew32s.lib",
        "opengl32.lib",
        # SDL2
        "-I", f"{SDL2_PATH}/include",
        "-L", f"{SDL2_PATH}/lib/x64",
        f"{SDL2_PATH}/lib/x64/SDL2.lib",
        # Opciones adicionales
        "-Xcompiler", "/DWIN32",
        "-Xcompiler", "/D_WINDOWS",
        "-Xcompiler", "/DBUILDING_DLL"  # Define que estamos construyendo una DLL
    ]

    try:
        subprocess.check_call(nvcc_cmd)
        print(f"DLL created successfully: {output_dll}")

        # Copiar DLLs necesarias
        sdl_dll = os.path.join(SDL2_PATH, "lib/x64/SDL2.dll")
        package_dir = os.path.join(os.path.dirname(current_dir), "cuda_render")
        
        for dll in [output_dll, "SDL2.dll"]:
            src = os.path.join(current_dir, dll)
            dst = os.path.join(package_dir, dll)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copied {dll} to package directory")

    except subprocess.CalledProcessError as e:
        print(f"Compilation error: {e}")
        raise

def setup_vs_environment():
    if platform.system() != "Windows":
        return

    vs_path = None
    possible_paths = [
        r"C:\Program Files\Microsoft Visual Studio\2022\Community",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            vs_path = path
            break

    if vs_path:
        vcvars_path = os.path.join(vs_path, "VC\\Auxiliary\\Build\\vcvars64.bat")
        if os.path.exists(vcvars_path):
            cmd = f'"{vcvars_path}" && set'
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for line in proc.stdout:
                line = line.decode('cp1252').strip()
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    setup_vs_environment()
    build_cuda_dll()