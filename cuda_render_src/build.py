import subprocess
import os


CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6"
GLEW_PATH = "C:/C_LIBRERIAS/glew-2.1.0"
SDL2_PATH = "C:/C_LIBRERIAS/SDL2-2.30.9"

def build_cuda_dll():
    if not os.path.exists(CUDA_PATH):
        print(f"El directorio de CUDA no existe: {CUDA_PATH}")
        print("Por favor, modifique la variable CUDA_PATH en el script.")
        return
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cuda_source = os.path.join(current_dir, "cuda_render.cpp")
    output_dll = os.path.join(current_dir, "cuda_render.dll")
    
    nvcc_cmd = [
        "nvcc",
        "--shared",
        "-Xcompiler", "/MD",
        cuda_source,
        "-o", output_dll,
        "-I", f"{CUDA_PATH}/include",
        "-I", f"{GLEW_PATH}/include",
        "-I", f"{SDL2_PATH}/include",
        "-L", f"{CUDA_PATH}/lib/x64",
        "-L", f"{GLEW_PATH}/lib/Release/x64",
        "-L", f"{SDL2_PATH}/lib/x64",
        "-lcudart",
        "-lglew32",
        "-lSDL2",
        "-lSDL2main",
        "-lopengl32",
        "-DBUILDING_DLL"
    ]
    
    try:
        print("Compilando DLL...")
        subprocess.check_call(nvcc_cmd)
        print(f"DLL creada exitosamente: {output_dll}")
        
        for ext in ['.exp', '.lib']:
            temp_file = output_dll.replace('.dll', ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
    except subprocess.CalledProcessError as e:
        print(f"Error durante la compilación: {e}")
        raise

if __name__ == "__main__":
    build_cuda_dll()
