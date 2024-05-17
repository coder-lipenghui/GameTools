from PIL import Image
import xml.etree.ElementTree as ET
import os

def generate_images_from_xml(xml_file, source_image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    tree = ET.parse(xml_file)
    root = tree.getroot()[0][1]
    
    files={}
    fileName=""
    for child in root:
        if child.tag=="key":
            fileName=child.text
            files[fileName]={}
        if child.tag=="dict":
            temp=1
            key=""
            for childd in child:
                if temp%2==0:
                    if key=="rotated":
                        files[fileName][key]=childd.tag=="true"
                    else:
                        vv=childd.text
                        vv=vv.replace("{","").replace("}","")
                        vv=vv.strip()
                        files[fileName][key]=vv.split(',')
                else:
                    key=childd.text
                    key=key.strip()
                temp=temp+1
        
            rotated=files[fileName]["rotated"]
            frame=files[fileName]["frame"]
            offset=files[fileName]["offset"]
            sourceColorRect=files[fileName]["sourceColorRect"]
            sourceSize=files[fileName]["sourceSize"]
            x=int(frame[0])
            y=int(frame[1])
            w=int(frame[2])
            h=int(frame[3])
            ox=int(offset[0])
            oy=int(offset[1])
            crop_box = (x, y, x+w, y+h)
            output_path = os.path.join(output_folder, fileName)
            paste_position=(int(sourceColorRect[0]),int(sourceColorRect[1]))
            if rotated:
                crop_box = (x, y, x+h, y+w)
            else:
                crop_box = (x, y, x+w, y+h)
            crop_and_paste(source_image_path,output_path,crop_box,paste_position,(ox,oy),int(sourceSize[0]),int(sourceSize[1]),rotated)
            

def crop_and_paste(input_image_path, output_image_path, crop_box, paste_position,offset,width,height,rotated):
    
    output_folder = os.path.dirname(output_image_path)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if os.path.exists(output_image_path):
        os.remove(output_image_path)
    # 这是SourceSize不规则的情况下使用的，如果SorceSize是统一的则改为 False
    if True: 
        width=1024  # 希望生成的图片大小
        height=1024 # 希望生成的图片大小
        centerX=int(width/2) # 图片生成的中心点
        centerY=int(height/2) # 图片生成的中心点

        paste_position=(centerX+offset[0],centerY+100-offset[1])
    input_image = Image.open(input_image_path)
    cropped_image = input_image.crop(crop_box)
    rotated_image=cropped_image
    if rotated:
        rotated_image = cropped_image.rotate(90, expand=True)
    try:
        output_image = Image.open(output_image_path)
    except FileNotFoundError:
        output_image = Image.new("RGBA", (width,height))
    output_image.paste(rotated_image, paste_position)
    output_image.save(output_image_path,format="PNG")

# 生成图片
folder_path="{your root folder}"
for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)
    if os.path.isfile(item_path) and item.endswith('.plist'):
        filename = os.path.splitext(item)[0]
        print(filename)
        parent_folder = os.path.abspath(os.path.dirname(item_path))
        xml_file = os.path.join(parent_folder,filename+".plist")
        source_image_path = os.path.join(parent_folder,filename+".png")
        output_folder = os.path.join(parent_folder,filename)
        generate_images_from_xml(xml_file, source_image_path, output_folder)
        break