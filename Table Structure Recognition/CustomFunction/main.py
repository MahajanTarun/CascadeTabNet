
# from border import border
from CustomFunctions.border import border
from mmdet.apis import inference_detector, show_result, init_detector
from google.colab.patches import cv2_imshow
import cv2
# from Functions.blessFunc import borderless
from CustomFunctions.blessFunc import borderless
# import lxml.etree as etree
import glob

i=img

# result = inference_detector(model, i)
res_border = []
res_bless = []
res_cell = []
# root = etree.Element("document")
root = []
table = {}
## for border
for r in result[0][0]:
    if r[4]>.85:
        res_border.append(r[:4].astype(int))
## for cells
for r in result[0][1]:
    if r[4]>.85:
        r[4] = r[4]*100
        res_cell.append(r.astype(int))
## for borderless
for r in result[0][2]:
    if r[4]>.85:
        res_bless.append(r[:4].astype(int))

## if border tables detected 
if len(res_border) != 0:
    ## call border script for each table in image
    for res in res_border:
        try:
            root.append(border(res,cv2.imread(i)))
            # table["table"] = border(res,cv2.imread(i))
            # table.add("table", border(res,cv2.imread(i)))   
        except:
            pass
if len(res_bless) != 0:
    if len(res_cell) != 0:
        for no,res in enumerate(res_bless):
            root.append(borderless(res,cv2.imread(i),res_cell))
            # table["table"] = borderless(res,cv2.imread(i),res_cell)
            # table.add("table", borderless(res,cv2.imread(i),res_cell))

# xmlPath = "/content/result.xml"
table["table"] = root
document = {}
document["document"] = table
print(document)
# myfile = open(xmlPath+i.split('/')[-1][:-3]+'xml', "w")
# myfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
# myfile.write(etree.tostring(root, pretty_print=True,encoding="unicode"))
# myfile.close()
import json
with open('/content/result.json', 'w', encoding='utf-8') as f:
    json.dump(document, f, ensure_ascii=False, indent=4)