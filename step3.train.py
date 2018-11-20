import sys
import time
import os,shutil,os.path
#print(sys.argv[0], sys.argv[1])

currentPath = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()


# 检查 tiff 和box 是否匹配
def checkTiffBoxFn(path):
    #todo
    return True
def combineBoxFn(sPath,tPath):
    #删除目标文件
    if os.path.exists(tPath) :
        os.unlink(tPath)
    #创建空文件
    tFile = open(tPath,'w',encoding='utf-8')
    ls = os.listdir(sPath)
    frame_num = 0
    for i in range(0,len(ls)):
        path = os.path.join(sPath,ls[i])
        fixs = os.path.splitext(path)
        if os.path.isfile(path) and len(fixs) >0 and fixs[1] =='.box' :
            fopen=open(path,'r',encoding='utf-8')
            # lines=fopen.readlines
            # for line in lines:
            #     print(line)
            #     tFile.writelines(line[:-1] + frame_num)
            line = fopen.readline()             # 调用文件的 readline()方法
            while line:
                #print(line)    
                tFile.writelines(line[:-2] + str(frame_num) + "\n")       
                line = fopen.readline()
            frame_num = frame_num +1 
            fopen.close()
    tFile.close()
    return

def run():
    if len(sys.argv) == 1:
        print('必须输入库名 ， 命令行如：python step3.train.py newLang')
        return
    trainName = sys.argv[1]
    # 检查 tiff 和 box的文件是否匹配
    if checkTiffBoxFn(currentPath + "/tiffs") == False :
        print('tiffs 和 .box 文件不匹配，请检查处理')
        return
    # tiff合并
    combinedTif = currentPath+ '/train/' + trainName + '.font.exp0.tif'
    os.system('magick '+currentPath+'/tiffs/*.tif ' + combinedTif)
    print('tif 合并成功：'  + combinedTif)
    #box 合并
    combinedBox = currentPath+ '/train/' + trainName + '.font.exp0.box'
    combineBoxFn(currentPath + "/tiffs" , combinedBox)
    print('box 合并成功：' + combinedBox)
    
    # 生成font
    font_properties = currentPath + '/train/font_properties'
    print('生成font_properties文件:' + font_properties)
    file = open(font_properties,'w',encoding='utf-8')
    file.write('font 0 0 0 0 0')
    file.close()
    # 生成训练文件
    #tesseract chi_my.font.exp0.tif chi_my.font.exp0 nobatch box.train
    trFileName = currentPath+ '/train/' + trainName + '.font.exp0'
    os.system('tesseract '+ combinedTif +' '+trFileName+' nobatch box.train')
    print('生成训练文件：'+trFileName + '.tr')
    print('如果程序出异常，说明训练中数据存在问题，请手动排除')

    #生成字符集文件
    os.system('unicharset_extractor ' + combinedBox)
    shutil.move(cwd + '/unicharset',currentPath + '/train/unicharset')
    print('生成字符集文件:' +currentPath + '/train/unicharset' )

    #生成字典
    #mftraining -F font_properties -U unicharset -O chi_my.unicharset chi_my.font.exp0.tr
    #cntraining chi_my.font.exp0.tr
    outUnicharset = currentPath + '/train/'+ trainName+'.unicharset'

    os.system('mftraining -F '+ font_properties +' -U '+ currentPath + '/train/unicharset' +' -O '+outUnicharset+' '+trFileName + '.tr')
    os.system('cntraining '+ trFileName + '.tr' )

    shutil.move(cwd + '/inttemp',currentPath + '/train/'+ trainName +'.inttemp')
    shutil.move(cwd + '/normproto',currentPath + '/train/'+ trainName +'.normproto')
    shutil.move(cwd + '/pffmtable',currentPath + '/train/'+ trainName +'.pffmtable')
    shutil.move(cwd + '/shapetable',currentPath + '/train/'+ trainName +'.shapetable')
    print('生成字典')

    os.system('combine_tessdata '+currentPath + '/train/'+ trainName+'.')

    shutil.move(currentPath + '/train/'+ trainName +'.traineddata',currentPath +'/tessdata/' +  trainName +'.traineddata' )
    print('合并数据文件为最终训练数据:' + currentPath +'/tessdata/' +  trainName +'.traineddata')
    cmd = 'copy /y ' + currentPath +'\\tessdata\\' +  trainName +'.traineddata %TESSDATA_PREFIX%\\' + trainName +'.traineddata'
    os.system(cmd)
    print('已复制到对应文件目录，请训练测试 ： tesseract cc.jpg  cc -l chi_sim+'+trainName+' --psm 1')
    return 

#os.system("echo \"hello good day\"")
run()

#print(os.getcwd())