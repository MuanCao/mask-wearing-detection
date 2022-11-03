def loadXmlandImg(xmlDir, loadImg=False, imgDir=imgDir, resize=False):
    # 输出的size是一个元组（w，h），theObjs为列表，每一位是一个字典，键name->标签，键box->[xxyy]
    xml = ET.parse(xmlDir)
    size = (
        int(xml.find("size").find("width").text),
        int(xml.find("size").find("height").text)
    )

    objs = xml.findall("object")
    theObjs = []
    # 遍历每个物品框生成一堆字典
    for obj in objs:
        bndbox = obj.find("bndbox")
        boxXXYY = [int(bndbox.find("xmin").text), int(bndbox.find("xmax").text),
                   int(bndbox.find("ymin").text), int(bndbox.find("ymax").text)]
        if resize:
            boxXXYY[0] *= resize[0] / size[0]
            boxXXYY[1] *= resize[0] / size[0]
            boxXXYY[2] *= resize[1] / size[1]
            boxXXYY[3] *= resize[1] / size[1]
        theObjs.append({
            "label": labelDic[obj.find("name").text],
            "box": boxXXYY
        })
    # 选择是不是加载图片
    if loadImg:
        fileName = xml.find("filename").text
        fileName = os.path.join(imgDir, fileName)
        img = cv2.imread(fileName)
        if resize:
            img = cv2.resize(img, resize)
        img = (cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype("float32") / 255.0).transpose(2, 0, 1)
        return size, theObjs, img
    else:
        return size, theObjs
