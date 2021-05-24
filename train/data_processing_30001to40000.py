# do not modify data_statistics_30001to40000.txt's line otherwise this program may not execute as intended
# back up your images indexed from 30001 to 40000 before execution
# you will need to make some choices to decide how to make your training data before acutal execution
# 
# suggestion: move all images indexed from 30001 to 40000, data_statistics_30001to40000.txt and this file
#             into a single folder before execution to avoid redundant index checks
# 
# read data_statistics_30001to40000.txt for the detailed explanation of each category
# 

import os
SUMMARY_FILE_NAME = "data_statistics_30001to40000.txt"
CATEGORY_NUMBER = 13
BASE = 30_000
LIMIT = 40_000

def process_index(list_like):
    return [int(index) + BASE for index in list_like]

def main():
    # main categories
    character_cut_into_another = dict()
    character_cut_into_component = set()
    multiple_characters = set()
    unidentifiable = set()
    empty = set()
    wrong_labels = dict()
    simplified_characters = dict()
    varied_character_forms = dict()
    
    # making choices about training data's labels
    simplified_flag = 0
    while(simplified_flag == 0):
        simplified_flag = input("對於簡體字的圖片，使用簡體字標籤(輸入1)還是使用繁體字標籤(輸入2)? ")
        if not (simplified_flag == '1' or simplified_flag == '2'):
            print("無效的輸入，請輸入1或2")
            simplified_flag = 0
        else:
            simplified_flag = int(simplified_flag)
    
    multiple_char_flag = 0
    while(multiple_char_flag == 0):
        multiple_char_flag = input("對於有多個字的圖片，使用isnull作為標籤(輸入1)還是使用原本的標籤(輸入2)? 使用原始的標籤可能會有該標籤不在圖裡面的錯誤情況: ")
        if not (multiple_char_flag == '1' or multiple_char_flag == '2'):
            print("無效的輸入，請輸入1或2")
            multiple_char_flag = 0
        else:
            multiple_char_flag = int(multiple_char_flag)

    empty_flag = 0
    while(empty_flag == 0):
        empty_flag = input("對於空的圖片，使用isnull標籤(輸入1)還是直接刪掉(不進垃圾桶)(輸入2)? ")
        if not (empty_flag == '1' or empty_flag == '2'):
            print("無效的輸入，請輸入1或2")
            empty_flag = 0
        else:
            empty_flag = int(empty_flag)

    # read config
    with open(SUMMARY_FILE_NAME, encoding="utf-8") as file:
        for i, line in enumerate(file):
            if not line.startswith('#'):
                line_list = [element.strip() for element in line.split(',')]
            if i in [11, 30, 37, 43]:
                tmp = process_index(line_list)
            elif i == 12:
                character_cut_into_another = {index:char for index, char in zip(tmp, line_list)}
            elif i == 15:
                character_cut_into_component = set(process_index(line_list))
            elif i == 18: # multiple char
                multiple_characters = set(process_index(line_list))
            elif i == 21: # bad seg that makes it unidentifiable
                unidentifiable = set(process_index(line_list))
            elif i == 24: # unidetifiable
                unidentifiable |= set(process_index(line_list))
            elif i == 29 and empty_flag == 1: # empty
                empty = set(process_index(line_list))
            elif i == 31:
                wrong_labels = {index:char for index, char in zip(tmp, line_list)}            
            elif i == 38 and simplified_flag == 1:
                simplified_characters = {index:char for index, char in zip(tmp, line_list)}
            elif i == 39 and simplified_flag == 2:
                simplified_characters = {index:char for index, char in zip(tmp, line_list)}
            elif i == 44:
                varied_character_forms = {index:char for index, char in zip(tmp, line_list)}
                
    # get all files in range for processing
    cwd = os.getcwd()
    files = []
    for f in os.listdir(cwd):
        if os.path.isfile(os.path.join(cwd, f)) and \
           f.endswith('.jpg') and \
           BASE < int(f.split('_')[0]) <= LIMIT:
           files.append(f)
                
    # start preprocessing
    processed_file_num = 0
    for f in files:
        new_name = None
        new_char = None
        
        original_f = os.path.join(cwd, f)
        
        index, char, jpg = f.replace('.', '_').split('_')
        index_num = int(index)
        
        new_char = character_cut_into_another.get(index_num, None)
        if new_char != None:
            new_name = index + '_' + new_char + '.jpg'
            
        if index_num in character_cut_into_component or \
            index_num in unidentifiable or \
            (multiple_char_flag == 1 and index_num in multiple_characters ) or \
            (empty_flag == 1 and index_num in empty):
            new_name = index + '_isnull.jpg'
            
        new_char = simplified_characters.get(index_num, None)
        if new_char != None:
            new_name = index + '_' + new_char + '.jpg'
            
        new_char = varied_character_forms.get(index_num, None)
        if new_char != None:
            new_name = index + '_' + new_char + '.jpg'
            
        new_char = wrong_labels.get(index_num, None)
        if new_char != None:
            new_name = index + '_' + new_char + '.jpg'

        if empty_flag == 2 and index_num in empty:
            os.remove(original_f)
            
        if new_name != None:
            processed_file_num += 1
            new_f = os.path.join(cwd, new_name)
            os.rename(original_f, new_f) # use this line if you want to rename file names
            # print(new_f) # use this line if you want a list of changed files
            
    print(f"{processed_file_num} files have been processed!")
    print("Remember to manually rotate images with these indices: 1595,3933,6261,7243,8642.")
            
if __name__ == "__main__":
    main()