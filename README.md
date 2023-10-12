# Budget_Predict_AI
### __주의!__ Test_Budget.py를 쓰기 위해서, 동봉된 AutogluonModel2.zip파일을 Test_Budget.py이 있는 폴더 위치에 압축풀기를 해야합니다.

## 1. 개요
이번에 만든 AI 모델은 Autogluon을 활용한 __"마이 데이터를 바탕으로 예산을 예측하는 AI 모델, BuPA(Budget Predict AI)__ 입니다.<br>
Autogluon을 활용하여, 이전까지 사용한 예산 데이터를 바탕으로, 현재 배당해야할 예산을 자동으로 예측해주는 모델입니다.<br>
가장 큰 장점으로, 모델을 정할 필요 없이, Autogluon API를 활용하여, 여러 모델을 한번에 학습하고, 가장 성능이 좋은 모델을 뽑아내, 모델 결정의 수고를 덜 수 있습니다.<br>
또한, CPU, GPU(구글 Colab 무료 버전)만으로도 학습이 가능한 가벼운 모델(?)이라는 점이 크다. (3G) <br>
따라서, 적은 컴퓨팅 성능을 요구하면서, 빠르게 예측을 돌릴 수 있는 모델입니다.<br>

## 2. AutoGluon
아마존에서 만든 머신러닝 자동화 오픈소스 Toolkit. <br>
회귀, 분류, 이미지 예측 등에서 사용이 가능, __모델을 선택할 필요가 없이__, ML모델을 만들 수 있고, 특정모델에 관한 학습도 가능<br>
CatBoost, RandomForest, LightGBM, ExtraTree, XGBoost 등의 예측 모델 알고리즘을 한번에 학습하고, 그 중, 가장 성능이 좋은 모델을 선택 혹은 앙상블을 할 수 있다.<br>
Autogluon은 학습 시, Tabular데이터셋을 활용해야 한다. 

## 3. 예측 과정
#### 1) 데이터베이스를 불러오기
