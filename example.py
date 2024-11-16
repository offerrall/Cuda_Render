from cuda_composer import create_buffer, clear_color
from cuda_render import create_renderer, destroy_renderer, display_buffer, begin_frame, end_frame, should_close



ventana = 1920, 1080
# Crear ventana
renderer = create_renderer("Test Window", 1920, 1080)

# Crear buffer CUDA
buffer = create_buffer(1920, 1080)

try:
    # Loop principal
    while not should_close(renderer):
        begin_frame(renderer)
        
        # Actualizar buffer (ejemplo: color azul)
        clear_color(buffer, 1920, 1080, 0, 0, 255, 255)
        
        # Mostrar
        display_buffer(renderer, buffer)
        end_frame(renderer)
finally:
    # Limpieza
    destroy_renderer(renderer)