import numpy as np
import cv2
import base64
import os
"""
This script converts into images test data recorded by server during competition rehearsal 
It also auto rename file names with image label after it's manually identified and put in labels.txt
"""

FILE_NAME = "temp_data/esun_post_data.json"
IMAGE_PATH = "temp_data/test_data"
LABEL_NAME = "labels.txt"

def base64_to_binary_for_cv2(image_64_encoded):
    """ Convert base64 to numpy.ndarray for cv2.

    @param:
        image_64_encode(str): image that encoded in base64 string format.
    @returns:
        image(numpy.ndarray): an image.
    """
    img_base64_binary = image_64_encoded.encode("utf-8")
    img_binary = base64.b64decode(img_base64_binary)
    image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
    return image

def code_to_img(input):
    """
    input is a collection of object in json format recorded by server
    """
    with open(input) as file:
        words = set()
        for line in file:
            l = line.strip()
            if l.startswith("\"image\""):
                words.add(l.split(':')[1].strip('" '))

    os.chdir(IMAGE_PATH)
    for i, word in enumerate(words):
        image = base64_to_binary_for_cv2(word)
        file_name = str(i) + '.jpg'
        cv2.imwrite(file_name, image)


def label_img(label_file):
    os.chdir(IMAGE_PATH)
    with open(label_file, encoding="utf-8") as file:
        index = 0
        composite_name = ''
        for line in file:
            for char in line:
                if char.isascii():
                    composite_name = composite_name + char
                elif composite_name != '':
                    if composite_name == 'isnull':
                        src = os.path.join(os.getcwd(), str(index) + '.jpg')
                        dst = os.path.join(os.getcwd(), str(index) +'_isnull.jpg')
                        os.rename(src, dst)
                        composite_name = ''
                        index += 1
                    elif len(composite_name) >= len('isnull'):
                        print("wrong label at", composite_name)
                        exit(0)
                else:
                    src = os.path.join(os.getcwd(), str(index) + '.jpg')
                    dst = os.path.join(os.getcwd(), str(index) + '_' + char + '.jpg')
                    os.rename(src, dst)
                    index += 1

def main():
    code_to_img(FILE_NAME)
    # label_img(LABEL_NAME) # call this function after image labels are manully identified and put in labels.txt

if __name__ == "__main__":
    main()   