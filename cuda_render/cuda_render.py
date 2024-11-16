from cffi import FFI
from typing import TypeAlias, Tuple, Optional, Any


ffi = FFI()


ffi.cdef("""

    typedef struct { unsigned char x, y, z, w; } uchar4;
    
    typedef struct {
        int x;
        int y;
        bool left_button;
        bool right_button;
        bool middle_button;
    } MouseInfo;
    
    typedef struct {
        float x, y;
        unsigned char r, g, b, a;
    } LineVertex;
    
    typedef struct CudaRenderer CudaRenderer;
    
    CudaRenderer* create_renderer(const char* title, int width, int height);
    void destroy_renderer(CudaRenderer* renderer);
    void begin_frame(CudaRenderer* renderer);
    void end_frame(CudaRenderer* renderer);
    void display_buffer(CudaRenderer* renderer, uchar4* cuda_buffer);
    bool should_close(CudaRenderer* renderer);
    void get_window_size(CudaRenderer* renderer, int* width, int* height);
    void get_mouse_info(CudaRenderer* renderer, MouseInfo* info);
    
    void begin_lines(CudaRenderer* renderer);
    void draw_line(CudaRenderer* renderer, float x1, float y1, float x2, float y2, 
                  unsigned char r, unsigned char g, unsigned char b, unsigned char a);
    void end_lines(CudaRenderer* renderer);
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

def begin_lines(renderer: RenderHandle) -> None:
    _lib.begin_lines(renderer)

def draw_line(renderer: RenderHandle, start_pos: Tuple[float, float], 
              end_pos: Tuple[float, float], color: Tuple[int, int, int, int]) -> None:
    _lib.draw_line(renderer, 
                   start_pos[0], start_pos[1],
                   end_pos[0], end_pos[1],
                   color[0], color[1], color[2], color[3])

def end_lines(renderer: RenderHandle) -> None:
    _lib.end_lines(renderer)