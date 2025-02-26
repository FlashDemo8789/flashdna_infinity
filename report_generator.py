import pdfkit
import datetime

def generate_investor_report(doc: dict, system_dyn=None, sir_data=None, hpc_data=None, patterns_matched=None):
    now= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name= doc.get("name","Unknown")
    sp= doc.get("success_prob",50.0)
    intangible= doc.get("intangible",50.0)
    team= doc.get("team_score",0.0)
    moat= doc.get("moat_score",0.0)
    final_score= doc.get("flashdna_score",sp)

    pat_html= ""
    if patterns_matched:
        pat_html= "<ul>"
        for p in patterns_matched:
            pat_html+= f"<li>{p}</li>"
        pat_html+= "</ul>"
    else:
        pat_html= "<p>No numeric patterns matched.</p>"

    html= f"""
<html>
<head><meta charset='utf-8'/><title>FlashDNA Infinity Report</title></head>
<body style='font-family:Arial; margin:20px;'>
<h1>FlashDNA Infinity - Investor Report</h1>
<p><strong>Startup:</strong> {name} | Generated: {now}</p>

<h2>1. Executive Overview</h2>
<ul>
  <li><strong>FlashDNA Score</strong>: {final_score:.2f}</li>
  <li><strong>Success Probability (XGBoost)</strong>: {sp:.2f}%</li>
  <li><strong>Intangible (LLM, DeepSeek-70B)</strong>: {intangible:.2f}</li>
  <li><strong>Team Depth</strong>: {team:.2f}</li>
  <li><strong>Moat Score</strong>: {moat:.2f}</li>
</ul>

<h3>Numeric Patterns Matched</h3>
{pat_html}

<h2>2. System Dynamics & SIR</h2>
"""
    if system_dyn:
        html+= f"<p>System Dynamics final user => {system_dyn[-1]:.1f}</p>"
    if sir_data:
        S,I,R= sir_data
        html+= f"<p>SIR final infected => {I[-1]:.1f}, recovered => {R[-1]:.1f}</p>"

    html+= "<h2>3. HPC Scenario</h2>"
    if hpc_data:
        html+= "<ul>"
        for c in hpc_data[:5]:
            html+= f"<li>Churn={c['churn']:.2f}, Referral={c['referral']:.2f} => final {c['final_users']:.1f}</li>"
        html+= "</ul>"
    else:
        html+= "<p>No HPC data found??</p>"

    html+= """
</body>
</html>
"""
    pdf_data= pdfkit.from_string(html, False, options={"page-size":"A4"})
    return pdf_data