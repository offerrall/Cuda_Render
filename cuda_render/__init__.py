from .cuda_render import (
    create_renderer,
    destroy_renderer,
    begin_frame,
    end_frame,
    display_buffer,
    should_close,
    get_window_size,
    RenderHandle,
    ffi,  # Exportamos ffi para que otros módulos puedan usar los mismos tipos
)