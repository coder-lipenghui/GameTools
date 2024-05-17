import os
import sys
import shutil
from PIL import Image

# 参数描述: 动作文件夹名称,帧数,方向数,是否翻转
# 按照顺序将资源归类到对应的文件夹中

imgSize=1024     # 生成的图像大小
FlipX=True       # 是否水平翻转

#参数描述：动作文件夹名称，帧数，方向数
desp=[
    ["动作1",8,8],
    ["动作2",6,8],
    ["动作3",8,8],
    ["动作4",6,8],
    ["动作5",9,8],
    ["动作6",7,8],
    ["动作7",5,8],
    ["动作8",9,8],

    # ["攻击特效1",8,8],
    # ["攻击特效2",8,8],
]

dirs=[
    "上",
    "右上",
    "右",
    "右下",
    "下",
    "左下",
    "左",
    "左上",
]


if __name__ == "__main__":
    '''
    使用pyinstaller生成exe文件:pyinstaller -F -i icon.ico -legend.py
    生成Legend私服资源，资源会按照中心点位置生成到1024*1024的新图片上
    '''
    #error  https://cn.dll-files.com/api-ms-win-core-path-l1-1-0.dll.html
    #root="C:/Users/lipenghui/Desktop/test/测试资源/monster/Mon205" #sys.argv[1]
    root=sys.argv[1]
    batch=False
    if len(sys.argv)>2:
        batch=int(sys.argv[2])>0
    roots=[]
    # if not os.path.exists(root+"/Placements"):
    #     print("不存在Placements目录")
    #     exit(1)
    if batch :
        tmp=os.listdir(root)
        for folder in tmp:
            if os.path.isdir(os.path.join(root,folder)) :
                roots.append(os.path.join(root,folder))
    else:
        roots.append(root)
    
    if FlipX:
           dirs=dirs[:1] + dirs[:0:-1]

    for folder in roots:
        imgs=os.listdir(folder)
        for img in imgs:
            imgPath=os.path.join(folder,img)
            newImgPath=os.path.join(folder,"Gen",img)
            if os.path.exists(newImgPath):
                continue
            if os.path.isfile(imgPath) and img.upper().endswith(".PNG"):
                with Image.open(imgPath) as im:
                    w=im.size[0]
                    h=im.size[1]
                    if w>1 and h>1:
                        txt=img.split(".")[0]
                        txtPath=os.path.join(folder,"Placements",txt+".txt")
                        if os.path.exists(txtPath):
                            f = open(txtPath,"r")
                            fileStr = f.read()
                            f.close()
                            xy=fileStr.split("\n")
                            x=str(xy[0])
                            y=str(xy[1])
                            newImg=Image.new("RGBA",[imgSize,imgSize])
                            centerX=int(imgSize/2)
                            centerY=int(imgSize/2)
                            newImg.paste(im,[centerX+int(x),centerY+int(y)])
                            newImgPath=os.path.join(folder,"Gen")
                            if not os.path.exists(newImgPath):
                                os.mkdir(newImgPath)
                            if FlipX:
                                newImg=newImg.transpose(Image.FLIP_LEFT_RIGHT)
                            newImg.save(os.path.join(newImgPath,img))
                            newImg=None
    root=os.path.join(folder,"Gen")
    for info in(desp):
        dirFolder=info[0]
        frameNum=info[1]
        dirNum=info[2]
        total=frameNum*dirNum
        list=os.listdir(root)
        list.sort()
        print("正在归类资源:",dirFolder,"帧数:",frameNum,"方向数:",dirNum,"图片数量:",total)

        #整个动作的资源
        imgs=list[0:total]
        for i in range(0,len(dirs)):
            start=i*frameNum
            end=start+frameNum
            needMove=imgs[start:end]
            dirName=dirs[i]
            
            # print("本次移动资源数量:",len(needMove),start,end)
            # print(needMove)
            for file in needMove:
                if file == '.DS_Store':
                    continue
                destination=os.path.join(root,dirFolder,dirName)
                if not os.path.exists(destination):
                    os.makedirs(destination)
                target_file = os.path.join(destination,os.path.basename(file))
                if os.path.exists(target_file):
                    os.remove(target_file)
                # print("正在将资源:",root+file,"移动至:",target_file)
                shutil.move(os.path.join(root,file), target_file)