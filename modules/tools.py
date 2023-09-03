import os
import pickle

put_path = './temp/'

def rm(path):
    if not os.path.exists(path):
        return False
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            rm(file_path)
        else:
            os.remove(file_path)
    os.rmdir(path)

def download_attachment(login, filename, data_to_save, selected_mailbox, message_id):
    mkdir(put_path)
    path = os.path.join(put_path, login)
    mkdir(path)
    path = os.path.join(path, selected_mailbox)
    mkdir(path)
    path = os.path.join(path, str(message_id))
    mkdir(path)
    path = os.path.join(path, "attachments")
    mkdir(path)
    path = os.path.join(path, "raw")
    mkdir(path)
    path = os.path.join(path, filename)
    if not os.path.exists(path):
        fp = open(path, 'wb')
        fp.write(data_to_save)
        fp.close()

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)

# not working
def find_vector(old_data: dict, data: dict, scale: int):
    # 0: top-left corner (x, y)
    # 1: bottom-right corner (x, y)
    # 2: color
    # 3: thickness
    r_key = 'rectangles'
    t_key = 'text'
    scale = 1
    for index, part in enumerate(data[r_key]):
        for old_part in old_data[r_key]:
            x = part[0][0]
            x1 = part[1][0]
            old_x = old_part[0][0]
            old_x1 = old_part[1][0]
            y = part[0][1]
            y1 = part[1][1]
            old_y = old_part[0][1]
            old_y1 = old_part[1][1]
            if abs(x - old_x) < 50 and abs(y - old_y) < 50:
                x_vector = (x-x1) - (old_x-old_x1)
                y_vector = (y-y1) - (old_y-old_y1)
                x_vector = int(x_vector / scale)
                y_vector = int(y_vector / scale)
                x = part[0][0] + x_vector
                y = part[0][1] + y_vector
                x1 = part[1][0] + x_vector
                y1 = part[1][1] + y_vector
                data[r_key][index] = ((x, y),
                                      (x1, y1),
                                      part[2],
                                      part[3])
                break
    return data

def define_filetype(filename):
    filetype_extension = {"image": ["png", "jpg", "jpeg"],
                          "video": ["mp4", "avi"],
                          "txt": "txt",
                          "pdf": "pdf",
                          "word": "word"}

    file_extension = filename.split('.')[-1]

    for filetype, extension in filetype_extension.items():
        if file_extension in extension:
            return filetype

    return "unknown"

def create_result_folder(filename, processed_folder_path):
    # no_ex_filename = "".join(filename.split('.')[:-1])
    # process_result_folder_path = os.path.join(processed_folder_path, no_ex_filename)
    process_result_folder_path = os.path.join(processed_folder_path, filename)
    mkdir(process_result_folder_path)
    return process_result_folder_path


def define_filetype_by_bites(path_to_read):
    return False, None


def remove_selected_mailbox(login, selected_mailbox):
    path = os.path.join(put_path, login)
    path = os.path.join(path, selected_mailbox)
    rm(path)

def save_in_bites(data_to_save, path):
    with open(path, 'wb') as f:
        pickle.dump(data_to_save, f)

def load_from_bites(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def save_text(text, path):
    with open(path, 'w') as f:
        f.write(text)

def load_text(path):
    with open(path, 'r') as f:
        return f.read()
