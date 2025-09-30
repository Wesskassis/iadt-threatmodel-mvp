# IADT Threat Modeling MVP (STRIDE + Computer Vision)

[![Build](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-ready-green)](#)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#)

**Objetivo:** interpretar **diagramas de arquitetura** (imagem), identificar **componentes** e gerar um **Relatório de Modelagem de Ameaças** segundo **STRIDE**, com **mitigações** sugeridas.

O repositório inclui **API (FastAPI)**, **pipeline CLI**, **catálogo STRIDE**, **scaffold de dataset (YOLO/COCO)** e **roteiro de vídeo**.

---

## 🚀 Como executar (local)

### 1) Preparar ambiente
```bash
python -m venv .venv
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 2) Gerar relatório via CLI
```bash
python -m src.pipeline --image examples/diagram_example.png --out reports/report.html
# Windows: Start-Process .\reports\report.html
# Linux/Mac: open ./reports/report.html  (ou xdg-open)
```

> Também funciona chamando o arquivo diretamente:
> ```bash
> python src/pipeline.py --image examples/diagram_example.png --out reports/report.html
> ```

### 3) Subir a API
```bash
uvicorn api.app:app --reload --port 8080
# Acesse http://127.0.0.1:8080/docs (Swagger)
```

**Testar upload (3 jeitos):**

- **Swagger UI:** `http://127.0.0.1:8080/docs` → POST `/analyze` → *Try it out* → selecione a imagem → *Execute*.
- **PowerShell 5.1 (Invoke-WebRequest):**
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
print("Salvo em reports/report_api.html")
PY
  ```

---

## 🧠 Como funciona

1. **Detector (mock)** lê a imagem do diagrama e retorna *bounding boxes* de componentes (`user, api, db, webapp…`).  
   > Em produção, substitua por um modelo real (YOLO/Detectron) treinado com seus diagramas.
2. **Stride Mapper** aplica `docs/ThreatCatalog.yaml` para mapear ameaças **S/T/R/I/D/E** e **mitigações** por tipo de componente.
3. **Reporter** gera **HTML** com tabela STRIDE e próximos passos.

---

## 📦 Estrutura

```
src/
  detector.py         # detector mock (substituir por modelo treinado)
  stride_mapper.py    # aplica catálogo STRIDE por componente
  reporter.py         # gera o relatório HTML
  pipeline.py         # CLI: imagem -> relatório

api/
  app.py              # FastAPI (POST /analyze)

docs/
  ThreatCatalog.yaml  # catálogo STRIDE (ameaças + mitigações por componente)
  Guia_Anotacao.md    # como anotar dataset (YOLO/COCO)
  Video_Roteiro.md    # roteiro da apresentação/demonstração
  img/report_preview.png  # (opcional) preview visual

dataset/
  data.yaml           # config YOLO
  images/train|val
  labels/train|val

training/
  train_yolo.py       # comando de referência (Ultralytics YOLO)

examples/
  diagram_example.png # diagrama de exemplo

reports/
  report.html         # relatório gerado pela CLI (exemplo)
```

---

## 🔐 Catálogo STRIDE

Arquivo: `docs/ThreatCatalog.yaml`  
Para cada **tipo de componente**, define:
- **Ameaças** (S/T/R/I/D/E)
- **Mitigações** recomendadas

> Personalize esse catálogo para a sua realidade (ex.: OWASP ASVS, NIST, CIS).

---

## 🗺️ Roadmap

- [ ] Substituir o **detector mock** por modelo YOLO treinado com diagramas anotados  
- [ ] Ampliar `ThreatCatalog.yaml` com padrões corporativos  
- [ ] Exportar **JSON** do modelo de ameaças e gerar **PDF** do relatório  
- [ ] Integração em **CI/CD** (gerar relatório a cada PR)

---

## ❗ Solução de problemas

- **`ModuleNotFoundError: No module named 'src'`**  
  Rode a partir da **raiz**: `python -m src.pipeline ...`  
  e garanta que `src/` e `api/` têm `__init__.py`.

- **`No module named 'yaml'` ou erro de upload**  
  `pip install -r requirements.txt` (inclui `pyyaml` e `python-multipart`).

- **`/analyze` “Not Found” ao abrir no navegador**  
  `/analyze` é **POST**. Use o Swagger em `http://127.0.0.1:8080/docs`.

- **PowerShell 5.1 não reconhece `-Form` em `Invoke-RestMethod`**  
  Use `Invoke-WebRequest -Form` (exemplo acima) ou **PowerShell 7** ou **curl**.

---

## 📄 Licença

MIT — use, modifique e contribua livremente.

---

### 🇬🇧 English
See `README.en.md` for an English version.
