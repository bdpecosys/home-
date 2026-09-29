# Extracting Hebrew TASE filings & reports

## Recipes
- Inspect first: `pdfinfo`, `pdffonts`, sample `pdftotext -f 1 -l 2 file.pdf -`. TASE annual reports run 150-250+ pages — never read linearly.
- Extract all text with layout: `pdftotext -layout file.pdf out.txt`
- Strip RTL/LTR control marks before searching (Python): remove `\u202a \u202b \u202c \u200e \u200f`
- Locate sections by keyword index, then read windows of ±2,000-5,000 chars around hits.
- If a "PDF" fails to parse, check `file` — uploads are sometimes ZIP archives of page images + per-page .txt, or renamed docx.

## Keyword anchors (annual/periodic reports)
- תיאור עסקי התאגיד — business description (Part A)
- דוח הדירקטוריון — directors' report (Part B; financial highlights live here)
- יעדים ואסטרטגיה עסקית — targets & strategy (usually §1.21; check for board-approved revisions and their dates)
- גורמי סיכון — risk factors
- רווח נקי / הון עצמי / תשואה להון — net profit / equity / ROE
- תיק האשראי / התיק המנוהל — credit/managed portfolio (lenders)
- בעלי השליטה / נושאי משרה — controlling shareholders / officers
- ועדת האשראי / ועדת השקעות — credit/investment committee (authority mapping)
- תגמול / עמלות בגין גיוס לקוחות — compensation / client-acquisition commissions (personal incentives)
- מיזוג / רכישה / הנפקה — merger / acquisition / offering
- Search the contact's first name in Hebrew (e.g., ארז) — finds role, committee seats, comp tables.

## Fresh-news pass
Search Hebrew: "[חברה] רבעון" / "[חברה] גיוס" / company name + year. Sources: Bizportal, Globes, Calcalist, TheMarker, TV10, Maya (mayafiles.tase.co.il). Anything dated after the filing goes in the memo as "recent."
