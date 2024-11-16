#define BUILDING_DLL
#include "cuda_render.h"
#include <SDL.h>
#include <GL/glew.h>
#include <cuda_gl_interop.h>

// Estructura interna del renderer
struct CudaRenderer {
    SDL_Window* window;
    SDL_GLContext gl_context;
    GLuint pbo;
    GLuint texture;
    cudaGraphicsResource* cuda_pbo_resource;
    int width;
    int height;
    bool should_quit;
};

extern "C" {

CudaRenderer* create_renderer(int width, int height) {
    SDL_Init(SDL_INIT_VIDEO);
    
    CudaRenderer* renderer = new CudaRenderer();
    renderer->width = width;
    renderer->height = height;
    renderer->should_quit = false;

    renderer->window = SDL_CreateWindow("CUDA Render",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        width, height, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
    
    renderer->gl_context = SDL_GL_CreateContext(renderer->window);

    glGenBuffers(1, &renderer->pbo);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, renderer->pbo);
    glBufferData(GL_PIXEL_UNPACK_BUFFER, width * height * 4, nullptr, GL_DYNAMIC_DRAW);
    cudaGraphicsGLRegisterBuffer(&renderer->cuda_pbo_resource, renderer->pbo, 
                                cudaGraphicsMapFlagsWriteDiscard);

    glGenTextures(1, &renderer->texture);
    glBindTexture(GL_TEXTURE_2D, renderer->texture);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    return renderer;
}

void destroy_renderer(CudaRenderer* renderer) {
    if (!renderer) return;
    cudaGraphicsUnregisterResource(renderer->cuda_pbo_resource);
    glDeleteBuffers(1, &renderer->pbo);
    glDeleteTextures(1, &renderer->texture);
    SDL_GL_DeleteContext(renderer->gl_context);
    SDL_DestroyWindow(renderer->window);
    SDL_Quit();
    delete renderer;
}

void display_buffer(CudaRenderer* renderer, void* cuda_buffer) {
    if (!renderer || !cuda_buffer) return;

    void* pbo_buffer;
    size_t buffer_size;
    cudaGraphicsMapResources(1, &renderer->cuda_pbo_resource, 0);
    cudaGraphicsResourceGetMappedPointer(&pbo_buffer, &buffer_size, 
                                        renderer->cuda_pbo_resource);
    
    cudaMemcpy(pbo_buffer, cuda_buffer, 
               renderer->width * renderer->height * 4, 
               cudaMemcpyDeviceToDevice);
    
    cudaGraphicsUnmapResources(1, &renderer->cuda_pbo_resource, 0);

    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, renderer->pbo);
    glBindTexture(GL_TEXTURE_2D, renderer->texture);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, renderer->width, renderer->height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, nullptr);

    glClear(GL_COLOR_BUFFER_BIT);
    glEnable(GL_TEXTURE_2D);
    glBegin(GL_QUADS);
        glTexCoord2f(0, 1); glVertex2f(-1, -1);
        glTexCoord2f(1, 1); glVertex2f( 1, -1);
        glTexCoord2f(1, 0); glVertex2f( 1,  1);
        glTexCoord2f(0, 0); glVertex2f(-1,  1);
    glEnd();

    SDL_GL_SwapWindow(renderer->window);
}

bool should_quit(CudaRenderer* renderer) {
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        if (event.type == SDL_QUIT) {
            renderer->should_quit = true;
        }
    }
    return renderer->should_quit;
}

}
