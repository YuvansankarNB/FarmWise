import os
import subprocess
import markdown

md_path = r"C:\Users\yuvan\Documents\FarmWise-AI\docs\FarmWise_AI_Complete_Feature_Guide.md"
html_path = r"C:\Users\yuvan\Documents\FarmWise-AI\docs\FarmWise_AI_Complete_Feature_Guide.html"
pdf_path = r"C:\Users\yuvan\Documents\FarmWise-AI\docs\FarmWise_AI_Complete_Feature_Guide.pdf"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

html_content = markdown.markdown(text, extensions=["tables", "fenced_code"])

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>FarmWise AI — Feature Architecture & Implementation Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }}

  body {{
    font-family: 'Inter', 'Noto Sans Tamil', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    background-color: #ffffff;
    font-size: 13px;
    padding: 0;
    margin: 0;
  }}

  h1 {{
    color: #065f46;
    font-size: 22px;
    font-weight: 800;
    border-bottom: 3px solid #10b981;
    padding-bottom: 6px;
    margin-top: 15px;
    margin-bottom: 12px;
  }}

  h2 {{
    color: #0f766e;
    font-size: 17px;
    font-weight: 700;
    border-bottom: 1.5px solid #ccfbf1;
    padding-bottom: 5px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }}

  h3 {{
    color: #115e59;
    font-size: 14px;
    font-weight: 700;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p, li {{
    color: #334155;
    font-size: 12.5px;
  }}

  ul, ol {{
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  code {{
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    background: #f1f5f9;
    color: #0f766e;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 11px;
  }}

  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 12px 14px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 11px;
    line-height: 1.4;
    margin: 10px 0;
    page-break-inside: avoid;
  }}

  pre code {{
    background: transparent;
    color: #38bdf8;
    padding: 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 11px;
    page-break-inside: avoid;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background-color: #0f766e;
    color: #ffffff;
    font-weight: 600;
  }}

  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  hr {{
    border: none;
    border-top: 2px solid #e2e8f0;
    margin: 20px 0;
  }}

  .header-box {{
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 1.5px solid #a7f3d0;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 18px;
  }}
</style>
</head>
<body>
<div class="header-box">
  <div style="font-size: 11px; font-weight: 700; color: #059669; text-transform: uppercase; letter-spacing: 1px;">FarmWise AI Platform Architecture</div>
  <div style="font-size: 20px; font-weight: 800; color: #064e3b; margin: 4px 0;">FarmWise AI — Technical & Agronomic Master Guide</div>
  <div style="font-size: 12px; color: #047857;">Bilingual Implementation Reference (English &amp; தமிழ்) &bull; Task 1 Campus Challenge</div>
</div>
{html_content}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("HTML written to:", html_path)

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
]

browser_exe = next((p for p in edge_paths if os.path.exists(p)), None)

if browser_exe:
    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        print(f"PDF successfully generated at: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    else:
        print("PDF failed to generate:", res.stderr)
else:
    print("No browser found.")
