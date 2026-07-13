#include "libdet.h"
#include <opencv2/opencv.hpp>
#include <cstring>
#include <cstdio>

static const char* class_names[] = {
    "pedestrian", "people", "bicycle", "car", "van", "truck",
    "tricycle", "awning-tricycle", "bus", "motor", "background"
};

int main(int argc, char *argv[]) {
    if (argc < 3) { 
        printf("Usage: %s <model.axmodel> <image.jpg> [threshold]\n", argv[0]);
        printf("  VisDrone YOLO11s Object Detection on AX650\n");
        return 1; 
    }
    const char *model_path = argv[1], *image_path = argv[2];
    float threshold = argc > 3 ? atof(argv[3]) : 0.25f;
    
    ax_devices_t ax_devices; memset(&ax_devices, 0, sizeof(ax_devices_t));
    if (ax_dev_enum_devices(&ax_devices) != 0) { printf("enum devices failed\n"); return -1; }
    if (ax_devices.host.available) ax_dev_sys_init(host_device, -1);
    if (!ax_devices.host.available) { printf("no AX device found\n"); return -1; }
    
    ax_det_init_t init_info; memset(&init_info, 0, sizeof(init_info));
    init_info.dev_type = host_device;
    init_info.model_type = ax_det_model_type_yolo11;
    sprintf(init_info.model_path, "%s", model_path);
    init_info.num_classes = 11;
    init_info.threshold = threshold;
    // Normalize uint8 BGR [0,255] to float [0,1] via 1/255
    init_info.std[0] = 1.0f/255.0f; init_info.std[1] = 1.0f/255.0f; init_info.std[2] = 1.0f/255.0f;
    
    ax_det_handle_t handle;
    if (ax_det_init(&init_info, &handle) != 0) { printf("model init failed\n"); return -1; }
    
    cv::Mat src = cv::imread(image_path);
    if (src.empty()) { printf("cannot read image: %s\n", image_path); return -1; }
    cv::resize(src, src, cv::Size(640, 640));
    
    ax_det_img_t img = {src.cols, src.rows, src.channels(), (int)src.step, src.data};
    ax_det_result_t result; memset(&result, 0, sizeof(result));
    if (ax_det(handle, &img, &result) != 0) { printf("detection failed\n"); return -1; }
    
    printf("Found %d objects:\n", result.num_objs);
    cv::Scalar colors[] = {
        cv::Scalar(0,255,0), cv::Scalar(255,0,0), cv::Scalar(0,0,255),
        cv::Scalar(255,255,0), cv::Scalar(255,0,255), cv::Scalar(0,255,255),
        cv::Scalar(128,255,0), cv::Scalar(255,128,0), cv::Scalar(0,128,255),
        cv::Scalar(128,0,255), cv::Scalar(0,0,0)
    };
    for (int i = 0; i < result.num_objs; i++) {
        auto &obj = result.objects[i];
        if (obj.score < threshold) continue;
        if (obj.label >= 11) continue;
        cv::Rect r(obj.box.x, obj.box.y, obj.box.w, obj.box.h);
        if (r.width <= 0 || r.height <= 0) continue;
        if (r.x + r.width > 640) r.width = 640 - r.x;
        if (r.y + r.height > 640) r.height = 640 - r.y;
        cv::rectangle(src, r, colors[obj.label % 10], 2);
        char buf[128]; 
        snprintf(buf, sizeof(buf), "%s %.2f", class_names[obj.label], obj.score);
        cv::putText(src, buf, cv::Point(obj.box.x, obj.box.y-5),
                    cv::FONT_HERSHEY_SIMPLEX, 0.4, colors[obj.label % 10], 1);
        printf("  [%d] %s %.3f [%d,%d,%d,%d]\n", 
               i, class_names[obj.label], obj.score,
               obj.box.x, obj.box.y, obj.box.w, obj.box.h);
    }
    cv::imwrite("result.jpg", src);
    printf("Result saved to result.jpg\n");
    ax_det_deinit(handle);
    ax_dev_sys_deinit(host_device, -1);
    return 0;
}
