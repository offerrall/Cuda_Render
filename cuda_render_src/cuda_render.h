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

// Forward declarations
struct SDL_Window;
typedef void* SDL_GLContext;
typedef unsigned int GLuint;
struct cudaGraphicsResource;

// Main renderer structure
struct DLL_EXPORT CudaRenderer {
    SDL_Window* window;
    SDL_GLContext gl_context;
    GLuint pbo;               
    GLuint texture;           
    cudaGraphicsResource* cuda_pbo_resource;
    int width;
    int height;
    bool should_quit;
};

#ifdef __cplusplus
extern "C" {
#endif

// Exported functions
DLL_EXPORT CudaRenderer* create_renderer(int width, int height);
DLL_EXPORT void destroy_renderer(CudaRenderer* renderer);
DLL_EXPORT void display_buffer(CudaRenderer* renderer, void* cuda_buffer);
DLL_EXPORT bool should_quit(CudaRenderer* renderer);

#ifdef __cplusplus
}
#endif

#endif // CUDA_RENDERER_H
