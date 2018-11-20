import sys
import time
import os,shutil,os.path
#print(sys.argv[0], sys.argv[1])

currentPath = os.path.dirname(os.path.realpath(__file__)) 

# init workdirs
if os.path.exists(currentPath + '/train') ==False :
    os.makedirs(currentPath + '/train')
if os.path.exists(currentPath + '/tiffs') ==False :
    os.makedirs(currentPath + '/tiffs')
if os.path.exists(currentPath + '/tessdata') ==False :
    os.makedirs(currentPath + '/tessdata')

currentPath = currentPath + "/tiffs"

cwd = os.getcwd()

def run():
    if len(sys.argv) == 1:
        print('必须传文件名 ， 命令行如：python step1.addTrainPic.py d:/1.jpg')
        return
    sourceFile = sys.argv[1]
    if os.path.isabs(sourceFile) == False :
        sourceFile = cwd + "/" + sourceFile
    # print(sourceFile)
    # print(os.path.exists(sourceFile))
    if(os.path.exists(sourceFile)) == False : 
        print('文件不存在:' + sys.argv[1])
        return
    
    filenameWithoutFix = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))  + "_" +os.path.splitext(os.path.basename(sourceFile))[0]
    filename =  filenameWithoutFix+ ".tif"
    # 将文件放入tiffs
    tgtFilePath = currentPath + "/" + filename
    
    os.system('magick.exe '+ sourceFile+' '+ tgtFilePath)
    print('加入到tiffs成功：' + tgtFilePath)

    # 生成.box
    #tesseract chi_my.font.exp0.tif chi_my.font.exp0 -l chi_sim batch.nochop makebox
    os.system('tesseract ' + tgtFilePath + ' ' + (currentPath + "/"+ filenameWithoutFix) + ' -l chi_sim batch.nochop makebox')
    print('生成box成功：' + (currentPath + "/"+ filenameWithoutFix) )
    return 

#os.system("echo \"hello good day\"")
run()

#print(os.path.splitext(os.path.basename('/abc/1bc'))[0])
#print(os.getcwd())