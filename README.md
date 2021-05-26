# esun_fintech


:rocket: rank: 43


## 5/26
:trophy: [solved] 5/25 1. 2.

:exclamation: 待解決問題
1. model accuracy 不夠 :dash:  結果為 0.787 acc


## 5/25
:exclamation: 待解決問題

1. connection fail issue :dash:  近8000筆資料 :point_right: 1058筆connection fail / 6663筆成功 [見log檔](https://docs.google.com/spreadsheets/d/1MOVoaUy45of2n_W1WR_OtxHR-_iFLVQtZrdvdR8Zoqg/edit#gid=244301917)
2. model accuracy 不夠 :dash:  結果為 0.44 acc


## 5/18 會議記錄
1. 23號之前將clean data number紀錄至train folder內的[readme](https://github.com/oceanchad/esun_fintech/tree/main/train#label%E5%88%86%E9%A1%9E)
2. 自行嘗試model，評估效能

## 5/12 會議記錄

待完成
1. clean data
2. model 自行嘗試
   1. edge detection + model

待討論
1. 資料前處理 pipeline

## 5/5 會議記錄

### dirty data 分佈
> 類別分類如下
> isnull定義: 分辨不出來，則為isnull
1. 含非字的線: 32
2. 字被印章蓋過: 981
3. 兩個字在同張圖: 121
4. 簡體字型:
5. 自行定義:
6. 自行定義:

#### Clean data

1. 紀錄dirty data
2. 改label, isnull

##### assignment
1. 將異常的label改成正確的label將原始資料記錄下來，並分類為何異常
2. 統計異常的數量與紀錄為什麼類型的異常

* Luca 1 - 10000
* Carol 10001 - 20000
* Zane 20001 - 30000
* Felix 30001 - 40000
* Joshephyi 40001 - 50000
* Kai 50001 - 60000
* Cheng 60000 - last

### Model 
1. AI-free
2. edge detection + model
