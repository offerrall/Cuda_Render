#pragma once

#include <GL/glew.h>
#include <cuda_runtime.h>

#ifdef __cplusplus
extern "C" {
#endif

struct CudaRenderer;

struct MouseInfo {
    int x;
    int y;
    bool left_button;
    bool right_button;
    bool middle_button;
};

__declspec(dllexport) CudaRenderer* create_renderer(const char* title, int width, int height);
__declspec(dllexport) void destroy_renderer(CudaRenderer* renderer);
__declspec(dllexport) void begin_frame(CudaRenderer* renderer);
__declspec(dllexport) void end_frame(CudaRenderer* renderer);
__declspec(dllexport) void display_buffer(CudaRenderer* renderer, uchar4* cuda_buffer);
__declspec(dllexport) bool should_close(CudaRenderer* renderer);
__declspec(dllexport) void get_window_size(CudaRenderer* renderer, int* width, int* height);
__declspec(dllexport) void get_mouse_info(CudaRenderer* renderer, MouseInfo* info);


#ifdef __cplusplus
}
#endif