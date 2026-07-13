#include "libdet.h"
#include <opencv2/opencv.hpp>
#include <cstring>
#include <cstdio>

int main(int argc, char *argv[])
{
    if (argc < 3) {
        printf("Usage: %s <model.axmodel> <image.jpg> [threshold]\n", argv[0]);
        return 1;
    }

    const char *model_path = argv[1];
    const char *image_path = argv[2];
    float threshold = argc > 3 ? atof(argv[3]) : 0.25f;

    // Enumerate devices
    ax_devices_t ax_devices;
    memset(&ax_devices, 0, sizeof(ax_devices_t));
    if (ax_dev_enum_devices(&ax_devices) != 0) {
        printf("enum devices failed\n");
        return -1;
    }

    if (ax_devices.host.available) {
        ax_dev_sys_init(host_device, -1);
    }
    if (ax_devices.devices.count > 0) {
        ax_dev_sys_init(axcl_device, 0);
    }

    if (!ax_devices.host.available && ax_devices.devices.count == 0) {
        printf("no device available\n");
        return -1;
    }

    // Init detector
    ax_det_init_t init_info;
    memset(&init_info, 0, sizeof(init_info));

    if (ax_devices.host.available) {
        init_info.dev_type = host_device;
    } else {
        init_info.dev_type = axcl_device;
        init_info.devid = 0;
    }

    init_info.model_type = ax_det_model_type_yolo11;
    sprintf(init_info.model_path, "%s", model_path);
    init_info.num_classes = 10;
    init_info.num_kpt = 0;
    init_info.threshold = threshold;

    ax_det_handle_t handle;
    if (ax_det_init(&init_info, &handle) != ax_det_errcode_success) {
        printf("ax_det_init failed\n");
        return -1;
    }

    // Load and preprocess image
    cv::Mat src = cv::imread(image_path);
    if (src.empty()) {
        printf("imread %s failed\n", image_path);
        return -1;
    }
    cv::resize(src, src, cv::Size(640, 640));
    cv::cvtColor(src, src, cv::COLOR_BGR2RGB);

    ax_det_img_t img;
    img.data = src.data;
    img.width = src.cols;
    img.height = src.rows;
    img.channels = src.channels();
    img.stride = src.step;

    // Detect
    ax_det_result_t result;
    memset(&result, 0, sizeof(result));
    if (ax_det(handle, &img, &result) != ax_det_errcode_success) {
        printf("ax_det failed\n");
        return -1;
    }

    printf("Found %d objects\n", result.num_objs);

    // Draw results
    cv::cvtColor(src, src, cv::COLOR_RGB2BGR);
    for (int i = 0; i < result.num_objs; i++) {
        ax_det_obj_t &obj = result.objects[i];
        if (obj.score < threshold) continue;

        cv::Rect rect(obj.box.x, obj.box.y, obj.box.w, obj.box.h);
        cv::rectangle(src, rect, cv::Scalar(0, 255, 0), 2);

        char label_info[128];
        sprintf(label_info, "%d %.2f", obj.label, obj.score);
        cv::putText(src, label_info, cv::Point(obj.box.x, obj.box.y + 25),
                    cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(0, 255, 0), 2);
        printf("  [%d] score=%.3f box=[%d,%d,%d,%d]\n",
               obj.label, obj.score, obj.box.x, obj.box.y, obj.box.w, obj.box.h);
    }

    cv::imwrite("result.jpg", src);
    printf("Result saved to result.jpg\n");

    ax_det_deinit(handle);

    if (ax_devices.host.available) {
        ax_dev_sys_deinit(host_device, -1);
    }
    if (ax_devices.devices.count > 0) {
        ax_dev_sys_deinit(axcl_device, 0);
    }

    return 0;
}
