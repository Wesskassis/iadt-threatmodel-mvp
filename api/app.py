# api/app.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, Response
from PIL import Image, UnidentifiedImageError
import io, pathlib, sys

# --- Garantir que a raiz do projeto esteja no sys.path (evita erro de import)
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Imports do pipeline
from src.detector import detect_components
from src.stride_mapper import map_threats
from src.reporter import render_report

app = FastAPI(title="IADT Threat Modeling API", version="0.1.0")

# ---- Página inicial com form de upload (GET /)
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html><body style="font-family: system-ui; max-width: 720px; margin: 40px auto;">
      <h1>IADT Threat Modeling – Upload</h1>
      <form action="/report" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" />
        <button type="submit">Analisar (ver HTML)</button>
      </form>
      <p>Ou use <a href="/docs">/docs</a> (Swagger) para testar os endpoints.</p>
      <ul>
        <li>POST <code>/analyze</code> → JSON com detections, threats e report_html</li>
        <li>POST <code>/report</code> → retorna o HTML do relatório diretamente</li>
      </ul>
    </body></html>
    """

# ---- Healthcheck (GET /health)
@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Ajuda para GET /analyze no navegador
@app.get("/analyze")
def analyze_get():
    return {"detail": "Use POST /analyze com form-data: file=<imagem>"}

# ---- POST /analyze → JSON
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Envie um arquivo de imagem.")
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Envie uma imagem.")

    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida.")

    tmp_path = pathlib.Path("examples") / f"upload_{file.filename}"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(tmp_path)

    det = detect_components(str(tmp_path))
    th = map_threats(det)
    html = render_report(det, th)
    return JSONResponse({"detections": det, "threats": th, "report_html": html})

# ---- POST /report → HTML direto (bom para abrir no navegador)
@app.post("/report", response_class=HTMLResponse)
async def report(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Envie um arquivo de imagem.")
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Envie uma imagem.")

    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida.")

    tmp_path = pathlib.Path("examples") / f"upload_{file.filename}"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(tmp_path)

    det = detect_components(str(tmp_path))
    th = map_threats(det)
    html = render_report(det, th)
    return HTMLResponse(content=html, status_code=200)

@app.post("/download")
async def download(file: UploadFile = File(...)):
    # validação básica
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Envie um arquivo de imagem.")
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="Tipo de arquivo inválido. Envie uma imagem.")

    # abre a imagem recebida
    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Arquivo não é uma imagem válida.")

    # salva cópia (opcional) em examples/
    tmp_path = pathlib.Path("examples") / f"upload_{file.filename}"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(tmp_path)

    # roda o pipeline e gera HTML
    det = detect_components(str(tmp_path))
    th  = map_threats(det)
    html = render_report(det, th)

    # sugere um nome de arquivo com base na imagem enviada
    stem = pathlib.Path(file.filename).stem
    download_name = f"report_{stem}.html"

    # devolve como DOWNLOAD (attachment)
    return Response(
        content=html.encode("utf-8"),
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{download_name}"'
        },
    )
