"""
 File : Test_Budget.py
 Writer : Meohong
 Objective : Testing Predict Budget AI Model (using Autogluon)
 First Write : 23 / 10 / 12
 
 Modify
 ==============================================================
    No.  |    Date    |                Detail
 --------------------------------------------------------------
    1    |   10/12    |             first write
    2    |   10/13    |   Add file directory route Tracking 
   ...   |    ...     |                 ....
    3    |   10/13    |             final modify
 ==============================================================
"""

import pandas as pd
import numpy as np
import random
import os
import sys
import warnings
from autogluon.tabular import TabularDataset, TabularPredictor
from sklearn.preprocessing import StandardScaler
import anvil.server
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

warnings.filterwarnings(action='ignore')
anvil.server.connect("server_QQ62KHHLTT3ZG237K7EG32EM-4IQLTPYPGEJZ5WKN")

path = os.path.dirname(os.path.realpath(__file__))

#데이터셋 로드 및 "Unnamed: 0"컬럼 삭제 (인덱스 컬럼)
testsets = pd.read_csv(path+"/testsets.csv", encoding='cp949')
testsets.drop(columns=['Unnamed: 0'], inplace=True)
print("load dataset Success")

# Autogluon 예측모델 로드
predictor = TabularPredictor(
    label='2023년-전기', problem_type='regression',
    eval_metric = 'rmse'
    ).load(path=path+'/AutogluonModels/TESTMODEL1')
print("load Success\n")

# '종목' 문자열 레이블링 함수
def event_labeling(predict_dataset):
    Event_Array = predict_dataset["종목"].unique()
    mapping = {}
    i = 0
    for event in Event_Array :
        mapping[event] = i
        i = i + 1
    predict_dataset.replace({"종목": mapping},inplace=True)
    
# 예측 후, 퍼센티지로 변환하기 위한 함수 (map용)
def percentage(n, sum):
    return (n / sum)

# Anvil에서 호출할 수 있는 함수
@anvil.server.callable
def predict_budget(objects):
    # 가져온 변수 리스트를 변수에 각각 다시 할당
    total_budget, Object1, Object2, Object3, Object4, Object5 = objects
    Sscaler = StandardScaler()

    # 데이터셋중 가장 첫번째 행들 (종목별로)을 가져오고 (왜냐하면 마이데이터를 활용할것이기 때문)
    data1 = pd.DataFrame([dict(testsets[testsets["종목"]==Object1].iloc[0])])
    data2 = pd.DataFrame([dict(testsets[testsets["종목"]==Object2].iloc[0])])
    data3 = pd.DataFrame([dict(testsets[testsets["종목"]==Object3].iloc[0])])
    data4 = pd.DataFrame([dict(testsets[testsets["종목"]==Object4].iloc[0])])
    data5 = pd.DataFrame([dict(testsets[testsets["종목"]==Object5].iloc[0])])
    predict_dataset = pd.concat([data1, data2, data3, data4, data5], ignore_index=True)

    # 데이터셋을 전처리한다.
    predict_dataset.drop(columns=['동아리명'], inplace=True)    # 동아리명 Drop
    # 문자열 -> 숫자 레이블링
    event_labeling(predict_dataset)
    # 데이터 스케일링
    scaled_dataset = pd.DataFrame(Sscaler.fit_transform(predict_dataset))
    # 데이터셋을 타블러데이터셋으로 변환
    test_df = TabularDataset(scaled_dataset)
    
    # 예측
    predict = predictor.predict(test_df)
    predict = (np.round(predict, -2))
    predict = list(map(int, predict))

    # 비율 계산
    predictsum = [ sum(predict) for i in range(0,len(predict)) ]
    real_budget_predict = list(map(percentage, predict, predictsum))
    real_budget_predict = list(np.round(real_budget_predict, 4))

    # 현재 예산에 맞춰서 재편성
    final_predict =  [int(radios * total_budget) for radios in real_budget_predict]

    return final_predict

# Anvil Web App의 버튼동작으로 함수가 호출될 때까지 영원히 기다림..
print("****************************************************************")
print("\nAnvil Web APP page : https://dependent-corny-soup.anvil.app/")
print("waiting for call . . . \n")
print("****************************************************************")
anvil.server.wait_forever()
