
#include "cuda_render.h"
#include <SDL.h>
#include <cuda_gl_interop.h>
#include <stdio.h>

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

CudaRenderer* create_renderer(const char* title, int width, int height) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL Init Error: %s\n", SDL_GetError());
        return nullptr;
    }

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1);

    CudaRenderer* renderer = new CudaRenderer();
    renderer->width = width;
    renderer->height = height;
    renderer->should_quit = false;

    renderer->window = SDL_CreateWindow(title,
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        width, height, SDL_WINDOW_OPENGL | SDL_WINDOW_SHOWN);
    if (!renderer->window) {
        printf("SDL Window Creation Error: %s\n", SDL_GetError());
        delete renderer;
        return nullptr;
    }

    renderer->gl_context = SDL_GL_CreateContext(renderer->window);
    if (!renderer->gl_context) {
        printf("OpenGL Context Creation Error: %s\n", SDL_GetError());
        SDL_DestroyWindow(renderer->window);
        delete renderer;
        return nullptr;
    }

    GLenum err = glewInit();
    if (err != GLEW_OK) {
        printf("GLEW Init Error: %s\n", glewGetErrorString(err));
        SDL_GL_DeleteContext(renderer->gl_context);
        SDL_DestroyWindow(renderer->window);
        delete renderer;
        return nullptr;
    }

    glGenBuffers(1, &renderer->pbo);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, renderer->pbo);
    glBufferData(GL_PIXEL_UNPACK_BUFFER, width * height * sizeof(uchar4), nullptr, GL_DYNAMIC_DRAW);

    cudaGraphicsGLRegisterBuffer(&renderer->cuda_pbo_resource, renderer->pbo, cudaGraphicsMapFlagsWriteDiscard);

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

void begin_frame(CudaRenderer* renderer) {
    if (!renderer) return;

    SDL_Event event;
    while (SDL_PollEvent(&event)) {
        if (event.type == SDL_QUIT) {
            renderer->should_quit = true;
        }
    }
}

void end_frame(CudaRenderer* renderer) {
    if (!renderer) return;
    SDL_GL_SwapWindow(renderer->window);
}

void display_buffer(CudaRenderer* renderer, uchar4* cuda_buffer) {
    if (!renderer || !cuda_buffer) return;

    uchar4* pbo_buffer;
    size_t buffer_size;
    cudaGraphicsMapResources(1, &renderer->cuda_pbo_resource, 0);
    cudaGraphicsResourceGetMappedPointer((void**)&pbo_buffer, &buffer_size, renderer->cuda_pbo_resource);
    
    cudaMemcpy(pbo_buffer, cuda_buffer, renderer->width * renderer->height * sizeof(uchar4), cudaMemcpyDeviceToDevice);
    
    cudaGraphicsUnmapResources(1, &renderer->cuda_pbo_resource, 0);

    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, renderer->pbo);
    glBindTexture(GL_TEXTURE_2D, renderer->texture);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, renderer->width, renderer->height, 0, GL_RGBA, GL_UNSIGNED_BYTE, nullptr);

    glClear(GL_COLOR_BUFFER_BIT);
    glEnable(GL_TEXTURE_2D);
    glBegin(GL_QUADS);
        glTexCoord2f(0.0f, 0.0f); glVertex2f(-1.0f, -1.0f);
        glTexCoord2f(1.0f, 0.0f); glVertex2f( 1.0f, -1.0f);
        glTexCoord2f(1.0f, 1.0f); glVertex2f( 1.0f,  1.0f);
        glTexCoord2f(0.0f, 1.0f); glVertex2f(-1.0f,  1.0f);
    glEnd();
}

bool should_close(CudaRenderer* renderer) {
    return renderer ? renderer->should_quit : true;
}

void get_window_size(CudaRenderer* renderer, int* width, int* height) {
    if (renderer && width && height) {
        *width = renderer->width;
        *height = renderer->height;
    }
}

}