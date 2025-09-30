import yaml, pathlib
CATALOG_PATH=pathlib.Path(__file__).resolve().parent.parent/"docs"/"ThreatCatalog.yaml"
def map_threats(detection_result:dict):
    catalog=yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8"))
    comp=catalog["components"]
    out=[]
    for d in detection_result["detections"]:
        e=comp.get(d["label"],{})
        stride={k:e.get(k,[]) for k in ["spoofing","tampering","repudiation","information_disclosure","denial_of_service","elevation_of_privilege"]}
        out.append({"component":d["label"],"bbox":d["bbox"],"confidence":d["confidence"],"stride":stride,"mitigations":e.get("mitigations",[])})
    return {"image":detection_result["image"],"threats":out}
