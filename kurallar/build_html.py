# -*- coding: utf-8 -*-
"""KURALLAR.md -> kurallar.html

Kullanım:  python kurallar/build_html.py
Kural dosyası her değiştiğinde çalıştırılır. Stok fotoğrafları photos/temiz
altından okunur ve HTML'e WebP olarak gömülür (dosya yoluna bağlanmaz).
"""
import base64
import html
import io
import re
from datetime import datetime
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = HERE / "KURALLAR.md"
OUT = HERE / "kurallar.html"
PHOTOS = ROOT / "photos" / "temiz"

CODE_RE = re.compile(r"^(?:10 \d{5}|LV\d{6}|CP1W-\d+EDT1)$")
RULE_CLS = 'class="rule'
RULE_RE = re.compile(r"^\*\*((?:R\d+\.\d+[a-z]?|Q\d+))(.*?)\*\*\s*(?:—\s*)?")

_thumbs = {}


def thumb(code):
    if code in _thumbs:
        return _thumbs[code]
    p = PHOTOS / f"{code}.png"
    uri = None
    if p.exists():
        im = Image.open(p).convert("RGBA")
        im.thumbnail((112, 112), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=75)
        uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    _thumbs[code] = uri
    return uri


def chip(code):
    has = thumb(code) is not None
    cls = "chip" + ("" if has else " nophoto")
    title = "" if has else ' title="Fotoğraf yok"'
    return f'<span class="{cls}" data-code="{code}"{title}>{code}</span>'


def inline(text):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`"):
            inner = part[1:-1]
            out.append(chip(inner) if CODE_RE.match(inner) else f"<code>{html.escape(inner)}</code>")
        else:
            s = html.escape(part, quote=False)
            s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
            s = s.replace("→", '<span class="arrow">→</span>')
            out.append(s)
    return "".join(out)


def cell(text):
    t = text.strip()
    if t == "STOK KODU YOK":
        return '<td><span class="nocode">STOK KODU YOK</span></td>'
    if CODE_RE.match(t):
        uri = thumb(t)
        img = f'<img src="{uri}" alt="">' if uri else '<span class="noimg">—</span>'
        return f'<td class="codecell"><div class="cc">{img}{chip(t)}</div></td>'
    return f"<td>{inline(t)}</td>"


def render_li(text):
    m = RULE_RE.match(text)
    if not m:
        return f"<li>{inline(text)}</li>"
    rid, label = m.group(1), m.group(2).strip()
    rest = text[m.end():]
    kind = "q" if rid.startswith("Q") else "r"
    lab = f'<span class="rlabel">{inline(label)}</span>' if label else ""
    return (f'<li class="rule {kind}" id="{rid}"><a class="rid" href="#{rid}">{rid}</a>'
            f'<div class="rbody">{lab}{inline(rest)}</div></li>')


CALLOUT = {"SOR": ("ask", "Sor"), "NOT": ("note", "Not"),
           "UYARI": ("warn", "Dikkat"), "ORNEK": ("ex", "Örnek")}


def parse(md):
    lines = md.splitlines()
    title, intro, sections = "", [], []
    cur = None
    buf = []  # html parts of current section
    i = 0

    def flush_section():
        if cur is not None:
            cur["html"] = "\n".join(buf)
            sections.append(cur)

    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# "):
            title = ln[2:].strip()
            i += 1
            continue
        if ln.startswith("## "):
            flush_section()
            h = ln[3:].strip()
            m = re.match(r"(\d+)\.\s*(.*)", h)
            num, name = (m.group(1), m.group(2)) if m else ("", h)
            cur = {"num": num, "name": name, "id": f"s{num or len(sections)}"}
            buf = []
            i += 1
            continue
        target = buf if cur is not None else intro
        if ln.startswith("### "):
            target.append(f"<h3>{inline(ln[4:].strip())}</h3>")
            i += 1
        elif ln.startswith(">"):
            block = []
            while i < len(lines) and lines[i].startswith(">"):
                block.append(lines[i].lstrip(">").strip())
                i += 1
            kind, label = "note", "Not"
            m = re.match(r"\[!(\w+)\]", block[0]) if block else None
            if m:
                kind, label = CALLOUT.get(m.group(1), ("note", m.group(1)))
                block = block[1:]
            body = "".join(f"<p>{inline(b)}</p>" for b in block if b)
            target.append(f'<div class="callout {kind}"><div class="ctag">{label}</div>{body}</div>')
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not re.match(r"^\s*-+\s*$", r[0])]
            th = "".join(f"<th>{inline(c.strip())}</th>" for c in head)
            tb = "".join("<tr>" + "".join(cell(c) for c in r) + "</tr>" for r in body)
            tw = "tw narrow" if len(head) <= 2 else "tw"
            target.append(f'<div class="{tw}"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>')
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(render_li(lines[i][2:].strip()))
                i += 1
            target.append("<ul>" + "".join(items) + "</ul>")
        elif ln.strip():
            target.append(f"<p>{inline(ln.strip())}</p>")
            i += 1
        else:
            i += 1
    flush_section()
    return title, intro, sections


CSS = r"""
:root{--bg:#f6f5f2;--panel:#fff;--ink:#1d2228;--mute:#68707a;--line:#e3e1dc;--accent:#c2410c;--accent-soft:#fff1e8;
--blue:#1d4ed8;--blue-soft:#e8efff;--ask:#7c3aed;--ask-soft:#f3edff;--warn:#b45309;--warn-soft:#fff6e0;--ok:#047857;--ok-soft:#e6f6ef;
--chip:#eef0f3;--chip-ink:#2b3440;--shadow:0 1px 2px rgba(0,0,0,.04),0 4px 14px rgba(0,0,0,.05)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121417;--panel:#1a1d21;--ink:#e7e9ec;--mute:#9aa3ad;--line:#2b3036;
--accent:#fb923c;--accent-soft:#2d1d12;--blue:#8fb0ff;--blue-soft:#1a2440;--ask:#b79cff;--ask-soft:#241c3a;--warn:#f5b54a;--warn-soft:#2d2412;
--ok:#4ade80;--ok-soft:#12291e;--chip:#252a30;--chip-ink:#d5dae0;--shadow:none}}
:root[data-theme="dark"]{--bg:#121417;--panel:#1a1d21;--ink:#e7e9ec;--mute:#9aa3ad;--line:#2b3036;--accent:#fb923c;--accent-soft:#2d1d12;
--blue:#8fb0ff;--blue-soft:#1a2440;--ask:#b79cff;--ask-soft:#241c3a;--warn:#f5b54a;--warn-soft:#2d2412;--ok:#4ade80;--ok-soft:#12291e;
--chip:#252a30;--chip-ink:#d5dae0;--shadow:none}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Segoe UI",system-ui,-apple-system,sans-serif}
header{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hbar{max-width:1280px;margin:0 auto;padding:12px 20px;display:flex;gap:16px;align-items:center}
.logo{width:34px;height:34px;border-radius:8px;background:var(--accent);display:grid;place-items:center;color:#fff;flex:none}
.htitle{font-weight:650;font-size:16px;line-height:1.2}.hsub{font-size:12px;color:var(--mute)}
.search{margin-left:auto;display:flex;gap:8px;align-items:center}
.search input{width:260px;max-width:40vw;padding:8px 12px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink);font:inherit}
.tbtn{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:7px 10px;cursor:pointer;font:inherit}
.plink{text-decoration:none;white-space:nowrap;background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.plink:hover{filter:brightness(1.08)}
.wrap{max-width:1280px;margin:0 auto;padding:20px;display:grid;grid-template-columns:240px 1fr;gap:28px}
nav{position:sticky;top:76px;align-self:start;max-height:calc(100vh - 96px);overflow:auto}
nav a{display:flex;justify-content:space-between;gap:8px;padding:6px 10px;border-radius:7px;color:var(--ink);text-decoration:none;font-size:14px}
nav a:hover{background:var(--chip)}nav a.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
nav .n{color:var(--mute);font-variant-numeric:tabular-nums;font-size:12px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
.stat b{display:block;font-size:26px;line-height:1.1;font-variant-numeric:tabular-nums}.stat span{font-size:12px;color:var(--mute)}
.stat.q b{color:var(--warn)}
.intro{color:var(--mute);margin-bottom:8px}.intro p{margin:4px 0}
section{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin-bottom:18px;box-shadow:var(--shadow)}
section h2{margin:0 0 12px;font-size:19px;display:flex;align-items:center;gap:10px}
section h2 .sn{width:28px;height:28px;border-radius:7px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-size:14px;flex:none}
section h3{font-size:14px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);margin:20px 0 8px}
ul{list-style:none;padding:0;margin:0}
li{padding:6px 0}
li.rule{display:grid;grid-template-columns:62px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--line)}
li.rule:first-child{border-top:0}
.rid{font:600 12px/1 ui-monospace,Consolas,monospace;color:var(--blue);background:var(--blue-soft);border-radius:6px;padding:5px 0;text-align:center;text-decoration:none;height:max-content;margin-top:2px}
li.q .rid{color:var(--warn);background:var(--warn-soft)}
li.rule:target{background:var(--accent-soft);border-radius:8px}
.rlabel{font-weight:650;margin-right:6px}.rlabel::after{content:" —";color:var(--mute);font-weight:400}
code{font:13px ui-monospace,Consolas,monospace;background:var(--chip);padding:1px 6px;border-radius:5px}
.chip{display:inline-block;font:600 12px/1.4 ui-monospace,Consolas,monospace;background:var(--chip);color:var(--chip-ink);border:1px solid var(--line);
padding:0 6px;border-radius:5px;white-space:nowrap;cursor:default}
.chip.nophoto{border-style:dashed}
.nocode{font:600 11px/1.4 ui-monospace,Consolas,monospace;color:var(--warn);background:var(--warn-soft);padding:2px 6px;border-radius:5px;white-space:nowrap}
.arrow{color:var(--accent);font-weight:700}
.callout{border-radius:10px;padding:12px 14px 12px 14px;margin:6px 0 12px;border-left:4px solid}
.callout p{margin:3px 0}.ctag{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px}
.callout.ask{background:var(--ask-soft);border-color:var(--ask)}.callout.ask .ctag{color:var(--ask)}
.callout.note{background:var(--blue-soft);border-color:var(--blue)}.callout.note .ctag{color:var(--blue)}
.callout.warn{background:var(--warn-soft);border-color:var(--warn)}.callout.warn .ctag{color:var(--warn)}
.callout.ex{background:var(--ok-soft);border-color:var(--ok)}.callout.ex .ctag{color:var(--ok)}
.tw.narrow{max-width:360px}
.tw{overflow-x:auto;margin:6px 0 10px;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{text-align:center;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mute);background:var(--chip);padding:8px 10px;font-weight:600}
td{padding:7px 10px;border-top:1px solid var(--line);vertical-align:middle}
tr:hover td{background:color-mix(in srgb,var(--accent-soft) 50%,transparent)}
td.codecell{width:150px}.cc{display:flex;align-items:center;gap:10px}
.cc img{width:44px;height:44px;object-fit:contain;flex:none}
.noimg{width:44px;text-align:center;color:var(--mute);flex:none}
#pop{position:fixed;pointer-events:none;z-index:50;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:8px;box-shadow:0 8px 30px rgba(0,0,0,.18);display:none}
#pop img{width:112px;height:112px;object-fit:contain;display:block}
.hide{display:none!important}
footer{color:var(--mute);font-size:12px;text-align:center;padding:10px 0 30px}
@media (max-width:860px){.wrap{grid-template-columns:1fr;padding:16px}nav{display:none}.stats{grid-template-columns:repeat(2,1fr)}
.hbar{flex-wrap:wrap;padding:10px 16px}.search{margin-left:0;width:100%}.search input{flex:1;max-width:none}section{padding:16px}
li.rule{grid-template-columns:54px 1fr}}
"""

JS = r"""
const q=document.getElementById('q');
q.addEventListener('input',()=>{const v=q.value.trim().toLocaleLowerCase('tr');
document.querySelectorAll('section').forEach(s=>{let any=false;
s.querySelectorAll('li,tbody tr').forEach(e=>{const m=!v||e.textContent.toLocaleLowerCase('tr').includes(v);e.classList.toggle('hide',!m);if(m)any=true});
const head=s.querySelector('h2').textContent.toLocaleLowerCase('tr').includes(v);
if(head&&v)s.querySelectorAll('.hide').forEach(e=>e.classList.remove('hide'));
s.classList.toggle('hide',!!v&&!any&&!head)})});
const pop=document.getElementById('pop');
document.addEventListener('mouseover',e=>{const c=e.target.closest('.chip');if(!c||!PH[c.dataset.code]){pop.style.display='none';return}
pop.innerHTML='<img src="'+PH[c.dataset.code]+'">';pop.style.display='block'});
document.addEventListener('mousemove',e=>{if(pop.style.display==='block'){pop.style.left=Math.min(e.clientX+14,innerWidth-140)+'px';pop.style.top=(e.clientY+14)+'px'}});
const links=[...document.querySelectorAll('nav a')];
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+en.target.id))}}),{rootMargin:'-80px 0px -70% 0px'});
document.querySelectorAll('section').forEach(s=>io.observe(s));
const tb=document.getElementById('theme');
tb.onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('kt',r.dataset.theme)}catch(e){}};
try{const t=localStorage.getItem('kt');if(t)document.documentElement.dataset.theme=t}catch(e){}
"""


def build():
    md = SRC.read_text(encoding="utf-8")
    title, intro, sections = parse(md)

    n_rules = len(re.findall(r"^- \*\*R\d+\.\d+", md, re.M))
    n_q = len(re.findall(r"^- \*\*Q\d+", md, re.M))
    codes = sorted(set(re.findall(r"\b10 \d{5}\b|\bLV\d{6}\b|\bCP1W-\d+EDT1\b", md)))
    n_photo = sum(1 for c in codes if thumb(c))

    nav = "".join(
        f'<a href="#{s["id"]}"><span>{s["num"]}. {html.escape(s["name"])}</span>'
        f'<span class="n">{s["html"].count(RULE_CLS) or s["html"].count("<tr>") - s["html"].count("<thead>")}</span></a>' for s in sections)
    secs = "".join(
        f'<section id="{s["id"]}"><h2><span class="sn">{s["num"]}</span>{html.escape(s["name"])}</h2>{s["html"]}</section>'
        for s in sections)
    stats = (f'<div class="stats"><div class="stat"><b>{n_rules}</b><span>Kural</span></div>'
             f'<div class="stat"><b>{len(codes)}</b><span>Stok kodu / ref</span></div>'
             f'<div class="stat"><b>{n_photo}/{len(codes)}</b><span>Fotoğrafı olan</span></div>'
             f'<div class="stat q"><b>{n_q}</b><span>Açık soru</span></div></div>')
    ph = "{" + ",".join(f'"{c}":"{thumb(c)}"' for c in codes if thumb(c)) + "}"
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    page = f"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pano Malzeme Kuralları</title><style>{CSS}</style></head>
<body>
<header><div class="hbar">
<div class="logo"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg></div>
<div><div class="htitle">{html.escape(title)}</div><div class="hsub">kurallar/KURALLAR.md · üretildi {stamp}</div></div>
<div class="search"><input id="q" type="search" placeholder="Ara: kural, malzeme, stok kodu…"><a class="tbtn plink" href="panolar.html">Pano modelleri →</a><button class="tbtn" id="theme" title="Tema">◐</button></div>
</div></header>
<div class="wrap">
<nav>{nav}</nav>
<main>{stats}<div class="intro">{"".join(intro)}</div>{secs}</main>
</div>
<footer>Kaynak: kurallar/KURALLAR.md — değiştirince <code>python kurallar/build_html.py</code></footer>
<div id="pop"></div>
<script>const PH={ph};{JS}</script>
</body></html>"""
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.name}: {n_rules} kural, {len(codes)} kod ({n_photo} fotolu), {n_q} açık soru")


if __name__ == "__main__":
    build()
