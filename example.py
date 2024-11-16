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

ventana = 1920, 1080
# Crear ventana
renderer = create_renderer("Test Window", 1920, 1080)

# Crear buffer CUDA
buffer = create_buffer(1920, 1080)

try:
    # Loop principal
    while not should_close(renderer):
        begin_frame(renderer)
        
        # Obtener información del mouse
        mouse_x, mouse_y, left_click, right_click, middle_click = get_mouse_info(renderer)
        
        # Ejemplo: cambiar colores según los clicks
        if left_click:
            # Rojo cuando se hace click izquierdo
            clear_color(buffer, 1920, 1080, 255, 0, 0, 255)
        elif right_click:
            # Verde cuando se hace click derecho
            clear_color(buffer, 1920, 1080, 0, 255, 0, 255)
        elif middle_click:
            # Amarillo cuando se hace click con la rueda
            clear_color(buffer, 1920, 1080, 255, 255, 0, 255)
        else:
            # Color base (azul) cuando no hay clicks
            clear_color(buffer, 1920, 1080, 0, 0, 255, 255)
            
        # Imprimir información del mouse para debug
        print(f"Mouse pos: ({mouse_x}, {mouse_y}) - Left: {left_click}, Right: {right_click}, Middle: {middle_click}")
        
        # Mostrar
        display_buffer(renderer, buffer)
        end_frame(renderer)
finally:
    # Limpieza
    destroy_renderer(renderer)