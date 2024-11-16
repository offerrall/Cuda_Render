#ifndef CUDA_RENDERER_H
#define CUDA_RENDERER_H

#ifdef _WIN32
    #ifdef BUILDING_DLL
        #define DLL_EXPORT __declspec(dllexport)
    #else
        #define DLL_EXPORT __declspec(dllimport)
    #endif
#else
    #define DLL_EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

// Declaraciones de funciones exportadas
struct CudaRenderer;

DLL_EXPORT CudaRenderer* create_renderer(int width, int height);
DLL_EXPORT void destroy_renderer(CudaRenderer* renderer);
DLL_EXPORT void display_buffer(CudaRenderer* renderer, void* cuda_buffer);
DLL_EXPORT bool should_quit(CudaRenderer* renderer);

#ifdef __cplusplus
}
#endif

#endif // CUDA_RENDERER_H
