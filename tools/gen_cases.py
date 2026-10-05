#!/usr/bin/env python3
"""Generate the case-study pages: cases/index.html and cases/<slug>.html.

Run from anywhere: python3 tools/gen_cases.py
cases/*.html are GENERATED - edit this generator, not the HTML.
Static output, no JS.
"""
import re
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "cases"
BASE = "https://cloverity.github.io/cases/"

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#222;background:#f5f5f5;display:flex;justify-content:center;padding:20px 10px}
.wrap{max-width:740px;width:100%;background:#fff;border-radius:12px;border:1px solid #ddd;overflow:hidden}
.nav{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;border-bottom:1px solid #ddd;background:#fff;flex-wrap:wrap;gap:8px}
.nav-logo{display:flex;align-items:center;gap:8px}
.nav-logo-icon{width:30px;height:30px;border-radius:6px;background:#333;display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;font-weight:700}
.nav-logo span{font-weight:700;font-size:14px}
.nav-btn{padding:5px 10px;font-size:11px;border-radius:5px;color:#333;text-decoration:none}
a.nav-btn:hover{background:#f0f0f0}
.nav-btn.active{background:#eee;font-weight:600}
.sec{padding:44px 24px;border-bottom:1px solid #eee}
.sec-alt{background:#fafafa}
h1.case-title{font-size:22px;font-weight:800;color:#111;margin:10px 0 8px;line-height:1.3}
h1.title,h2.title{font-size:18px;font-weight:700;margin-bottom:6px;color:#111}
h3.stitle{font-size:14px;font-weight:700;margin-bottom:4px;color:#222}
.sub{font-size:12px;color:#888;margin-bottom:20px;line-height:1.6}
.lead{font-size:13px;color:#444;line-height:1.7}
.text{font-size:13px;color:#444;line-height:1.7}
.text+.text{margin-top:10px}
.card{background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:18px}
.card+.card{margin-top:12px}
a.card{display:block;color:inherit;text-decoration:none}
a.card:hover{border-color:#bbb}
.badge{display:inline-block;padding:4px 10px;border-radius:4px;background:#f0f0f0;font-size:10px;font-weight:600;color:#555}
.pills{display:flex;flex-wrap:wrap;gap:6px}
.pill{padding:5px 12px;border-radius:20px;background:#f0f0f0;font-size:11px;font-weight:500;color:#444;display:inline-block}
ul.built{list-style:none}
ul.built li{font-size:13px;color:#444;line-height:1.6;padding:8px 0 8px 18px;border-bottom:1px solid #f0f0f0;position:relative}
ul.built li:last-child{border-bottom:none}
ul.built li::before{content:"";position:absolute;left:2px;top:15px;width:6px;height:6px;border-radius:50%;background:#333}
.results{display:flex;flex-direction:column;gap:10px}
.result{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px}
.result-tag{font-size:12px;color:#333;font-weight:600;padding:6px 10px;background:#eafbe7;border-radius:4px;display:inline-block}
.basis{font-size:11px;color:#888}
.note{font-size:12px;color:#555;line-height:1.6;margin-top:14px;padding:10px 12px;background:#fff8e6;border-radius:6px}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.img-ph{width:100%;height:180px;background:#ebebeb;border:2px dashed #c0c0c0;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:4px}
.img-ph strong{font-size:12px;color:#888}
.img-ph span{font-size:10px;color:#aaa}
.more{display:inline-block;margin-top:12px;font-size:12px;font-weight:600;color:#333}
.footer{padding:20px 24px;font-size:10px;color:#bbb}
@media(max-width:600px){
  .grid2{grid-template-columns:1fr}
  .nav{flex-direction:column;align-items:flex-start}
  .sec{padding:28px 16px}
  h1.case-title{font-size:19px}
}
""".strip()

LOGO = ('<div class="nav-logo"><div class="nav-logo-icon">C</div>'
        '<span>Cloverity</span></div>')
FOOTER = '<div class="footer">© 2026 Cloverity Software</div>'


def head(title, desc, url, og_type):
    if len(desc) > 160:
        raise SystemExit(f"meta description too long ({len(desc)} > 160): {title}")
    t, d = escape(title), escape(desc)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">
<meta name="robots" content="index, follow">
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
"""


def pills(items):
    return '<div class="pills">' + "".join(
        f'<span class="pill">{escape(i)}</span>' for i in items) + "</div>"


CASES = [
    dict(
        slug="tender-rfp-platform",
        name="AI tender-document analysis platform",
        badge="Client delivery · production SaaS",
        desc=("AI SaaS that scores tender responses and recommends improvements. "
              "Review time cut from 3 days to 15 minutes, measured on the project."),
        summary="Scorecards and improvement recommendations for tender responses; review time 3 days → 15 minutes (measured on the project).",
        lead="Full-stack engineering for an Irish construction-tech company: an AI-powered SaaS that analyses tender responses.",
        problem=[
            "A bid team needs to see where a tender response is weak before it is submitted.",
            "The platform analyses a tender response and produces a scorecard with improvement "
            "recommendations.",
        ],
        built=[
            "Tender-analysis pipeline — LLM-based analysis of a tender response that produces a scorecard and improvement recommendations.",
            "Data layer — PostgreSQL with the pgvector extension for vector search.",
            "LLM layer on the Claude API, including a migration of the analysis pipeline from a previous model provider to Claude.",
            "Web application — Next.js frontend with dashboard and scorecard views; FastAPI backend.",
            "Subscription billing — Stripe hosted Checkout with a free / paid tier model and per-user report limits.",
            "Cloud deployment and operations — GCP Cloud Run, Cloud SQL and Cloud Storage; error monitoring with Sentry; ongoing production support.",
        ],
        stack=["Python", "FastAPI", "Next.js", "PostgreSQL + pgvector", "Claude API",
               "GCP Cloud Run", "Cloud SQL", "Cloud Storage", "Stripe hosted Checkout", "Sentry"],
        results=[
            ("Tender review time: 3 days → 15 minutes", "measured on the project"),
            ("In production", "the platform is live"),
        ],
        note=None,
        shots=["Scorecard view", "Improvement recommendations"],
        role=[
            "Full-stack engineering, end to end — backend, frontend, data layer, LLM pipeline, billing and "
            "cloud deployment, plus ongoing production support.",
            "The product belongs to the client; Cloverity provides the engineering.",
        ],
    ),
    dict(
        slug="sec-filing-extraction",
        name="Financial-statement extraction from SEC filings",
        badge="Client delivery · proof-of-concept",
        desc=("Extraction of all 5 financial-statement types from SEC 10-K / 10-Q filings to Excel. "
              "Up to 98% accuracy, measured on the project."),
        summary="All 5 financial-statement types from 10-K / 10-Q filings to Excel; up to 98% accuracy (measured on the project).",
        lead="A ~3-month proof-of-concept that turns SEC 10-K and 10-Q filings into structured financial statements.",
        problem=[
            "We worked with a client that needed structured financial statements from SEC 10-K / 10-Q filings.",
            "All five financial-statement types had to be extracted from each filing and delivered as "
            "Excel spreadsheets.",
        ],
        built=[
            "Extraction engine for text-based PDF filings, built on pdfplumber — covers all 5 financial-statement types in 10-K / 10-Q filings.",
            "FastAPI backend exposing the extraction workflow.",
            "Excel export pipeline — extracted statements delivered as spreadsheets.",
            "Working PoC delivered at the end of a ~3-month engagement.",
        ],
        stack=["Python", "FastAPI", "pdfplumber", "Excel export"],
        results=[
            ("High extraction accuracy (up to 98%)", "measured on the project"),
            ("All 5 financial-statement types extracted from 10-K / 10-Q filings", "delivered in the PoC"),
        ],
        note=None,
        shots=["Extracted statement", "Excel export"],
        role=[
            "Designed and built the extraction engine, the backend and the Excel export pipeline, and "
            "delivered the working PoC.",
        ],
    ),
    dict(
        slug="llm-gateway-finops",
        name="LLM gateway with cost controls (R&D)",
        badge="R&D · proof-of-concept",
        desc=("R&D PoC: a cost-and-usage control layer in front of AWS Bedrock. Under 1% budget "
              "overshoot and ~+2s latency overhead, measured in the PoC."),
        summary="Per-key and per-team budgets for LLM usage on AWS Bedrock; under 1% budget overshoot in the PoC.",
        lead="An R&D proof-of-concept Cloverity ran, offered as a capability: LLM cost governance without blocking developers.",
        problem=[
            "Problem we set out to solve in R&D: in an engineering org with many teams on AWS Bedrock, LLM spend is hard to govern — budgets are not "
            "enforced per team or per key, and cost, token and latency data is scattered.",
            "We built and validated a cost-and-usage control layer that sits in front of Bedrock and keeps "
            "developers unblocked.",
        ],
        built=[
            "Gateway on LiteLLM Proxy + PostgreSQL + Langfuse, containerised with Docker Compose.",
            "Per-key spending limits, verified against real budgets.",
            "Per-team budgets with a hard cut-off — when a team exhausts its budget, all of its keys stop at once.",
            "Latency characterised, with guidance on when to route through the gateway and when to call Bedrock directly.",
            "Accurate token counting for streaming responses confirmed.",
            "Real IDE clients integrated and tested — Claude Code CLI, VS Code extension, Continue.dev.",
            "Full observability in Langfuse — cost, tokens and latency per call.",
            "PoC report with findings and production recommendations.",
        ],
        stack=["LiteLLM Proxy", "AWS Bedrock (Claude Haiku / Sonnet)", "PostgreSQL", "Langfuse",
               "Docker Compose", "Python", "IAM", "Continue.dev", "Claude Code CLI"],
        results=[
            ("< 1% budget overshoot with per-key limits", "measured in our R&D PoC on real budgets"),
            ("~+2s latency overhead from the proxy", "measured in our R&D PoC"),
        ],
        note="This is R&D Cloverity ran to prove the approach — not a system running in production for a client.",
        shots=["Langfuse cost / token view", "Budget cut-off in action"],
        role=[
            "Designed, built and ran the R&D PoC end to end — architecture, setup, IDE client testing, "
            "measurements and the PoC report.",
        ],
    ),
    dict(
        slug="legacy-php-to-python",
        name="Legacy PHP → Python migration (R&D)",
        badge="R&D · applied-AI engineering",
        desc=("R&D: AI-agent-assisted legacy PHP → Python + React migration. 11 of 14 units (79%), "
              "918+ passing tests, API kept stable — measured in our R&D project."),
        summary="AI-agent-assisted migration to FastAPI + React; 11 of 14 units (79%) migrated with 918+ tests (R&D project, partial).",
        lead="An R&D project Cloverity ran to prove a risk-controlled, AI-agent-assisted method for legacy modernisation.",
        problem=[
            "Legacy PHP applications are hard to change safely: fixing one file tends to break ten others, and a "
            "big-bang rewrite is too risky.",
            "We tested an AI-agent-assisted migration method on Tiny Tiny RSS, an open-source legacy PHP "
            "application, moving it to Python (FastAPI) + React/TypeScript while keeping its public API stable "
            "so existing API clients keep working.",
        ],
        built=[
            "Code map → ordered units: mapped the PHP codebase and split it into 14 ordered units, avoiding the \"fix one file, break ten\" cascade.",
            "Migrated 11 of 14 units with passing tests and clean linting.",
            "Clean separation: all rendering in React; the Python backend returns JSON only.",
            "Libraries over bespoke code wherever possible — e.g. a large legacy search client replaced by a thin wrapper.",
            "Largest function decomposed into small, testable async parts.",
            "Data layer rebuilt: raw SQL → async SQLAlchemy.",
            "2FA (OTP / TOTP) reimplemented and verified against test vectors.",
            "Living migration report and a stakeholder demo deck.",
        ],
        stack=["Python 3.12", "FastAPI", "SQLAlchemy (async) + Alembic", "Pydantic", "httpx", "pytest",
               "flake8", "mypy", "React + TypeScript + Vite", "NetworkX / Leiden", "ast-grep", "PostgreSQL",
               "bleach / feedgen / langdetect", "Claude Code (AI agents)"],
        results=[
            ("11 of 14 units migrated (79%)", "measured in our R&D project — partial migration"),
            ("918+ passing tests", "measured in our R&D project"),
            ("1,691-line search client → 15-line wrapper", "measured in our R&D project"),
            ("948-line function → 5 testable async parts", "measured in our R&D project"),
            ("576+ redundant DB calls removed", "measured in our R&D project"),
            ("2FA verified against 67 test vectors", "measured in our R&D project"),
        ],
        note=("The migration is partial: 11 of 14 units are done. The project demonstrates the method; "
              "it is not a finished product migration."),
        shots=["Unit dependency map", "Migrated React UI"],
        role=[
            "Designed and ran the AI-agent-assisted migration as Cloverity R&D — code mapping and unit "
            "ordering, migration with Claude Code agents under human direction, tests and the migration report.",
        ],
    ),
]


CLIENT_SLUGS = {"tender-rfp-platform", "sec-filing-extraction"}


def case_page(c):
    url = BASE + c["slug"] + ".html"
    title = f'{c["name"]} — Cloverity case study'
    h = head(title, c["desc"], url, "article")
    nav = f'<div class="nav">{LOGO}<a class="nav-btn" href="index.html">All cases</a></div>\n'
    intro = (f'<div class="sec"><span class="badge">{escape(c["badge"])}</span>'
             f'<h1 class="case-title">{escape(c["name"])}</h1>'
             f'<p class="lead">{escape(c["lead"])}</p></div>\n')
    problem = ('<div class="sec sec-alt"><h2 class="title">Problem</h2>'
               + "".join(f'<p class="text">{escape(p)}</p>' for p in c["problem"]) + "</div>\n")
    built = ('<div class="sec"><h2 class="title">What we built</h2><ul class="built">'
             + "".join(f"<li>{escape(b)}</li>" for b in c["built"]) + "</ul></div>\n")
    stack = ('<div class="sec sec-alt"><h2 class="title">Stack</h2>' + pills(c["stack"]) + "</div>\n")
    res = "".join(
        f'<div class="result"><span class="result-tag">{escape(v)}</span>'
        f'<span class="basis">— {escape(b)}</span></div>' for v, b in c["results"])
    note = f'<p class="note">{escape(c["note"])}</p>' if c["note"] else ""
    results = ('<div class="sec"><h2 class="title">Results</h2>'
               '<p class="sub">Each figure is shown with its basis.</p>'
               f'<div class="results">{res}</div>{note}</div>\n')
    if c["slug"] in CLIENT_SLUGS:
        shots_sub = "Screenshots omitted to protect client confidentiality."
        shots_ph = "Screenshot omitted"
    else:
        shots_sub = "Placeholders — real screenshots are being prepared."
        shots_ph = "Screenshot coming soon"
    shots = ('<div class="sec sec-alt"><h2 class="title">Screenshots</h2>'
             f'<p class="sub">{shots_sub}</p>'
             + ("" if c["slug"] in CLIENT_SLUGS else '<div class="grid2">'
                + "".join(f'<div class="img-ph"><strong>{shots_ph}</strong>'
                          f'<span>{escape(s)}</span></div>' for s in c["shots"]) + "</div>")
             + "</div>\n")
    role = ('<div class="sec"><h2 class="title">Role</h2>'
            + "".join(f'<p class="text">{escape(p)}</p>' for p in c["role"]) + "</div>\n")
    return h + nav + intro + problem + built + stack + results + shots + role + FOOTER + "\n</div>\n</body>\n</html>\n"


def index_page():
    desc = ("Selected Cloverity case studies: AI document analysis, SEC filing extraction, "
            "LLM cost controls and AI-assisted legacy migration.")
    h = head("Case studies — Cloverity", desc, BASE + "index.html", "website")
    nav = f'<div class="nav">{LOGO}<span class="nav-btn active" aria-current="page">All cases</span></div>\n'
    intro = ('<div class="sec"><h1 class="title">Case studies</h1>'
             '<p class="sub">Selected work by Cloverity Software — client deliveries and R&amp;D projects, '
             'each with the figures we can back up.</p>\n')
    cards = ""
    for c in CASES:
        cards += (f'<a class="card" href="{c["slug"]}.html"><span class="badge">{escape(c["badge"])}</span>'
                  f'<h3 class="stitle" style="margin-top:10px">{escape(c["name"])}</h3>'
                  f'<p class="sub" style="margin-bottom:12px">{escape(c["summary"])}</p>'
                  + pills(c["stack"][:5]) + '<span class="more">Read the case →</span></a>\n')
    return h + nav + intro + cards + "</div>\n" + FOOTER + "\n</div>\n</body>\n</html>\n"


if __name__ == "__main__":
    for c in CASES:
        if not re.fullmatch(r"[a-z0-9-]+", c["slug"]):
            raise SystemExit(f'invalid slug {c["slug"]!r}: must match ^[a-z0-9-]+$')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(index_page(), encoding="utf-8", newline="\n")
    for c in CASES:
        (OUT / f'{c["slug"]}.html').write_text(case_page(c), encoding="utf-8", newline="\n")
    print("ok")
