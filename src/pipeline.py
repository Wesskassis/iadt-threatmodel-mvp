# src/pipeline.py
import argparse
import pathlib
import sys

# --- Fallback para execução direta: garante que a raiz do projeto esteja no sys.path
# pasta_atual = .../src  -> raiz = .../
THIS_FILE = pathlib.Path(__file__).resolve()
PROJECT_ROOT = THIS_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Tenta import absoluto (quando roda como script) e relativo (quando roda com -m)
try:
    from src.detector import detect_components
    from src.stride_mapper import map_threats
    from src.reporter import render_report
except ModuleNotFoundError:
    # Executado como pacote: python -m src.pipeline
    from .detector import detect_components
    from .stride_mapper import map_threats
    from .reporter import render_report


def main():
    ap = argparse.ArgumentParser(description="Gera relatório STRIDE a partir de um diagrama.")
    ap.add_argument("--image", required=True, help="Caminho da imagem de diagrama (PNG/JPG).")
    ap.add_argument("--out", required=True, help="Caminho de saída do relatório HTML.")
    args = ap.parse_args()

    det = detect_components(args.image)
    threats = map_threats(det)
    html = render_report(det, threats)

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"[OK] Relatório gerado em: {out_path.resolve()}")


if __name__ == "__main__":
    main()
