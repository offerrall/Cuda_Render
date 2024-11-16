import subprocess
import os
import platform
import shutil

# Configuración de rutas
CUDA_PATH = "C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v12.6"
GLEW_PATH = "C:/C_LIBRERIAS/glew-2.1.0"
SDL2_PATH = "C:/C_LIBRERIAS/SDL2-2.30.9"

def build_cuda_dll():
    # Verificar dependencias
    if not os.path.exists(CUDA_PATH):
        print(f"El directorio de CUDA no existe: {CUDA_PATH}")
        return
    if not os.path.exists(GLEW_PATH):
        print(f"El directorio de GLEW no existe: {GLEW_PATH}")
        return
    if not os.path.exists(SDL2_PATH):
        print(f"El directorio de SDL2 no existe: {SDL2_PATH}")
        return

    # Obtener directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cuda_source = os.path.join(current_dir, "cuda_render.cpp")
    output_dll = "cuda_render.dll"

    # Verificar archivo fuente
    if not os.path.exists(cuda_source):
        print(f"No se encuentra el archivo fuente: {cuda_source}")
        return

    # Comando de compilación
    nvcc_cmd = [
        "nvcc",
        "-O3",
        "--shared",
        "-Xcompiler", "/MD",
        "-Xlinker", "/NODEFAULTLIB:libcmt.lib",  # Opción de linker corregida
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
        "-Xcompiler", "/D_WINDOWS"
    ]

    try:
        print(f"Compilando desde: {cuda_source}")
        print(f"Salida a: {output_dll}")
        subprocess.check_call(nvcc_cmd)
        print(f"DLL creada exitosamente: {output_dll}")

        # Copiar SDL2.dll
        sdl_dll = os.path.join(SDL2_PATH, "lib/x64/SDL2.dll")
        if os.path.exists(sdl_dll):
            shutil.copy2(sdl_dll, current_dir)
            print(f"Copiado {sdl_dll} al directorio actual")

        # Limpiar archivos temporales
        for ext in ['.exp', '.lib']:
            temp_file = output_dll.replace('.dll', ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)

    except subprocess.CalledProcessError as e:
        print(f"Error durante la compilación: {e}")
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
    os.remove("./cuda_render_src/SDL2.dll")