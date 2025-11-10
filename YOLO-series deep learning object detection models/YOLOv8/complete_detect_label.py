import os

# 定义两个文件夹路径
truth_label = "G:/data/500/detect/not_buffer/test_dataset_without_bg/truth/truth_labels"  # 替换为第一个文件夹路径
lack_label = "G:/data/500/all_model/yolov8/not_buffer/detect_img/labels"  # 替换为第二个文件夹路径

# 获取两个文件夹中的文件名列表（仅限 .txt 文件）
txt_files_folder1 = {f for f in os.listdir(truth_label) if f.endswith('.txt')}
txt_files_folder2 = {f for f in os.listdir(lack_label) if f.endswith('.txt')}

# 找到 folder1 中存在但 folder2 中不存在的文件
missing_files = txt_files_folder1 - txt_files_folder2

# 在 folder2 中创建这些缺失的空 txt 文件
for file in missing_files:
    empty_file_path = os.path.join(lack_label, file)
    with open(empty_file_path, 'w') as f:  # 创建空文件
        pass

print(f"已在 {lack_label} 中创建 {len(missing_files)} 个空的 txt 文件。")


# D:\study\yolov5_study\yolov8_python\python.exe D:/study/yolov5_study/yolov8/test.py
# Warning: Missing detection file for 1_10038.txt
# Warning: Missing detection file for 1_1290.txt
# Warning: Missing detection file for 1_2577.txt
# Warning: Missing detection file for 1_2808.txt
# Warning: Missing detection file for 1_2863.txt
# Warning: Missing detection file for 1_3018.txt
# Warning: Missing detection file for 1_3037.txt
# Warning: Missing detection file for 1_3801.txt
# Warning: Missing detection file for 1_4006.txt
# Warning: Missing detection file for 1_4034.txt
# Warning: Missing detection file for 1_4370.txt
# Warning: Missing detection file for 1_4406.txt
# Warning: Missing detection file for 1_5427.txt
# Warning: Missing detection file for 1_5646.txt
# Warning: Missing detection file for 1_5989.txt
# Warning: Missing detection file for 1_6072.txt
# Warning: Missing detection file for 1_6088.txt
# Warning: Missing detection file for 1_6630.txt
# Warning: Missing detection file for 1_6686.txt
# Warning: Missing detection file for 1_6796.txt
# Warning: Missing detection file for 1_711.txt
# Warning: Missing detection file for 1_7514.txt
# Warning: Missing detection file for 1_7758.txt
# Warning: Missing detection file for 1_9784.txt
# Warning: Missing detection file for 1_9799.txt
# Warning: Missing detection file for 2_1504.txt
# Warning: Missing detection file for 2_1862.txt
# Warning: Missing detection file for 2_3594.txt
# Warning: Missing detection file for 2_3816.txt
# Warning: Missing detection file for 2_4159.txt
# Warning: Missing detection file for 2_426.txt
# Warning: Missing detection file for 2_4477.txt
# Warning: Missing detection file for 2_4792.txt
# Warning: Missing detection file for 2_5501.txt
# Warning: Missing detection file for 2_5725.txt
# Warning: Missing detection file for 2_6114.txt
# Warning: Missing detection file for 3_1075.txt
# Warning: Missing detection file for 3_3542.txt
# Warning: Missing detection file for 3_3865.txt
# Warning: Missing detection file for 3_388.txt
# Warning: Missing detection file for 3_4780.txt
# Warning: Missing detection file for 3_4877.txt
# Warning: Missing detection file for 3_4918.txt
# Warning: Missing detection file for 3_565.txt
# Warning: Missing detection file for 3_699.txt
# Warning: Missing detection file for 3_719.txt
# Warning: Missing detection file for 4_2849.txt
# Warning: Missing detection file for 4_3197.txt
# Warning: Missing detection file for 4_3553.txt
# Warning: Missing detection file for 4_36.txt
# Warning: Missing detection file for 4_533.txt
# Warning: Missing detection file for 5_1425.txt
# Warning: Missing detection file for 5_1612.txt
# Warning: Missing detection file for 5_1963.txt
# Warning: Missing detection file for 5_1975.txt
# Warning: Missing detection file for 5_24.txt
# Warning: Missing detection file for 5_3450.txt
# Warning: Missing detection file for 5_3761.txt
# Warning: Missing detection file for 5_4283.txt
# Warning: Missing detection file for 5_4289.txt
# Warning: Missing detection file for 5_4343.txt
# Warning: Missing detection file for 5_4469.txt
# Warning: Missing detection file for 5_980.txt
# Warning: Missing detection file for 6_1552.txt
# Warning: Missing detection file for 6_2550.txt
# Warning: Missing detection file for 6_2964.txt
# Warning: Missing detection file for 6_3207.txt
# Warning: Missing detection file for 6_3557.txt
# Warning: Missing detection file for 6_3682.txt
# Warning: Missing detection file for classes.txt
# Per-Class Evaluation Metrics (IOU=0.6):
# Class 0: Precision=0.8099, Recall=0.8333, F1-Score=0.8214, AP=0.8099
# Class 1: Precision=0.8227, Recall=0.8844, F1-Score=0.8524, AP=0.8227
# Overall Evaluation Metrics (IOU=0.6):
# Precision=0.8189, Recall=0.8690, F1-Score=0.8432, mAP@0.5=0.8163
#
# Process finished with exit code 0
