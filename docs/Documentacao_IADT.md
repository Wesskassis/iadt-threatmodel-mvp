# Documentação do Fluxo – MVP STRIDE com IA

## Visão geral
- Objetivo: interpretar diagrama de arquitetura (imagem), identificar componentes e gerar relatório STRIDE automático com mitigações.
- Entregáveis: documentação do fluxo, vídeo de demonstração, código no GitHub.

## Fluxo ponta a ponta
1. **Entrada**: imagem do diagrama (.png/.jpg) via API ou CLI.
2. **Detecção de componentes**: `src/detector.py` (mock para MVP; substituível por YOLO treinado).
3. **Mapeamento STRIDE**: `src/stride_mapper.py` usa `docs/ThreatCatalog.yaml` para S/T/R/I/D/E + mitigações.
4. **Geração de Relatório**: `src/reporter.py` renderiza HTML (`reports/report.html`).
5. **API**: `api/app.py`  
   - `POST /analyze` → JSON com `detections`, `threats`, `report_html`  
   - `POST /report` → retorna HTML direto  
   - `POST /download` → baixa o HTML (attachment)

## Como executar (resumo)
- `pip install -r requirements.txt`
- `uvicorn api.app:app --reload --port 8080` → `http://127.0.0.1:8080/docs`
- `python -m src.pipeline --image examples/diagram_example.png --out reports/report.html`

## Dataset e Treino (supervisionado)
- Estrutura em `dataset/` + `training/`.  
- Anotar classes: user, api, db, webapp, etc.  
- Exemplo (Ultralytics): `yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640`  
- Trocar o mock no `detector.py` pelo modelo treinado.

## Decisões e Limitações do MVP
- Detector **mock** para comprovar viabilidade e fluxo end-to-end.
- Catálogo STRIDE mínimo (exemplos) — pode ser expandido (OWASP/NIST/CIS).

## Próximos passos
- Substituir mock por YOLO treinado com 20–50 imagens anotadas.
- Ampliar `ThreatCatalog.yaml` alinhado a padrões da empresa.
- Exportar JSON do threat model e gerar PDF.
- Integrar em CI/CD para gerar relatório a cada PR.
