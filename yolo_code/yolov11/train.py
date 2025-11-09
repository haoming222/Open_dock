from ultralytics import YOLO

# 加载模型
# model = YOLO("yolov8n.yaml")  # 从头开始构建新模型
model = YOLO("./weights/yolo11l.pt")  # 加载预训练模型（建议用于训练）
path = "./data/port.yaml"
# 使用模型
train_results = model.train(
    data=path,  # path to dataset YAML
    epochs=200,  # number of training epochs
    # imgsz=960,  # training image size
    batch=16,
    device=0,  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
    workers=0,
    name='grid500dataset_yolov11_200epo',
)
