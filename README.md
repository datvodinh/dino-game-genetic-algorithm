### PROJECT INTRO AI HUST IT3160E
![image](https://user-images.githubusercontent.com/90944231/209748112-7728473f-6d0e-4f4b-b2af-74931e3af76b.png)
### Member:
    1.Võ Đình Đạt 20214890
    2.Đường Minh Quân 20210710
    3.Phan Khôi Nguyên 20210652
    4.Nguyễn Trung Trực 20214936

### How to clone repository
```
git clone https://github.com/datvodinh10/dino-ai-project-intro-ai-hust.git
```
### I.Two way to train/eval model
### 1. Run all the code in main.ipynb (jupyter notebook)
### 2. Run in terminal
-How to Train:
```
python main.py train [num_population] [num_dinosaur] [fps]
```
For example:
```
python main.py train 100 100 1200
```
-How to Evaluate:
```
python main.py eval [fps]
```
For example:
```
python main.py eval 60
```
-Evaluate by human:
```
python humanPLayWithGuidance.py
```
-Evaluate with If Else Algorithm:
```
python GeneticVSHandTuning.py
```
### II.Requirement:
```
pip install pygame
pip install numpy
```
