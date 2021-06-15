#   This file merges all labels to generate final_labels.txt
#   and rename all training files

import os

FILE_NAME_1 = ["1-10000.txt", "10001_20000and30001_40000.txt", "20001_30000.txt", 
               "40001_50000.txt", "50001_60000.txt", "60000.txt"]
FILE_NAME_2 = ["0-170.txt", "170-340.txt", "341_510.txt", "511-680.txt",
               "681-850.txt", "851-995.txt"]

FINAL_LABELS = "final_labels.txt"

def getNum(line):
    return int(line.strip().split('_')[0])

def collect_labels():
    labels = dict()
    for file_name in FILE_NAME_1:
        print(file_name)
        with open(file_name, encoding="utf-8") as file:
            for line in file:
                num = getNum(line)
                labels[num] = line.strip()
    for file_name in FILE_NAME_2:
        print(file_name)
        with open(file_name, encoding="utf-8") as file:
            for line in file:
                num = getNum(line)
                labels[num] = line.strip()

    label_list = list(labels.values())
    label_list.sort(key=lambda str: getNum(str))
    with open(FINAL_LABELS, "w", encoding="utf-8") as f:
        for label in label_list:
            f.write(label + '\n')

def rename():
    labels = dict()
    with open(FINAL_LABELS, encoding="utf-8") as f:
        for line in f:
            num = getNum(line)
            labels[num] = line.strip()

    count = 0
    cwd = os.getcwd()
    path = os.path.join(cwd, 'train')
    for file_name in os.listdir(path):
        abs_file_path = os.path.join(path, file_name)
        num = getNum(file_name)
        new_file_name = labels.get(num, None)
        if f is not None and new_file_name != file_name:
            count += 1
            new_abs_file_path = os.path.join(path, new_file_name)
            os.rename(abs_file_path, new_abs_file_path)
    print(f"processed {count} files")

def main():
    # collect_labels()
    rename()

if __name__ == "__main__":
    main()