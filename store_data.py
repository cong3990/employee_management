import json


def read_file(file):
    """Lấy dữ liệu từ file định dạng .json"""

    # Check if file is valid
    try:
        r_file = open(file, "r", encoding="utf-8")
        data = json.load(r_file)
        r_file.close()
        # Make sure output data is a list for later iteration
        if type(data) != type([]):
            data = [data]
        return data

    # Check input file name if file cannot be found
    except FileNotFoundError:
        print("Không thể tìm thấy file. Kiểm tra lại đường dẫn file và tên file.")


def write_file(file, data):
    """Viết dữ liệu vào file định dạng .json"""

    with open(file, "w", encoding="utf-8") as w_file:
        json.dump(data, w_file, ensure_ascii=False, indent=2)
