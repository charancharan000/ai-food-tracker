"""
Dataset Multi-Format Exporter
Converts internal FoodSample records to standard deep learning training formats:
COCO JSON, YOLO format (txt), and PyTorch classification CSV/manifests.
"""

import json
from typing import List, Dict, Any
from .schema import FoodSample

class DatasetExporter:
    @staticmethod
    def export_to_coco_format(samples: List[FoodSample]) -> Dict[str, Any]:
        """Exports food samples to standard MS-COCO JSON instance format."""
        images = []
        annotations = []
        categories = {}
        category_list = []
        cat_counter = 1
        ann_counter = 1

        for s in samples:
            images.append({
                "id": s.sample_id,
                "file_name": s.image_path,
                "width": s.image_width,
                "height": s.image_height,
                "meal_id": s.meal_id,
                "view_angle": s.view_angle,
                "plate_diameter_cm": s.reference_scale.plate_diameter_cm if s.reference_scale else 26.0
            })

            for item in s.food_items:
                if item.class_name not in categories:
                    categories[item.class_name] = cat_counter
                    category_list.append({"id": cat_counter, "name": item.class_name, "supercategory": "food"})
                    cat_counter += 1

                cat_id = categories[item.class_name]
                ymin = item.bbox.ymin * s.image_height
                xmin = item.bbox.xmin * s.image_width
                ymax = item.bbox.ymax * s.image_height
                xmax = item.bbox.xmax * s.image_width
                w = xmax - xmin
                h = ymax - ymin

                annotations.append({
                    "id": ann_counter,
                    "image_id": s.sample_id,
                    "category_id": cat_id,
                    "bbox": [round(xmin, 1), round(ymin, 1), round(w, 1), round(h, 1)],
                    "area": round(w * h, 1),
                    "segmentation": [sum(item.segmentation_polygon, [])] if item.segmentation_polygon else [],
                    "iscrowd": 0,
                    "actual_weight_grams": item.actual_weight_grams,
                    "portion_class": item.portion_class
                })
                ann_counter += 1

        return {
            "info": {
                "description": "NutriScan AI Food Vision & Instance Segmentation Dataset",
                "version": "2.0.0",
                "year": 2026
            },
            "images": images,
            "annotations": annotations,
            "categories": category_list
        }

    @staticmethod
    def export_to_yolo_lines(sample: FoodSample, class_to_id: Dict[str, int]) -> List[str]:
        """Converts bounding boxes into YOLO normalized [class_id, x_center, y_center, width, height] format."""
        lines = []
        for item in sample.food_items:
            cls_id = class_to_id.get(item.class_name, 0)
            x_center = (item.bbox.xmin + item.bbox.xmax) / 2.0
            y_center = (item.bbox.ymin + item.bbox.ymax) / 2.0
            w = item.bbox.xmax - item.bbox.xmin
            h = item.bbox.ymax - item.bbox.ymin
            lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")
        return lines
