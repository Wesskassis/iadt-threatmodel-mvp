from PIL import Image
import random
COMPONENT_LABELS=["user","service","api","db","queue","cache","external","network","server","storage","webapp"]
def detect_components(image_path:str):
    random.seed(42)
    img=Image.open(image_path).convert("RGB")
    W,H=img.size
    dets=[]
    for _ in range(5):
        w=max(60,W//6); h=max(60,H//6)
        x=random.randint(0,max(0,W-w)); y=random.randint(0,max(0,H-h))
        dets.append({"label":random.choice(COMPONENT_LABELS),"confidence":0.8,"bbox":[x,y,w,h]})
    return {"image":image_path,"width":W,"height":H,"detections":dets}
