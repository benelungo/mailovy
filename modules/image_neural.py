import os
import time

import cv2
import numpy as np

image_net = cv2.dnn.readNetFromTensorflow(r"data\models\saved_model.pb",
                                          r"data\models\saved_model.pbtxt")


class ImageNeural:
    def __init__(self):
        self.class_names = [{"supercategory": "person", "id": 1, "name": "person"},
                       {"supercategory": "vehicle", "id": 2, "name": "bicycle"},
                       {"supercategory": "vehicle", "id": 3, "name": "car"},
                       {"supercategory": "vehicle", "id": 4, "name": "motorcycle"},
                       {"supercategory": "vehicle", "id": 5, "name": "airplane"},
                       {"supercategory": "vehicle", "id": 6, "name": "bus"},
                       {"supercategory": "vehicle", "id": 7, "name": "train"},
                       {"supercategory": "vehicle", "id": 8, "name": "truck"},
                       {"supercategory": "vehicle", "id": 9, "name": "boat"},
                       {"supercategory": "outdoor", "id": 10, "name": "traffic light"},
                       {"supercategory": "outdoor", "id": 11, "name": "fire hydrant"},
                       {"supercategory": "outdoor", "id": 12, "name": "street sign"},
                       {"supercategory": "outdoor", "id": 13, "name": "stop sign"},
                       {"supercategory": "outdoor", "id": 14, "name": "parking meter"},
                       {"supercategory": "outdoor", "id": 15, "name": "bench"},
                       {"supercategory": "animal", "id": 16, "name": "bird"},
                       {"supercategory": "animal", "id": 17, "name": "cat"},
                       {"supercategory": "animal", "id": 18, "name": "dog"},
                       {"supercategory": "animal", "id": 19, "name": "horse"},
                       {"supercategory": "animal", "id": 20, "name": "sheep"},
                       {"supercategory": "animal", "id": 21, "name": "cow"},
                       {"supercategory": "animal", "id": 22, "name": "elephant"},
                       {"supercategory": "animal", "id": 23, "name": "bear"},
                       {"supercategory": "animal", "id": 24, "name": "zebra"},
                       {"supercategory": "animal", "id": 25, "name": "giraffe"},
                       {"supercategory": "accessory", "id": 26, "name": "hat"},
                       {"supercategory": "accessory", "id": 27, "name": "backpack"},
                       {"supercategory": "accessory", "id": 28, "name": "umbrella"},
                       {"supercategory": "accessory", "id": 29, "name": "shoe"},
                       {"supercategory": "accessory", "id": 30, "name": "eye glasses"},
                       {"supercategory": "accessory", "id": 31, "name": "handbag"},
                       {"supercategory": "accessory", "id": 32, "name": "tie"},
                       {"supercategory": "accessory", "id": 33, "name": "suitcase"},
                       {"supercategory": "sports", "id": 34, "name": "frisbee"},
                       {"supercategory": "sports", "id": 35, "name": "skis"},
                       {"supercategory": "sports", "id": 36, "name": "snowboard"},
                       {"supercategory": "sports", "id": 37, "name": "sports ball"},
                       {"supercategory": "sports", "id": 38, "name": "kite"},
                       {"supercategory": "sports", "id": 39, "name": "baseball bat"},
                       {"supercategory": "sports", "id": 40, "name": "baseball glove"},
                       {"supercategory": "sports", "id": 41, "name": "skateboard"},
                       {"supercategory": "sports", "id": 42, "name": "surfboard"},
                       {"supercategory": "sports", "id": 43, "name": "tennis racket"},
                       {"supercategory": "kitchen", "id": 44, "name": "bottle"},
                       {"supercategory": "kitchen", "id": 45, "name": "plate"},
                       {"supercategory": "kitchen", "id": 46, "name": "wine glass"},
                       {"supercategory": "kitchen", "id": 47, "name": "cup"},
                       {"supercategory": "kitchen", "id": 48, "name": "fork"},
                       {"supercategory": "kitchen", "id": 49, "name": "knife"},
                       {"supercategory": "kitchen", "id": 50, "name": "spoon"},
                       {"supercategory": "kitchen", "id": 51, "name": "bowl"},
                       {"supercategory": "food", "id": 52, "name": "banana"},
                       {"supercategory": "food", "id": 53, "name": "apple"},
                       {"supercategory": "food", "id": 54, "name": "sandwich"},
                       {"supercategory": "food", "id": 55, "name": "orange"},
                       {"supercategory": "food", "id": 56, "name": "broccoli"},
                       {"supercategory": "food", "id": 57, "name": "carrot"},
                       {"supercategory": "food", "id": 58, "name": "hot dog"},
                       {"supercategory": "food", "id": 59, "name": "pizza"},
                       {"supercategory": "food", "id": 60, "name": "donut"},
                       {"supercategory": "food", "id": 61, "name": "cake"},
                       {"supercategory": "furniture", "id": 62, "name": "chair"},
                       {"supercategory": "furniture", "id": 63, "name": "couch"},
                       {"supercategory": "furniture", "id": 64, "name": "potted plant"},
                       {"supercategory": "furniture", "id": 65, "name": "bed"},
                       {"supercategory": "furniture", "id": 66, "name": "mirror"},
                       {"supercategory": "furniture", "id": 67, "name": "dining table"},
                       {"supercategory": "furniture", "id": 68, "name": "window"},
                       {"supercategory": "furniture", "id": 69, "name": "desk"},
                       {"supercategory": "furniture", "id": 70, "name": "toilet"},
                       {"supercategory": "furniture", "id": 71, "name": "door"},
                       {"supercategory": "electronic", "id": 72, "name": "tv"},
                       {"supercategory": "electronic", "id": 73, "name": "laptop"},
                       {"supercategory": "electronic", "id": 74, "name": "mouse"},
                       {"supercategory": "electronic", "id": 75, "name": "remote"},
                       {"supercategory": "electronic", "id": 76, "name": "keyboard"},
                       {"supercategory": "electronic", "id": 77, "name": "cell phone"},
                       {"supercategory": "appliance", "id": 78, "name": "microwave"},
                       {"supercategory": "appliance", "id": 79, "name": "oven"},
                       {"supercategory": "appliance", "id": 80, "name": "toaster"},
                       {"supercategory": "appliance", "id": 81, "name": "sink"},
                       {"supercategory": "appliance", "id": 82, "name": "refrigerator"},
                       {"supercategory": "appliance", "id": 83, "name": "blender"},
                       {"supercategory": "indoor", "id": 84, "name": "book"},
                       {"supercategory": "indoor", "id": 85, "name": "clock"},
                       {"supercategory": "indoor", "id": 86, "name": "vase"},
                       {"supercategory": "indoor", "id": 87, "name": "scissors"},
                       {"supercategory": "indoor", "id": 88, "name": "teddy bear"},
                       {"supercategory": "indoor", "id": 89, "name": "hair drier"},
                       {"supercategory": "indoor", "id": 90, "name": "toothbrush"},
                       {"supercategory": "indoor", "id": 91, "name": "hair brush"}]
        self.colors = np.random.randint(100, 240, (100, 3))
        self.net = image_net

    def detect(self, img):
        height, width, depth = img.shape

        blob = cv2.dnn.blobFromImage(img, swapRB=True)
        self.net.setInput(blob)

        boxes = self.net.forward("detection_out_final")
        detection_count = boxes.shape[2]
        detect_info = {"rectangles": [], "text": []}

        for i in range(detection_count):
            box = boxes[0, 0, i]
            score = box[2]
            if score < 0.5:
                continue

            class_id = box[1]
            color = self.colors[int(class_id)]
            x = int(box[3] * width)
            y = int(box[4] * height)
            x2 = int(box[5] * width)
            y2 = int(box[6] * height)

            name = self.class_names[int(class_id)]['name']
            text = name + ' (' + str(np.round(score, 2)) + ')'
            detect_info["rectangles"].append(((x, y), (x2, y2), (int(color[0]), int(color[1]), int(color[2])), 2))  # cv2.rectangle(img, (x, y), (x2, y2), (int(color[0]), int(color[1]), int(color[2])), 3)
            detect_info["text"].append((text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(color[0]), int(color[1]), int(color[2])), 1))  # cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(color[0]), int(color[1]), int(color[2])), 2)
        return detect_info  #img

    def segment(self, img):
        height, width, depth = img.shape
        black_image = np.zeros((height, width, 3))

        blob = cv2.dnn.blobFromImage(img, swapRB=True)
        self.net.setInput(blob)

        boxes, masks = self.net.forward(["detection_out_final", "detection_masks"])
        detection_count = boxes.shape[2]
        for i in range(detection_count):
            box = boxes[0, 0, i]
            score = box[2]
            if score < 0.5:
                continue

            class_id = box[1]
            color = self.colors[int(class_id)]
            x = int(box[3] * width)
            y = int(box[4] * height)
            x2 = int(box[5] * width)
            y2 = int(box[6] * height)
            roi = img[y: y2, x: x2]
            roi_height, roi_width, _ = roi.shape

            name = self.class_names[int(class_id)]['name']
            text = name + ' (' + str(np.round(score, 2)) + ')'
            mask = masks[i, int(class_id)]
            mask = cv2.resize(mask, (roi_width, roi_height))
            _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(color[0]), int(color[1]), int(color[2])), 2)

            contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        return img

    def segment_and_detect(self, img):
        height, width, depth = img.shape
        black_image = np.zeros((height, width, 3))

        blob = cv2.dnn.blobFromImage(img, swapRB=True)
        self.net.setInput(blob)

        boxes, masks = self.net.forward(["detection_out_final", "detection_masks"])
        detection_count = boxes.shape[2]
        for i in range(detection_count):
            box = boxes[0, 0, i]
            class_id = box[1]
            score = box[2]
            if score < 0.5:
                continue

            x = int(box[3] * width)
            y = int(box[4] * height)
            x2 = int(box[5] * width)
            y2 = int(box[6] * height)
            roi = black_image[y: y2, x: x2]
            roi_height, roi_width, _ = roi.shape

            name = self.class_names[int(class_id)]['name']
            text = name + ' (' + str(np.round(score, 2)) + ')'
            mask = masks[i, int(class_id)]
            mask = cv2.resize(mask, (roi_width, roi_height))
            _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
            cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 3)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            color = self.colors[int(class_id)]
            for cnt in contours:
                cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        return img, black_image
