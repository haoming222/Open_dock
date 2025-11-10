from ultralytics import YOLO
import os
# 读取模型，这里传入训练好的模型
model = YOLO('./runs/detect/grid500dataset_yolov8_1280size_200epo/weights/best.pt')

# 模型预测，save=True 的时候表示直接保存yolov8的预测结果
# metrics = model.predict(source="G:/data/500/all_model/random_detect_img/images",save=True,save_txt=True,save_conf=True,imgsz=800)
metrics = model.predict(source="G:/data/500/all_model/train_1280size/yolov8/buffer_500/6/test_dataset/img",
                        save=True,save_txt=True,save_conf=True,imgsz=2880)
save_dir = "G:/data/500/all_model/train_1280size/yolov8/buffer_500/6/detect_result_h_w"
os.makedirs(save_dir, exist_ok=True)

# 自定义处理预测结果并保存
for i, m in enumerate(metrics, start=1):
    # 获取图片文件名
    image_name = os.path.basename(m.path).split('.')[0]
    save_path = os.path.join(save_dir, f"{image_name}.txt")

    # 打开文件保存每个目标框的信息
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"检测结果：图片 {image_name}\n")

        # 获取每个预测结果的 boxes
        boxes = m.boxes
        for j, box in enumerate(boxes, start=1):
            # 提取 box 的位置、类别和置信度
            xyxy = box.xyxy[0].cpu().numpy()  # 转换为 [x1, y1, x2, y2]
            confidence = box.conf[0].item()
            cls = int(box.cls[0].item())

            # 计算宽、高和中心点
            x1, y1, x2, y2 = xyxy
            width = x2 - x1
            height = y2 - y1
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            # 写入每个目标框的信息
            f.write(f"第{j}个框信息：\n")
            f.write(f"左上点的坐标为：({x1:.1f},{y1:.1f})，右上点的坐标为({x2:.1f},{y1:.1f})\n")
            f.write(f"左下点的坐标为：({x1:.1f},{y2:.1f})，右下点的坐标为({x2:.1f},{y2:.1f})\n")
            f.write(f"中心点的坐标为：({center_x:.1f},{center_y:.1f})，类别id为{cls}\n")
            f.write(f"高为{height:.1f},宽为{width:.1f}，置信度为{confidence:.5f}\n\n")