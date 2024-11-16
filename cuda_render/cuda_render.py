from cffi import FFI
from typing import TypeAlias, Tuple, Optional, Any


ffi = FFI()


ffi.cdef("""
    // Tipos compartidos con cuda_composer
    typedef struct { unsigned char x, y, z, w; } uchar4;
    
    // Estructura para información del mouse
    typedef struct {
        int x;
        int y;
        bool left_button;
        bool right_button;
        bool middle_button;
    } MouseInfo;
    
    // Tipos específicos de cuda_render
    typedef struct CudaRenderer CudaRenderer;
    
    // Funciones de cuda_render
    CudaRenderer* create_renderer(const char* title, int width, int height);
    void destroy_renderer(CudaRenderer* renderer);
    void begin_frame(CudaRenderer* renderer);
    void end_frame(CudaRenderer* renderer);
    void display_buffer(CudaRenderer* renderer, uchar4* cuda_buffer);
    bool should_close(CudaRenderer* renderer);
    void get_window_size(CudaRenderer* renderer, int* width, int* height);
    void get_mouse_info(CudaRenderer* renderer, MouseInfo* info);
""")


_lib = ffi.dlopen("cuda_render.dll")

RenderHandle: TypeAlias = Any

def create_renderer(title: str, width: int, height: int) -> Optional[RenderHandle]:
    return _lib.create_renderer(
        ffi.new("char[]", title.encode('utf-8')),
        width,
        height
    )

def destroy_renderer(renderer: RenderHandle) -> None:
    _lib.destroy_renderer(renderer)

def begin_frame(renderer: RenderHandle) -> None:
    _lib.begin_frame(renderer)

def end_frame(renderer: RenderHandle) -> None:
    _lib.end_frame(renderer)

def display_buffer(renderer: RenderHandle, cuda_buffer: Any) -> None:
    cuda_buffer_ptr = ffi.cast("uchar4*", cuda_buffer)
    _lib.display_buffer(renderer, cuda_buffer_ptr)

def should_close(renderer: RenderHandle) -> bool:
    return bool(_lib.should_close(renderer))

def get_window_size(renderer: RenderHandle) -> Tuple[int, int]:
    width = ffi.new("int*")
    height = ffi.new("int*")
    _lib.get_window_size(renderer, width, height)
    return width[0], height[0]

def get_mouse_info(renderer: RenderHandle) -> Tuple[int, int, bool, bool, bool]:
    info = ffi.new("MouseInfo*")
    _lib.get_mouse_info(renderer, info)
    return (info.x, info.y, 
            bool(info.left_button), 
            bool(info.right_button), 
            bool(info.middle_button))