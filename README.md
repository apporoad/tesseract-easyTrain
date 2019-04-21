# tesseract-easyTrain
    windows tesseract4.0 train shell swapper
    windows only  
    linux need edit *.py 

## tools
1. magick and env set
2. tesseract4 and env set  
3. jdk7 + (8 suggested)
4. jTessBoxEditor 
5. python 3+

## step by step
1. convert pdfs (others ) to pics
```bash
magick -density 400 -units PixelsPerInch  xxx.pdf xxx.jpg
```
2. recognise pic 
```bash
tesseract cc.jpg  tgt -l chi_sim --psm 1
```
3. vi tgt.txt
    find error content
4. cut errror parts 
    like  1.jpg 2.jpg
5. add pic to train
```bash
python xxx/xxx/step1.addTrainPic.py 1.jpg
```
6. editBox
```bash
python xxx/xxx/step2.editBox.py
```
7. train
```bash
python xxx/xxx/step3.train.py [newLang]
```
8. re recognise pic 
```bash
tesseract cc.jpg  tgt -l newLang+chi_sim --psm 1
```
