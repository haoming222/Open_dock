

import os
import numpy as np
from collections import defaultdict


def load_labels(file_path):
    """加载标签文件"""
    labels = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cls = int(parts[0])  # 类别
            bbox = list(map(float, parts[1:5]))  # 边界框 (x_center, y_center, width, height)
            conf = float(parts[5]) if len(parts) == 6 else None  # 置信度（仅用于检测结果）
            labels.append((cls, bbox, conf))
    return labels


def calculate_iou(box1, box2):
    """计算两个边界框的 IOU"""
    x1_min, y1_min = box1[0] - box1[2] / 2, box1[1] - box1[3] / 2
    x1_max, y1_max = box1[0] + box1[2] / 2, box1[1] + box1[3] / 2
    x2_min, y2_min = box2[0] - box2[2] / 2, box2[1] - box2[3] / 2
    x2_max, y2_max = box2[0] + box2[2] / 2, box2[1] + box2[3] / 2

    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)

    inter_area = max(0, inter_x_max - inter_x_min) * max(0, inter_y_max - inter_y_min)
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = area1 + area2 - inter_area

    return inter_area / union_area if union_area > 0 else 0


def evaluate_file(detection_file, ground_truth_file, iou_threshold=0.5):
    """评估单个文件，并返回每个类别的统计结果"""
    detection_labels = load_labels(detection_file)
    ground_truth_labels = load_labels(ground_truth_file)

    detection_labels = sorted(detection_labels, key=lambda x: x[2], reverse=True)
    per_class_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    used_gt = set()

    for det_cls, det_box, conf in detection_labels:
        matched = False
        for i, (gt_cls, gt_box, _) in enumerate(ground_truth_labels):
            if i in used_gt or det_cls != gt_cls:
                continue
            if calculate_iou(det_box, gt_box) >= iou_threshold:
                per_class_stats[det_cls]["tp"] += 1
                used_gt.add(i)
                matched = True
                break
        if not matched:
            per_class_stats[det_cls]["fp"] += 1

    # 计算未匹配的真值
    for i, (gt_cls, _, _) in enumerate(ground_truth_labels):
        if i not in used_gt:
            per_class_stats[gt_cls]["fn"] += 1

    return per_class_stats


def evaluate_multiple_files(detection_dir, ground_truth_dir, iou_threshold=0.5):
    """评估多个文件，并按类别计算统计指标"""
    all_class_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})

    # 遍历所有文件
    for filename in os.listdir(ground_truth_dir):
        ground_truth_file = os.path.join(ground_truth_dir, filename)
        detection_file = os.path.join(detection_dir, filename)
        if not os.path.exists(detection_file):
            print(f"Warning: Missing detection file for {filename}")
            continue
        if filename == "classes.txt":
            print(f"Warning: Missing detection file for {filename}")
            continue

        file_class_stats = evaluate_file(detection_file, ground_truth_file, iou_threshold)

        # 累加每个类别的统计数据
        for cls, stats in file_class_stats.items():
            all_class_stats[cls]["tp"] += stats["tp"]
            all_class_stats[cls]["fp"] += stats["fp"]
            all_class_stats[cls]["fn"] += stats["fn"]

    # 计算每个类别的 P、R、F1 和 AP
    per_class_results = {}
    total_tp, total_fp, total_fn = 0, 0, 0
    for cls, stats in all_class_stats.items():
        tp, fp, fn = stats["tp"], stats["fp"], stats["fn"]
        total_tp += tp
        total_fp += fp
        total_fn += fn
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        ap = precision  # 对于单一 IOU 阈值下，AP 等于 Precision
        per_class_results[cls] = {"precision": precision, "recall": recall, "f1_score": f1_score, "ap": ap}

    # 计算总体指标
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
    overall_f1_score = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (
            overall_precision + overall_recall) > 0 else 0
    overall_ap = np.mean([res["ap"] for res in per_class_results.values()]) if per_class_results else 0

    return per_class_results, overall_precision, overall_recall, overall_f1_score, overall_ap


iou_threshold = 0.5
# 500grid
# detection_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/yolov5_detect_labels_with_conf"
# filter_detection_byrelationrate10_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/all_relations_labels/0.1relation/labels_with_conf"
# filter_detection_byrelationrate30_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/all_relations_labels/0.3relation/labels_with_conf"
filter_detection_byrelationrate50_dir = "G:/data/500/all_model/train_1280size/yolov11/not_buffer/get_filter_by_only_fd_lz_labels/labels_with_conf"
# filter_detection_byrelationrate70_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/all_relations_labels/0.7relation/labels_with_conf"
# filter_detection_byrelationrate90_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/all_relations_labels/0.9relation/labels_with_conf"
#
# filter_detection_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/filter_relation_0.5_detectby2880_labels_with_conf"
# ground_truth_dir = "G:/data/500/detect/not_buffer/test_dataset_without_bg/truth/truth_labels"

detection_dir = "G:/data/500/all_model/train_1280size/yolov11/not_buffer/detect_img/label_with_conf"
ground_truth_dir = "G:/data/500/all_model/truth/truth_labels"
per_class_results, overall_precision, overall_recall, overall_f1_score, overall_ap = evaluate_multiple_files(
    detection_dir, ground_truth_dir, iou_threshold)

# 打印每个类别的指标
print("Per-Class Evaluation Metrics (IOU=0.5):")
for cls, metrics in sorted(per_class_results.items()):
    print(f"Class {cls}: Precision={metrics['precision']:.4f}, Recall={metrics['recall']:.4f}, "
          f"F1-Score={metrics['f1_score']:.4f}, AP={metrics['ap']:.4f}")

# 打印总体指标
print("Overall Evaluation Metrics (IOU=0.5):")
print(f"Precision={overall_precision:.4f}, Recall={overall_recall:.4f}, "
      f"F1-Score={overall_f1_score:.4f}, mAP@0.5={overall_ap:.4f}")



print("\n\n\nafter_filter_by_relaiton_rate_0.5----------------------------------------------------------------------------after_filter_by_relaiton_rate_0.5")
per_class_results, overall_precision, overall_recall, overall_f1_score, overall_ap = evaluate_multiple_files(
    filter_detection_byrelationrate50_dir, ground_truth_dir, iou_threshold)

# 打印每个类别的指标
print("Per-Class Evaluation Metrics (IOU=0.5):")
for cls, metrics in sorted(per_class_results.items()):
    print(f"Class {cls}: Precision={metrics['precision']:.4f}, Recall={metrics['recall']:.4f}, "
          f"F1-Score={metrics['f1_score']:.4f}, AP={metrics['ap']:.4f}")

# 打印总体指标
print("Overall Evaluation Metrics (IOU=0.5):")
print(f"Precision={overall_precision:.4f}, Recall={overall_recall:.4f}, "
      f"F1-Score={overall_f1_score:.4f}, mAP@0.5={overall_ap:.4f}")
