from cffi import FFI
from typing import TypeAlias, Optional, Any

# Inicializar CFFI
ffi = FFI()

# Definición de las interfaces C desde el encabezado
ffi.cdef("""
    typedef struct { unsigned char x, y, z, w; } uchar4;
    typedef struct CudaRenderer CudaRenderer;

    CudaRenderer* create_renderer(int width, int height);
    void destroy_renderer(CudaRenderer* renderer);
    void display_buffer(CudaRenderer* renderer, void* cuda_buffer);
    bool should_quit(CudaRenderer* renderer);
""")

# Cargar la biblioteca compartida (DLL)
try:
    _lib = ffi.dlopen("cuda_render.dll")  # Cambia la ruta si es necesario
except OSError as e:
    raise RuntimeError("No se pudo cargar la DLL: verifica la ruta y la configuración.") from e

# Tipo para el handle del renderer
RenderHandle: TypeAlias = Any

def create_renderer(width: int, height: int) -> Optional[RenderHandle]:
    """Crear un nuevo renderer CUDA."""
    renderer = _lib.create_renderer(width, height)
    if renderer == ffi.NULL:
        raise RuntimeError("No se pudo crear el renderer.")
    return renderer

def destroy_renderer(renderer: RenderHandle) -> None:
    """Liberar recursos del renderer."""
    if renderer is not None:
        _lib.destroy_renderer(renderer)

def display_buffer(renderer: RenderHandle, cuda_buffer: Any) -> None:
    """Mostrar un buffer CUDA en la ventana."""
    if renderer is None or cuda_buffer is None:
        raise ValueError("Renderer o buffer no puede ser None.")
    buffer_ptr = ffi.cast("void*", cuda_buffer)
    _lib.display_buffer(renderer, buffer_ptr)

def should_quit(renderer: RenderHandle) -> bool:
    """Comprobar si se debe cerrar la ventana."""
    if renderer is None:
        raise ValueError("Renderer no puede ser None.")
    return bool(_lib.should_quit(renderer))
