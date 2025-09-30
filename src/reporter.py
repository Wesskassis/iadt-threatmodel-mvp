import datetime, html
def _row(component, conf, stride_dict, mitigations):
    cats=["spoofing","tampering","repudiation","information_disclosure","denial_of_service","elevation_of_privilege"]
    cols=[]
    for c in cats:
        items=stride_dict.get(c,[])
        cols.append("<ul>"+ "".join(f"<li>{html.escape(x)}</li>" for x in items) + "</ul>")
    mitig="<ul>"+ "".join(f"<li>{html.escape(x)}</li>" for x in mitigations) + "</ul>"
    return f"<tr><td>{component}</td><td>{conf:.2f}</td>" + "".join(f"<td>{col}</td>" for col in cols) + f"<td>{mitig}</td></tr>"
def render_report(detections, threats):
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    rows=[_row(t["component"],t["confidence"],t["stride"],t["mitigations"]) for t in threats["threats"]]
    table = "<table border='1' cellspacing='0' cellpadding='6'><thead><tr><th>Comp</th><th>Conf</th><th>S</th><th>T</th><th>R</th><th>I</th><th>D</th><th>E</th><th>Mitig.</th></tr></thead><tbody>"+ "".join(rows) +"</tbody></table>"
    return f"<!doctype html><html><head><meta charset='utf-8'><title>Relatório STRIDE</title></head><body><h1>Relatório</h1><p><b>Data:</b> {now}</p>{table}</body></html>"
