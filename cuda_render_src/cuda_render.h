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

#define CUDAAPI __stdcall  // Añadimos la convención de llamada

DLLEXPORT CudaRenderer* CUDAAPI create_renderer(int width, int height);
DLLEXPORT void CUDAAPI destroy_renderer(CudaRenderer* renderer);
DLLEXPORT void CUDAAPI display_buffer(CudaRenderer* renderer, void* cuda_buffer);
DLLEXPORT bool CUDAAPI should_quit(CudaRenderer* renderer);

#ifdef __cplusplus
}
#endif