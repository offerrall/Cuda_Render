from cffi import FFI
from typing import TypeAlias, Optional, Any

ffi = FFI()

# Definición C minimalista
ffi.cdef("""
    // Tipos
    typedef struct { unsigned char x, y, z, w; } uchar4;
    typedef struct CudaRenderer CudaRenderer;
    
    // API
    CudaRenderer* create_renderer(int width, int height);
    void destroy_renderer(CudaRenderer* renderer);
    void display_buffer(CudaRenderer* renderer, void* cuda_buffer);
    bool should_quit(CudaRenderer* renderer);
""")

# Cargar la biblioteca
_lib = ffi.dlopen("cuda_render.dll")

# Tipo para el handle del renderer
RenderHandle: TypeAlias = Any

def create_renderer(width: int, height: int) -> Optional[RenderHandle]:
    """Crear un nuevo renderer CUDA."""
    return _lib.create_renderer(width, height)

def destroy_renderer(renderer: RenderHandle) -> None:
    """Liberar recursos del renderer."""
    _lib.destroy_renderer(renderer)

def display_buffer(renderer: RenderHandle, cuda_buffer: Any) -> None:
    """Mostrar un buffer CUDA en la ventana."""
    buffer_ptr = ffi.cast("void*", cuda_buffer)
    _lib.display_buffer(renderer, buffer_ptr)

def should_quit(renderer: RenderHandle) -> bool:
    """Comprobar si se debe cerrar la ventana."""
    return bool(_lib.should_quit(renderer))