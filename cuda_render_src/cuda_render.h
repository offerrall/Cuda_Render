#pragma once

#include <GL/glew.h>
#include <cuda_runtime.h>

#ifdef __cplusplus
extern "C" {
#endif

struct CudaRenderer;

#ifdef _WIN32
    #define DLLEXPORT __declspec(dllexport)
#else
    #define DLLEXPORT
#endif


DLLEXPORT CudaRenderer* create_renderer(int width, int height);
DLLEXPORT void destroy_renderer(CudaRenderer* renderer);
DLLEXPORT void display_buffer(CudaRenderer* renderer, void* cuda_buffer);
DLLEXPORT bool should_quit(CudaRenderer* renderer);

#ifdef __cplusplus
}
#endif