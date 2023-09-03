import os.path
import cv2
from modules.image_neural import ImageNeural
from modules import image_neural, tools
import fitz
import io
from PIL import Image

from modules.text_neural import TextNeural, DatasetAgNews
dataset = DatasetAgNews()
text_neural = TextNeural(dataset)

def process_txt(raw_folder_path: str, processed_folder_path: str, filename: str):  # todo
    path_to_read = os.path.join(raw_folder_path, filename)
    path_to_save = os.path.join(processed_folder_path, filename)
    tools.mkdir(processed_folder_path)
    tools.mkdir(path_to_save)
    with open(path_to_read, "r") as f:
        to_predict = f.read()
    predict = text_neural.predict([to_predict])[0]
    text_to_save = []
    for pred in predict:
        text_to_save.append(str(pred[0]).capitalize() + " (" + str(round(float(pred[1]), 2)) + ")")
    text_to_save = ", ".join(text_to_save)
    tools.save_text(text_to_save, os.path.join(path_to_save, "analysis_result.txt"))
    return text_to_save

def process_image(raw_folder_path: str, processed_folder_path: str, filename: str):  # todo
    net = ImageNeural()
    path_to_read = os.path.join(raw_folder_path, filename)
    path_to_save_processed = os.path.join(processed_folder_path, filename)
    path_to_save_image = os.path.join(path_to_save_processed, "detected_" + filename)
    tools.mkdir(processed_folder_path)
    tools.mkdir(path_to_save_processed)
    img = cv2.imread(path_to_read)
    image_content = []

    detect_info = net.detect(img)
    for rectangle_info in detect_info["rectangles"]:
        cv2.rectangle(img, *rectangle_info)
    for text_info in detect_info["text"]:
        image_content.append(text_info[0].capitalize())
        cv2.putText(img, *text_info)

    cv2.imwrite(path_to_save_image, img)

    path_to_save_result = os.path.join(path_to_save_processed, "analysis_result.txt")

    if len(image_content) != 0:
        result = ", ".join(image_content)
        tools.save_text(result, path_to_save_result)
    else:
        result = "Content wasn't detected"
        tools.save_text(result, path_to_save_result)
    return result

def process_video(raw_folder_path: str, processed_folder_path: str, filename: str):  # todo
    net = ImageNeural()
    path_to_read = os.path.join(raw_folder_path, filename)
    path_to_save_processed = os.path.join(processed_folder_path, filename)
    path_to_save_video = os.path.join(path_to_save_processed, filename)
    tools.mkdir(path_to_save_processed)
    video = cv2.VideoCapture(path_to_read)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_size = (int(video.get(3)), int(video.get(4)))

    video_out = cv2.VideoWriter(path_to_save_video, -1, fps, video_size)

    detect_info = None
    detect_scale = 15
    resolution = 480
    scale_rate = resolution / video_size[1]
    detect_size = (int(video_size[0] * scale_rate), int(video_size[1] * scale_rate))
    success, frame = video.read()
    video_content = []
    i = 0
    while success:
        print("Frame: " + str(int(video.get(1))))
        frame = cv2.resize(frame, detect_size)
        if i % detect_scale == 0:
            detect_info = net.detect(frame)
        for rectangle_info in detect_info["rectangles"]:
            cv2.rectangle(frame, *rectangle_info)
        for text_info in detect_info["text"]:
            video_content.append(text_info[0].capitalize().split("(")[0])
            cv2.putText(frame, *text_info)
        frame = cv2.resize(frame, video_size)
        video_out.write(frame)
        success, frame = video.read()
        i += 1

    video_out.release()
    video.release()

    path_to_save_result = os.path.join(path_to_save_processed, "analysis_result.txt")

    if len(video_content) != 0:
        result = ", ".join(set(video_content))
        tools.save_text(result, path_to_save_result)
    else:
        result = "Content wasn't detected"
        tools.save_text(result, path_to_save_result)
    return result

def process_pdf(raw_folder_path: str, processed_folder_path: str, filename: str):  # todo
    tools.mkdir(processed_folder_path)
    return "PDF_TEST"


class FilesProcessor:
    @staticmethod
    def process_files(raw_folder_path, processed_folder_path, filenames, event, analise_list):
        for filename in filenames:
            filetype = tools.define_filetype(filename)
            path_to_save = os.path.join(processed_folder_path, filename)
            if "image" in filetype.lower():
                path_to_result = os.path.join(path_to_save, "analysis_result.txt")
                if not os.path.exists(path_to_result):
                    result = process_image(raw_folder_path, processed_folder_path, filename)
                else:
                    result = tools.load_text(path_to_result)
            elif "video" in filetype.lower():
                path_to_result = os.path.join(path_to_save, "analysis_result.txt")
                if not os.path.exists(path_to_result):
                    result = process_video(raw_folder_path, processed_folder_path, filename)
                else:
                    result = tools.load_text(path_to_result)
            elif "txt" in filetype.lower():
                path_to_result = os.path.join(path_to_save, "analysis_result.txt")
                if not os.path.exists(path_to_result):
                    result = process_txt(raw_folder_path, processed_folder_path, filename)
                else:
                    result = tools.load_text(path_to_result)
            elif "pdf" in filetype.lower():
                path_to_result = os.path.join(path_to_save, "analysis_result.txt")
                if not os.path.exists(path_to_result):
                    result = process_pdf(raw_folder_path, processed_folder_path, filename)
                else:
                    result = tools.load_text(path_to_result)
            else:
                result = f'Bad filetype "{filetype}"'
            analise_list.append(filename + " - " + result)
        event.set()
