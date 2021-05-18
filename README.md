esun_fintech
# 5/5 會議記錄

## dirty data 分佈
> 類別分類如下
> isnull定義: 分辨不出來，則為isnull
1. 含非字的線: 32
2. 字被印章蓋過: 981
3. 兩個字在同張圖: 121
4. 簡體字型:
5. 自行定義:
6. 自行定義:

### Clean data

1. 紀錄dirty data
2. 改label, isnull

#### assignment
1. 將異常的label改成正確的label將原始資料記錄下來，並分類為何異常
2. 統計異常的數量與紀錄為什麼類型的異常

* Luca 1 - 10000
* Carol 10001 - 20000
* Zane 20001 - 30000
* Felix 30001 - 40000
* Joshephyi 40001 - 50000
* Kai 50001 - 60000
* Cheng 60000 - last

## Model 
1. AI-free
2. edge detection + model

# 5/12

待完成
1. clean data
2. model 自行嘗試
   1. edge detection + model

待討論
1. 資料前處理 pipeline


# 5/18 會議記錄
1. 23號之前將clean data number紀錄至train folder內的readme
2. 自行嘗試model，評估效能

## Label分類
### [改label]
* 因為Label錯誤 (eg. 13863、13967)
* 因為label錯誤且為1.5個字 (eg. 14703、14710)
### [改成isnull]
* 因為有2個字   (eg. 15774、15811)
* 因為只有線條  (eg. 12690、12714)
* 因為線條遮到  (eg. 14658)
* 因為字卡到    (eg. 15840、15892)
* 因為整個空白  (eg. 12201、12284)
* 因為看不出來是什麼 (eg. 14166(stamp)、14309)
* 因為紅底沒字  (eg. 12747、14545(stamp))
* 因為黑底     (eg. 12240、13682)
### [沒改]
* 為簡體字     (eg. 12534、12573)
* 1.5個字      (eg. 13167、13175)
* 有其他線條   (eg. 13569、13756)
* 有紅色印章   (eg. 14865、14929)
* 字有卡到     (eg. 13270、13458)
* 字體翻轉     (eg. 13687、15201)
* 彩色背景     (eg. 15493)
