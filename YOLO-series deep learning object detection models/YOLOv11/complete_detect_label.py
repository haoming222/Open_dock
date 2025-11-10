import os

# 定义两个文件夹路径
truth_label = "G:/data/500/detect/not_buffer/test_dataset_without_bg/truth/truth_labels"  # 替换为第一个文件夹路径
lack_label = "G:/data/500/all_model/yolov11/not_buffer/detect_img/labels"  # 替换为第二个文件夹路径

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


