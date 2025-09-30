# IADT Threat Modeling MVP (STRIDE + Computer Vision)

[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-ready-green)](#)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#)

**Goal:** parse **architecture diagrams** (image), detect **components**, and generate a **STRIDE Threat Modeling Report** with recommended **mitigations**.

The repo ships with a **FastAPI** endpoint, a **CLI pipeline**, a **STRIDE catalog**, a **YOLO/COCO dataset scaffold**, and a **video script**.

---

## 🚀 Quickstart

### 1) Environment
```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Generate report (CLI)
```bash
python -m src.pipeline --image examples/diagram_example.png --out reports/report.html
# Windows: Start-Process .\reports\report.html
# Linux/Mac: open ./reports/report.html
```

> Also works running the file directly:
> ```bash
> python src/pipeline.py --image examples/diagram_example.png --out reports/report.html
> ```

### 3) Run the API
```bash
uvicorn api.app:app --reload --port 8080
# Open http://127.0.0.1:8080/docs (Swagger)
```

**Upload test (3 ways):**

- **Swagger UI:** `http://127.0.0.1:8080/docs` → POST `/analyze` → *Try it out* → choose the image → *Execute*.
- **Windows PowerShell 5.1 (Invoke-WebRequest):**
  ```powershell
  $Form = @{ file = Get-Item ".\examples\diagram_example.png" }
  $r = Invoke-WebRequest "http://127.0.0.1:8080/analyze" -Method Post -Form $Form
  $json = $r.Content | ConvertFrom-Json
  $json.report_html | Out-File ".\reports\report_api.html" -Encoding utf8
  Start-Process ".\reports\report_api.html"
  ```
- **curl:**
  ```bash
  curl -F "file=@examples/diagram_example.png" http://127.0.0.1:8080/analyze -o reports/resp.json
  python - << 'PY'
import json, pathlib
j=json.load(open("reports/resp.json","r",encoding="utf-8"))
pathlib.Path("reports/report_api.html").write_text(j["report_html"], encoding="utf-8")
print("Saved to reports/report_api.html")
PY
  ```

---

## 🧠 How it works

1. **Detector (mock)** produces bounding boxes for components in the diagram (`user, api, db, webapp…`).  
   > Replace with a real model (YOLO/Detectron) trained on your annotated diagrams.
2. **Stride Mapper** applies `docs/ThreatCatalog.yaml` to map **S/T/R/I/D/E** threats and **mitigations**.
3. **Reporter** renders an **HTML** report with a STRIDE table and next steps.

---

## 📦 Structure

```
src/
  detector.py
  stride_mapper.py
  reporter.py
  pipeline.py
api/
  app.py
docs/
  ThreatCatalog.yaml
  Guia_Anotacao.md
  Video_Roteiro.md
dataset/
  data.yaml
  images/train|val
  labels/train|val
training/
  train_yolo.py
examples/
  diagram_example.png
reports/
  report.html
```

---

## 🗺️ Roadmap

- [ ] Replace mock detector with a trained YOLO model  
- [ ] Enrich `ThreatCatalog.yaml` with standards (OWASP/NIST/CIS)  
- [ ] Export **JSON** threat model and generate **PDF** report  
- [ ] CI/CD integration (report per PR)

---

## ❗ Troubleshooting

- **`ModuleNotFoundError: No module named 'src'`**  
  Run from repo **root**: `python -m src.pipeline ...`  
  Ensure `src/` and `api/` have `__init__.py`.

- **`No module named 'yaml'` or upload error**  
  `pip install -r requirements.txt` (includes `pyyaml` and `python-multipart`).

- **`/analyze` “Not Found” in browser**  
  `/analyze` is **POST**. Use Swagger at `http://127.0.0.1:8080/docs`.

- **PowerShell 5.1 lacks `-Form` on `Invoke-RestMethod`**  
  Use `Invoke-WebRequest -Form` (above), **PowerShell 7**, or **curl**.

---

## 📄 License

MIT
