#coding=utf-8
from argparse import ArgumentParser
import base64
import json
import datetime
import hashlib
import time
import cv2
from flask import Flask
from flask import request
from flask import jsonify
import numpy as np
import torch
import torchvision.transforms as transforms
from model import Classifier
from PIL import Image
import torch.nn as nn


app = Flask(__name__)

####### PUT YOUR INFORMATION HERE #######
CAPTAIN_EMAIL = 'mandychad12@gmail.com'          #
SALT = 'r09942162'                        #
#########################################

dict_ = ['宋', '名', '楊', '活', '杜', '輪', '緯', '詹', '小', '牙', '歐', '勤', '聖', '築', '代', '川', '臻', '地', '德', '連', '千', '海', '蓁', '限', '貨', '蕭', '鑽', '公', '林', '潔', '詮', '防', '葳', '化', '房', '涵', '園', '采', '亮', '漁', '米', '碩', '兆', '店', '利', '普', '證', '記', '鴻', '巨', '幼', '豪', '基', '宗', '元', '勳', '御', '薛', '皓', '佳', '兒', '好', '翁', '密', '山', '有', '蔣', '能', '京', '彩', '吉', '經', '瑋', '朱', '團', '藥', '專', '影', '江', '娟', '龍', '市', '晟', '整', '捷', '綠', '湯', '澤', '悅', '絲', '包', '煌', '竹', '道', '展', '通', '眾', '羅', '護', '聚', '五', '禎', '敬', '報', '柯', '婉', '清', '翰', '慶', '振', '劉', '先', '源', '佩', '生', '貞', '文', '羽', '樂', '大', '珮', '苑', '司', '宸', '進', '慧', '視', '紋', '皇', '貴', '秦', '良', '冠', '鎮', '製', '時', '位', '宜', '賜', '盟', '卿', '嘉', '銓', '爾', '福', '峰', '寧', '雲', '百', '事', '農', '梅', '丞', '日', '欽', '杰', '正', '新', '奕', '長', '祐', '鐵', '城', '計', '賴', '施', '師', '漢', '登', '自', '曹', '騰', '投', '芝', '盧', '郭', '力', '盈', '汽', '中', '義', '紅', '翊', '政', '用', '扶', '郎', '方', '內', '同', '材', '馮', '徐', '樹', '永', '社', '順', '珊', '曾', '慈', '謙', '憶', '帝', '紘', '戶', '黃', '原', '于', '陞', '妹', '姚', '榮', '復', '坊', '彭', '侯', '會', '勝', '琦', '昕', '顧', '凱', '音', '治', '純', '意', '倫', '玫', '台', '佑', '素', '謝', '花', '鋁', '寬', '療', '言', '術', '場', '年', '上', '毓', '刷', '雨', '昇', '益', '特', '產', '民', '之', '合', '職', '志', '堂', '屬', '孟', '泓', '萱', '瑩', '誠', '若', '傑', '綸', '忠', '紙', '春', '寓', '逸', '喬', '敏', '具', '堅', '芸', '麒', '哲', '顯', '營', '崇', '暉', '鋼', '消', '芷', '租', '統', '法', '麟', '廣', '問', '本', '賓', '總', '份', '餐', '君', '介', '璟', '策', '韻', '仲', '裝', '蕙', '育', '鄭', '祥', '醫', '儀', '森', '蓉', '勁', '亞', '善', '財', '工', '拓', '申', '欣', '藍', '武', '南', '務', '信', '食', '世', '明', '宏', '韋', '寶', '器', '洲', '沙', '趙', '仕', '氣', '權', '智', '庭', '奇', '造', '宣', '里', '尚', '潤', '險', '電', '開', '琴', '梁', '紹', '津', '告', '禾', '娥', '聲', '鈴', '立', '臺', '機', '曜', '瑞', '貿', '阿', '東', '典', '伍', '珠', '木', '券', '保', '局', '心', '航', '興', '重', '禮', '美', '安', '頂', '子', '科', '交', '愷', '翠', '協', '行', '企', '厚', '吟', '鈞', '鳳', '程', '王', '媛', '白', '浩', '霖', '思', '球', '貝', '光', '運', '錦', '菊', '卓', '竑', '塑', '樓', '平', '蘇', '冷', '隆', '池', '朝', '竣', '坤', '圓', '客', '風', '田', '械', '琇', '燕', '衛', '敦', '薇', '聯', '水', '艾', '呈', '鵬', '男', '偉', '游', '范', '不', '匠', '真', '吳', '沈', '鋐', '色', '燦', '古', '英', '教', '神', '物', '迪', '分', '網', '員', '琳', '潘', '祺', '鈺', '強', '致', '姿', '士', '閔', '賀', '峻', '許', '友', '昶', '愛', '高', '莉', '月', '宇', '孫', '鄧', '際', '周', '鼎', '廠', '蘭', '學', '研', '舜', '廷', '章', '和', '彥', '菱', '融', '雪', '駿', '舒', '巫', '蔡', '太', '診', '匯', '律', '博', '碧', '呂', '委', '聰', '理', '精', '震', '丁', '晴', '幸', '瑄', '輝', '品', '晶', '技', '婷', '灣', '柔', '超', '弘', '縣', '門', '堡', '景', '玉', '建', '彰', '銘', '承', '石', '詠', '泉', '李', '筱', '優', '澄', '堯', '家', '如', '室', '儒', '伶', '備', '揚', '北', '紀', '管', '加', '耀', '香', '鉅', '億', '區', '培', '屋', '茹', '盛', '勇', '應', '棋', '維', '銀', '股', '秋', '健', '動', '來', '瓊', '可', '鎧', '拉', '邱', '彬', '茂', '康', '萬', '菁', '調', '三', '成', '實', '胡', '任', '克', '設', '威', '戴', '啟', '天', '旻', '易', '邦', '廈', '村', '作', '酒', '枝', '蓮', '得', '商', '鑫', '洋', '陽', '院', '款', '念', '恆', '郁', '芳', '惠', '俊', '富', '部', '閎', '觀', '達', '靖', '壽', '賃', '卉', '穎', '沛', '憲', '詩', '樺', '馨', '婕', '玻', '館', '琪', '語', '期', '仙', '簡', '書', '鋒', '境', '系', '添', '喜', '凌', '照', '魏', '遠', '瑜', '淨', '藝', '余', '顏', '定', '玲', '金', '斯', '亨', '谷', '旺', '唐', '關', '廖', '鏡', '怡', '辰', '訊', '曉', '橋', '膠', '助', '松', '創', '服', '車', '料', '綺', '鍾', '桂', '張', '秉', '翔', '芬', '資', '腦', '何', '毅', '靜', '常', '油', '所', '淑', '麗', '姜', '泰', '侑', '岳', '晨', '飾', '星', '嬌', '巧', '瀚', '體', '私', '晉', '妤', '雄', '升', '昌', '全', '媒', '容', '董', '萍', '主', '央', '宥', '炳', '飲', '女', '馬', '伊', '華', '果', '珍', '陳', '暘', '昱', '青', '旅', '雯', '旭', '柏', '倉', '空', '傳', '睿', '多', '桃', '流', '發', '誼', '希', '其', '國', '環', '秀', '居', '霞', '瑛', '洪', '映', '虹', '軒', '恩', '傅', '煜', '處', '昭', '黎', '衣', '凍', '西', '葉', '伯', '齊', '賢', '人', '土', '群', '雅', '守', '鈦', '僑', '莊', '璃', '斌', '豐', '數', '銷', '允', '昆', '妮', '首', '籌', '仁', '迅', '茶', '久', '印', '燿', '織', '修', '鐘', '格', '飛', '榕', '裕', '苗', '煒', '託', '業', '磊', '班', '集', '覽', '買', '圖', 'isnull']

'''
load model first
'''
trainied_model = Classifier()
model = torch.load("./best_model.pth", map_location=torch.device('cpu'))
trainied_model.load_state_dict(model)
trainied_model.eval()

def generate_server_uuid(input_string):
    """ Create your own server_uuid.

    @param:
        input_string (str): information to be encoded as server_uuid
    @returns:
        server_uuid (str): your unique server_uuid
    """
    s = hashlib.sha256()
    data = (input_string + SALT).encode("utf-8")
    s.update(data)
    server_uuid = s.hexdigest()
    return server_uuid


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

def preprocess(image):
    compose = [
        transforms.ToPILImage(),
        transforms.Resize((64, 64)),
        transforms.Grayscale(num_output_channels=3),
        transforms.ToTensor(),
    ]
    transform = transforms.Compose(compose)
    return transform(image)


def predict(image):
    """ Predict your model result.

    @param:
        image (numpy.ndarray): an image.
    @returns:
        prediction (str): a word.
    """

    ####### PUT YOUR MODEL INFERENCING CODE HERE #######
    img = preprocess(image)
    key = torch.argmax(trainied_model(img.unsqueeze(0)))
    prediction = dict_[key]

    # prediction = '陳'
    ####################################################
    if _check_datatype_to_string(prediction):
        return prediction


def _check_datatype_to_string(prediction):
    """ Check if your prediction is in str type or not.
        If not, then raise error.

    @param:
        prediction: your prediction
    @returns:
        True or raise TypeError.
    """
    if isinstance(prediction, str):
        return True
    raise TypeError('Prediction is not in string type.')


@app.route('/inference', methods=['POST'])
def inference():
    """ API that return your model predictions when E.SUN calls this API. """
    data = request.get_json(force=True)

    # 自行取用，可紀錄玉山呼叫的 timestamp
    esun_timestamp = data['esun_timestamp']

    # 取 image(base64 encoded) 並轉成 cv2 可用格式
    image_64_encoded = data['image']
    image = base64_to_binary_for_cv2(image_64_encoded)

    t = datetime.datetime.now()
    ts = str(int(t.utcnow().timestamp()))
    server_uuid = generate_server_uuid(CAPTAIN_EMAIL + ts)

    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(image_64_encoded, f, ensure_ascii=False, indent=4)

    try:
        answer = predict(image)
    except TypeError as type_error:
        # You can write some log...
        raise type_error
    except Exception as e:
        # You can write some log...
        raise e
    server_timestamp = time.time()

    return jsonify({'esun_uuid': data['esun_uuid'],
                    'server_uuid': server_uuid,
                    'answer': answer,
                    'server_timestamp': server_timestamp})

@app.route('/testget', methods=['GET'])
def testget():
    return "get success"



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8080, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', port=options.port, debug=options.debug)
    
