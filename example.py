# cuda_composer is another module that is not included in this repository
# It provides CUDA buffer creation and manipulation functions
from cuda_composer import create_buffer, clear_color

from cuda_render import create_renderer, destroy_renderer, display_buffer, should_quit

def main():
    # Create window and CUDA buffer
    width, height = 1920, 1080
    renderer = create_renderer(width, height)
    buffer = create_buffer(width, height) # CUDA buffer, RGBA format, uchar4

    try:
        # Main render loop
        while not should_quit(renderer):
            # Update buffer (example: blue color)
            clear_color(buffer, width, height, 0, 0, 255, 255)
            
            # Display the buffer
            display_buffer(renderer, buffer)
            
    finally:
        # Cleanup
        destroy_renderer(renderer)

if __name__ == "__main__":
    main()