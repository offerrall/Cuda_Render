#pragma once

#include <GL/glew.h>
#include <cuda_runtime.h>
#include <vector>

#ifdef __cplusplus
extern "C" {
#endif

struct MouseInfo {
    int x;
    int y;
    bool left_button;
    bool right_button;
    bool middle_button;
};

struct LineVertex {
    float x, y;
    unsigned char r, g, b, a;
};

struct CudaRenderer;

__declspec(dllexport) CudaRenderer* create_renderer(const char* title, int width, int height);
__declspec(dllexport) void destroy_renderer(CudaRenderer* renderer);
__declspec(dllexport) void begin_frame(CudaRenderer* renderer);
__declspec(dllexport) void end_frame(CudaRenderer* renderer);
__declspec(dllexport) void display_buffer(CudaRenderer* renderer, uchar4* cuda_buffer);
__declspec(dllexport) bool should_close(CudaRenderer* renderer);
__declspec(dllexport) void get_window_size(CudaRenderer* renderer, int* width, int* height);
__declspec(dllexport) void get_mouse_info(CudaRenderer* renderer, MouseInfo* info);

// Nuevas funciones para dibujo
__declspec(dllexport) void begin_lines(CudaRenderer* renderer);
__declspec(dllexport) void draw_line(CudaRenderer* renderer, float x1, float y1, float x2, float y2, 
                                   unsigned char r, unsigned char g, unsigned char b, unsigned char a);
__declspec(dllexport) void end_lines(CudaRenderer* renderer);

#ifdef __cplusplus
}
#endif