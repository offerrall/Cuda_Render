from cuda_composer import create_buffer, clear_color
from cuda_render import (
    create_renderer, 
    destroy_renderer, 
    display_buffer, 
    begin_frame, 
    end_frame, 
    should_close,
    get_mouse_info
)

ventana = 1280, 720

renderer = create_renderer("Test Window", ventana[0], ventana[1])


buffer = create_buffer(ventana[0], ventana[1])

try:

    while not should_close(renderer):
        begin_frame(renderer)
        
        mouse_x, mouse_y, left_click, right_click, middle_click = get_mouse_info(renderer)
        
        if left_click:
            clear_color(buffer, ventana[0], ventana[1], 255, 0, 0, 255)
        elif right_click:
            clear_color(buffer, ventana[0], ventana[1], 0, 255, 0, 255)
        elif middle_click:
            clear_color(buffer, ventana[0], ventana[1], 255, 255, 0, 255)
        else:
            clear_color(buffer, ventana[0], ventana[1], 0, 0, 255, 255)
            
        print(f"Mouse pos: ({mouse_x}, {mouse_y}) - Left: {left_click}, Right: {right_click}, Middle: {middle_click}")
        
        display_buffer(renderer, buffer)
        end_frame(renderer)
finally:
    destroy_renderer(renderer)