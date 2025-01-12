# CUDA Render

Simple CUDA buffer renderer using OpenGL for display.

## Requirements
- CUDA Toolkit
- OpenGL
- SDL2
- Python 3.6+
- CFFI

## Installation

1. Build the C++ library:
Modify the build script build.py in cuda_render_src to match your system configuration.
Then run the following commands:
```bash
cd cuda_render_src
./compile_lib.bat  # or compile using your preferred method
```

2. Install the Python package:
```bash
pip install -e .
```

## Usage

```python
import cuda_render
import cupy as cp  # or your CUDA framework of choice

# Create renderer
renderer = cuda_render.create_renderer(width=800, height=600)

# Main loop
while not cuda_render.should_quit(renderer):
    # Your CUDA buffer here (RGBA format)
    cuda_buffer = ...  
    cuda_render.display_buffer(renderer, cuda_buffer)

# Cleanup
cuda_render.destroy_renderer(renderer)
```

## License
MIT
