# -*- coding: utf-8 -*-
"""KURALLAR.md + model tanımları -> panolar.html

Kullanım:  python kurallar/build_panolar.py
Malzeme adları, kural metinleri ve fotoğraflar KURALLAR.md / photos/temiz'den
okunur. Bu dosyada yalnız model yapısı (etiket yerleşimi, standart kalemler,
opsiyonlar) durur; kural değişince buradaki ilgili model de güncellenir.
"""
import html
import json
import re
from datetime import datetime

import build_html as bh

OUT = bh.HERE / "panolar.html"

# ---------------------------------------------------------------------------
# Etiket bileşenleri: t = estop | btn | lamp | twin | sel | mandal | disp | hmi
#                         | pako | tms | tapaB | tapaL
# kb = [NO, NC] kontak blok; opt = yalnız bu opsiyon açıkken; off = opsiyon kapalıyken yerine
# ---------------------------------------------------------------------------
TAPA_B = {"t": "tapaB", "l": "TAPA"}
TAPA_L = {"t": "tapaL", "l": "TAPA"}

MODELS = [
    {
        "id": "kbn1b",
        "name": "KBN 1B",
        "tag": "Manuel pano · ORDEL",
        "desc": "Termokupl kontrollü manuel yıkama makinesi panosu. Sepet redüktörü her zaman invertörle döner.",
        "facts": [
            ("Pano ölçüsü", "710 × 710 mm (standart)", "R7.1"),
            ("Ana kesme", "Pako şalter", "R1.2"),
            ("Güç kaynağı", "MDR 100/24", "R5.1"),
            ("Kaçak akım", "1 adet (tüm pano)", "R5.4"),
            ("IOF", "Yok", "R1.3"),
            ("Bara", "4×7 · 1 adet", "R5.10"),
            ("Motor düzeni", "Termik + kontaktör", "R3.3"),
            ("Etiket dili", "Almanca + İngilizce", "R14.1"),
        ],
        "label": {
            "brand": "KBN 1B",
            "rows": [
                [None, {"t": "disp", "l": "ORDEL", "code": "10 00229", "big": True}, None],
                [{"t": "lamp", "c": "white", "l": "YIKAMA", "code": "10 00279"}, None,
                 {"t": "lamp", "c": "white", "l": "ISITICI", "code": "10 00279"}],
                [{"t": "btn", "c": "blue", "l": "RESET", "code": "10 00272", "kb": [1, 1]},
                 {"t": "estop", "l": "ACİL STOP", "code": "10 03445", "kb": [0, 2]},
                 {"t": "btn", "c": "white", "l": "SEPET TEST", "code": "10 00270", "kb": [1, 0]}],
                [{"t": "mandal", "l": "YAĞ SIYIRICI", "code": "10 00262", "kb": [1, 0], "opt": "yag", "off": TAPA_B},
                 None,
                 {"t": "lamp", "c": "white", "l": "YAĞ SIYIRICI", "code": "10 00279", "opt": "yag", "off": TAPA_L}],
                [{"t": "lamp", "c": "red", "l": "DÜŞÜK SU", "code": "10 00278"},
                 {"t": "lamp", "c": "red", "l": "POMPA ARIZA", "code": "10 00278"},
                 {"t": "lamp", "c": "red", "l": "REDÜKTÖR ARIZA", "code": "10 00278"}],
                "CIFT_EL",
            ],
            "note": "Şematik yerleşim. ORDEL olduğu için START/STOP yok; yerine YIKAMA ve ISITICI beyaz lambaları var (R7.6).",
        },
        "cift_el": True,
        "standard": [
            {"series": "Pako şalter", "photo": "10 00287", "choices": "3×25 · 3×40 · 3×63 A", "note": "Tablo akımına göre en küçük", "rule": "R5.6"},
            {"series": "Kaçak akım 4P", "photo": "10 00304", "choices": "25 · 40 · 63 · 80 · 100 A", "note": "Tüm pano için 1 adet", "rule": "R5.4"},
            {"series": "Aşırı akım koruma 4P", "photo": "10 02664", "choices": "25 · 40 · 63 A", "note": "Tüm pano için 1 adet", "rule": "R5.5"},
            {"code": "10 02772", "qty": 1, "rule": "R5.1"},
            {"code": "10 00258", "qty": 1, "rule": "R5.2"},
            {"code": "10 00302", "qty": 1, "note": "Kumanda", "rule": "R5.3"},
            {"code": "10 01421", "qty": 2, "note": "Sepet invertörü + pano lambası", "rule": "R4.1b"},
            {"code": "10 03253", "qty": 1, "rule": "R5.7"},
            {"code": "10 16235", "qty": 1, "note": "Pano lambası anahtarı", "rule": "R5.7"},
            {"code": "10 03313", "qty": 1, "rule": "R5.8"},
            {"code": "10 03578", "qty": 1, "note": "Motor grubu", "rule": "R5.10"},
            {"code": "10 00229", "qty": 1, "rule": "R7.5"},
            {"code": "10 16319", "qty": 1, "note": "Sepet redüktörü", "rule": "R4.1a"},
            {"code": "10 01398", "qty": 1, "rule": "R7.4"},
            {"code": "10 00294", "qty": 3, "note": "2 manuel + 1 sepet", "rule": "R7.4"},
            {"code": "10 00295", "qty": 4, "note": "3 manuel + 1 sepet (döner nozzle: 6)", "rule": "R7.4"},
            {"code": "10 01332", "qty": "ısıtıcı başına 1", "note": "Isıtıcı yalnız kontaktörle", "rule": "R4.3"},
        ],
        "loads": [
            ("Motor", "Termik + kontaktör, In'e göre", "R3.3"),
            ("Sepet redüktörü 0,37 kW", "İnvertör + 1×6 sigorta + 220V röle + soket", "R4.1"),
            ("Isıtıcı", "Yalnız LC1K1610M7; koruma girişteki sigortadan", "R4.3"),
            ("Sensör / termokupl", "Kontaktör, termik, MKŞ yok", "R4.5"),
        ],
        "options": [
            {"key": "yag", "title": "Yağ sıyırıcı", "rule": "R4.7a",
             "desc": "Termik + kontaktör ile sürülür. Etikete buton (sol) + lamba (sağ); yoksa tapa.",
             "items": [("10 00243", 1), ("10 02314", 1), ("10 00262", 1), ("10 00279", 1)], "kb": [0, 0]},
            {"key": "noz", "title": "Döner nozzle", "rule": "R7.4a",
             "desc": "Röle seti 6 sokete çıkar: +2 soket ve +2 röle (röle tipi açık soru Q17).",
             "items": [("10 00295", 2)], "kb": [0, 0]},
            {"key": "emn", "title": "Emniyet rölesi", "rule": "R1.6",
             "desc": "Her panoda sorulur. Kapak kapalı switchleri ve acil stop bu röleye bağlanır.",
             "items": [("10 04538", 1)], "kb": [0, 0]},
        ],
        "rules": ["R1.0", "R1.1", "R1.2", "R1.3", "R1.5", "R4.1", "R4.1a", "R4.1b", "R4.1c", "R4.1d", "R4.3",
                  "R4.7a", "R4.7c", "R5.1", "R5.2", "R5.4", "R5.6", "R5.10",
                  "R1.6", "R7.1", "R7.2", "R7.3", "R7.4", "R7.4a", "R7.5", "R7.6", "R7.7", "R7.8", "R7.9",
                  "R9.1", "R9.2", "R9.3", "R9.4", "R9.5", "R9.6a", "R9.7", "R14.1", "R14.4", "R14.5"],
    },
    {
        "id": "kbn2b",
        "name": "KBN 2B",
        "tag": "PLC'li pano · OMRON",
        "desc": "OMRON CP2E PLC ve NB7W ekranlı otomatik panosu. Ana kesme TMŞ, kaçak akımlar grup başına ve IOF'lu.",
        "facts": [
            ("Pano ölçüsü", "Her projede sorulur", "R1.1"),
            ("Ana kesme", "TMŞ + döner kol (kapakta) · aşırı akım yok", "R5.11"),
            ("Güç kaynağı", "LRS 350/24", "R5.1"),
            ("Kaçak akım", "Grup başına", "R5.4"),
            ("IOF", "Her kaçak akıma 1", "R1.3"),
            ("Bara", "4×7 + 2×7", "R5.10"),
            ("Isıtıcı", "Kontaktör + 3P 16 A", "R4.4"),
            ("Etiket dili", "Almanca + İngilizce", "R14.1"),
        ],
        "label": {
            "brand": "KBN 2B",
            "rows": [
                [None, {"t": "hmi", "l": "NB7W-TW01B", "code": "10 16496"}, None],
                [{"t": "btn", "c": "green", "l": "START", "code": "10 00273", "kb": [1, 1]},
                 {"t": "btn", "c": "blue", "l": "SIFIRLA", "code": "10 00272", "kb": [1, 1]},
                 {"t": "btn", "c": "red", "l": "STOP", "code": "10 00271", "kb": [1, 1]}],
                [None, {"t": "estop", "l": "ACİL STOP", "code": "10 03445", "kb": [0, 2]}, None],
                "CIFT_EL",
            ],
            "note": "Şematik yerleşim. Sepet test butonu yok (R8.1). Yağ sıyırıcı ekrandan kumanda edilir, etikette yok. TMŞ döner kolu etikette değil, pano kapağındadır (R14.7).",
        },
        "cift_el": True,
        "standard": [
            {"series": "TMŞ EasyPact CVS F 3P3D", "photo": "LV516332", "choices": "16 … 250 A (12 boy)", "note": "Tablo akımına göre en küçük In", "rule": "R5.11"},
            {"code": "LV429338", "qty": 1, "note": "TMŞ döner kolu", "rule": "R5.12"},
            {"series": "Kaçak akım 4P", "photo": "10 00304", "choices": "25 · 40 · 63 · 80 · 100 A", "note": "Grup başına 1", "rule": "R5.4"},
            {"code": "10 10820", "qty": "kaçak akım başına 1", "rule": "R1.3"},
            {"code": "10 04903", "qty": 1, "rule": "R5.1"},
            {"code": "10 01421", "qty": 2, "note": "LRS girişi + pano lambası", "rule": "R5.9"},
            {"code": "10 01422", "qty": 1, "note": "LRS çıkışı", "rule": "R5.9"},
            {"code": "10 00258", "qty": 1, "rule": "R5.2"},
            {"code": "10 00302", "qty": 1, "note": "Kumanda", "rule": "R5.3"},
            {"code": "10 03253", "qty": 1, "rule": "R5.7"},
            {"code": "10 16235", "qty": 1, "rule": "R5.7"},
            {"code": "10 03313", "qty": 1, "rule": "R5.8"},
            {"code": "10 03578", "qty": 1, "note": "Motor grubu", "rule": "R5.10"},
            {"code": "10 15962", "qty": 1, "note": "Ek bara", "rule": "R5.10"},
            {"code": "10 17185", "qty": 1, "rule": "R8.4"},
            {"code": "10 18528", "qty": "giriş > 36 / çıkış > 24 ise 1", "rule": "R8.4a"},
            {"code": "10 17183", "qty": 1, "rule": "R8.4"},
            {"code": "10 17184", "qty": 1, "rule": "R8.4"},
            {"code": "10 16496", "qty": 1, "rule": "R8.1"},
            {"code": "10 02146", "qty": "R numarası kadar", "note": "Çıkış rölesi", "rule": "R8.5"},
            {"code": "10 13016", "qty": "her 24 röleye 1", "rule": "R8.6"},
            {"code": "10 01332", "qty": "ısıtıcı başına 1", "note": "+ 3P 16 A sigorta", "rule": "R4.4"},
            {"code": "10 04000", "qty": "ısıtıcı başına 1", "rule": "R4.4"},
        ],
        "loads": [
            ("Motor", "Termik + kontaktör veya MKŞ + kontaktör + GVAE11", "R3.1"),
            ("Isıtıcı 6–8 kW", "LC1K1610M7 + A9F74316 16 A; termik/MKŞ yok", "R4.4"),
            ("Pompa 7,5 kW", "VFD75E43A + 3P 40 A ön sigorta", "R4.2"),
            ("PLC I/O", "48 giriş / 32 çıkış; aşarsa 2. ek modül (en çok 72/48)", "R8.4a"),
        ],
        "options": [
            {"key": "yag", "title": "Yağ sıyırıcı", "rule": "R4.7b",
             "desc": "MKŞ + kontaktör ile sürülür. Ekrandan kumanda; etikete buton/lamba konmaz.",
             "items": [("10 01368", 1), ("10 02314", 1), ("10 01365", 1)], "kb": [0, 0]},
            {"key": "safety", "title": "Safety PLC", "rule": "R8.7",
             "desc": "SO1–SO6 için 6 adet 24V yaprak röle; röle köprüsü sayımına dahil.",
             "items": [("10 02146", 6)], "kb": [0, 0]},
            {"key": "io20", "title": "2. ek modül · 12DI/8DO", "rule": "R8.4a",
             "desc": "Fazla I/O ≤ 12 giriş ve ≤ 8 çıkış ise. Giriş 4.0–4.11, çıkış 104.0–104.7.",
             "items": [("10 18528", 1)], "kb": [0, 0]},
            {"key": "io40", "title": "2. ek modül · 24DI/16DO", "rule": "R8.4a",
             "desc": "Fazla I/O ≤ 24 giriş ve ≤ 16 çıkış ise. Stok kodu henüz yok.",
             "items": [("CP1W-40EDT1", 1)], "kb": [0, 0]},
            {"key": "emn", "title": "Emniyet rölesi", "rule": "R1.6",
             "desc": "Her panoda sorulur. Kapak kapalı switchleri ve acil stop bu röleye bağlanır.",
             "items": [("10 04538", 1)], "kb": [0, 0]},
        ],
        "rules": ["R1.0", "R1.1", "R1.2", "R1.3", "R1.5", "R4.2", "R4.4", "R4.6", "R4.7b",
                  "R1.6", "R5.1", "R5.2", "R5.4", "R5.5", "R5.9", "R5.10", "R5.11", "R5.12",
                  "R8.1", "R8.2", "R8.3", "R8.4", "R8.4a", "R8.5", "R8.6", "R8.7",
                  "R9.1", "R9.2", "R9.3", "R9.4", "R9.7", "R11.13a", "R14.1", "R14.4", "R14.7"],
    },
    {
        "id": "lym",
        "name": "LYM",
        "tag": "Manuel pano · GEMO",
        "desc": "Dolfin LYM yıkama makinesi panosu. GEMO zaman rölesi ve termostatlı, dar dikey İngilizce etiket.",
        "facts": [
            ("Pano ölçüsü", "Her projede sorulur", "R1.1"),
            ("Ana kesme", "Pako (kapakta POWER)", "R1.2"),
            ("Güç kaynağı", "MDR 20/24", "R5.1"),
            ("Kaçak akım", "1 adet (tüm pano)", "R5.4"),
            ("IOF", "Yok", "R1.3"),
            ("Bara", "Yok", "R5.10"),
            ("Motor düzeni", "Termik + kontaktör", "R3.3"),
            ("Etiket dili", "İngilizce", "R14.1"),
        ],
        "label": {
            "brand": "Dolfin",
            "sub": "INDUSTRIAL WASHING SYSTEMS",
            "rows": [
                [None, {"t": "estop", "l": "EMERGENCY STOP", "code": "10 03445", "kb": [0, 2]}, None],
                [{"t": "twin", "l": "WASHING", "code": "10 00266", "kb": [1, 1], "kbOpt": {"inter": [1, 1]}},
                 None,
                 {"t": "disp", "l": "TIMER", "code": "10 10465", "txt": "DZ482"}],
                [{"t": "btn", "c": "white", "l": "TEST", "code": "10 00270", "kb": [1, 0]},
                 None,
                 {"t": "btn", "c": "blue", "l": "RESET", "code": "10 00272", "kb": [1, 1]}],
                [{"t": "sel", "l": "HEATER", "code": "10 00263", "kb": [1, 0]},
                 None,
                 {"t": "disp", "l": "THERMOSTAT", "code": "10 00237", "txt": "DT481"}],
                [{"t": "mandal", "l": "OIL SEPERATOR", "code": "10 00262", "kb": [1, 0], "opt": "yag", "off": TAPA_B},
                 None,
                 {"t": "lamp", "c": "white", "l": "OIL SEPERATOR", "code": "10 00279", "opt": "yag", "off": TAPA_L}],
                [{"t": "lamp", "c": "red", "l": "INADEQUATE WATER LEVEL", "code": "10 00278"},
                 {"t": "lamp", "c": "red", "l": "REDUCTOR FAILURE", "code": "10 00278"},
                 {"t": "lamp", "c": "red", "l": "PUMP FAILURE", "code": "10 00278"}],
                [None, {"t": "pako", "l": "POWER", "code": "10 00287"}, None],
            ],
            "note": "Gerçek etiketten (Dolfin LYM) alındı. Yağ sıyırıcı yoksa iki delik tapa ile kapatılır; tapa depo listesine yazılmaz.",
        },
        "cift_el": False,
        "standard": [
            {"series": "Pako şalter", "photo": "10 00287", "choices": "3×25 · 3×40 · 3×63 A", "note": "Tablo akımına göre en küçük", "rule": "R5.6"},
            {"series": "Kaçak akım 4P", "photo": "10 00304", "choices": "25 · 40 · 63 · 80 · 100 A", "note": "Tüm pano için 1 adet", "rule": "R5.4"},
            {"series": "Aşırı akım koruma 4P", "photo": "10 02664", "choices": "25 · 40 · 63 A", "note": "Tüm pano için 1 adet", "rule": "R5.5"},
            {"code": "10 02491", "qty": 1, "rule": "R5.1"},
            {"code": "10 00258", "qty": 1, "rule": "R5.2"},
            {"code": "10 00302", "qty": 1, "note": "Kumanda", "rule": "R5.3"},
            {"code": "10 01421", "qty": 1, "note": "Pano lambası", "rule": "R5.7"},
            {"code": "10 03253", "qty": 1, "rule": "R5.7"},
            {"code": "10 16235", "qty": 1, "rule": "R5.7"},
            {"code": "10 03313", "qty": 1, "rule": "R5.8"},
            {"code": "10 01398", "qty": 1, "rule": "R5.13"},
            {"code": "10 00294", "qty": 2, "note": "İnvertörle 3", "rule": "R5.13"},
            {"code": "10 00295", "qty": 3, "note": "İnvertörle 4", "rule": "R5.13"},
            {"code": "10 10465", "qty": 1, "note": "TIMER", "rule": "R14.8"},
            {"code": "10 00237", "qty": 1, "note": "THERMOSTAT", "rule": "R14.8"},
        ],
        "loads": [
            ("Motor", "Termik + kontaktör, In'e göre", "R3.3"),
            ("Sepet redüktörü", "İnvertör istenirse: invertör + 1×6 + 220V röle + soket", "R4.1"),
            ("Sensör", "Kontaktör, termik, MKŞ yok", "R4.5"),
        ],
        "options": [
            {"key": "yag", "title": "Yağ sıyırıcı", "rule": "R4.7a",
             "desc": "Termik + kontaktör ile sürülür. Etikete buton (sol) + lamba (sağ); yoksa tapa.",
             "items": [("10 00243", 1), ("10 02314", 1), ("10 00262", 1), ("10 00279", 1)], "kb": [0, 0]},
            {"key": "inter", "title": "İnterlock kilit", "rule": "R9.3a",
             "desc": "WASHING ikiz butonu 1 NO + 1 NC yerine 2 NO + 2 NC olur.",
             "items": [], "kb": [0, 0]},
            {"key": "inv", "title": "Sepet invertörü", "rule": "R4.1",
             "desc": "Sepet redüktörü invertörle sürülürse; 220V röle ve soket de eklenir (unutma).",
             "items": [("10 16319", 1), ("10 01421", 1), ("10 00294", 1), ("10 00295", 1)], "kb": [0, 0]},
            {"key": "emn", "title": "Emniyet rölesi", "rule": "R1.6",
             "desc": "Her panoda sorulur. Kapak kapalı switchleri ve acil stop bu röleye bağlanır.",
             "items": [("10 04538", 1)], "kb": [0, 0]},
        ],
        "rules": ["R1.0", "R1.1", "R1.2", "R1.3", "R1.5", "R4.1", "R4.1a", "R4.1b", "R4.1c", "R4.1d",
                  "R4.7a", "R4.7c", "R1.6", "R5.1", "R5.2", "R5.4", "R5.6", "R5.10", "R5.13",
                  "R9.1", "R9.2", "R9.3a", "R9.5", "R9.5a", "R9.6a", "R9.7",
                  "R14.1", "R14.5", "R14.6", "R14.8", "R14.9", "R14.10"],
    },
]

SHARED = [  # her modelde olmazsa olmaz kurallar
    "R0.2", "R0.3", "R0.4", "R0.5", "R0.6", "R2.1", "R2.6", "R2.7", "R2.7a", "R2.8", "R3.1", "R10.3", "R10.6",
]


def catalog(md):
    """Katalog tablolarından kod/ref -> malzeme adı."""
    names = {}
    for ln in md.splitlines():
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        for c in cells[1:]:
            if bh.CODE_RE.match(c) and cells[0] and not cells[0].startswith("-"):
                names.setdefault(c, cells[0])
    return names


def rules(md):
    out = {}
    for ln in md.splitlines():
        if ln.startswith("- **"):
            m = bh.RULE_RE.match(ln[2:])
            if m:
                out[m.group(1)] = bh.render_li(ln[2:].strip())
    return out


def build():
    md = bh.SRC.read_text(encoding="utf-8")
    names = catalog(md)
    rl = rules(md)

    codes = set()
    for m in MODELS:
        for it in m["standard"]:
            codes.add(it.get("code") or it.get("photo"))
        for o in m["options"]:
            codes.update(c for c, _ in o["items"])
        for row in m["label"]["rows"]:
            if isinstance(row, list):
                for c in row:
                    if c:
                        codes.add(c["code"]) if "code" in c else None
        missing = [r for r in m["rules"] if r not in rl]
        if missing:
            raise SystemExit(f"{m['name']}: KURALLAR.md'de olmayan kural: {missing}")
    for extra in ("10 00267", "10 00268", "10 00273", "10 00271"):
        codes.add(extra)
    unknown = [c for c in codes if c not in names]
    if unknown:
        raise SystemExit(f"Katalogda adı olmayan kod: {unknown}")

    data = {
        "models": MODELS,
        "names": {c: names[c] for c in codes},
        "photos": {c: bh.thumb(c) for c in codes if bh.thumb(c)},
        "rules": rl,
        "shared": SHARED,
    }
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    page = TEMPLATE.replace("/*DATA*/", json.dumps(data, ensure_ascii=False)).replace("{{STAMP}}", stamp)
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.name}: {len(MODELS)} model, {len(codes)} kalem")


TEMPLATE = r"""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pano Modelleri</title>
<style>
:root{--bg:#f4f3ef;--panel:#fff;--ink:#1c2127;--mute:#69717b;--line:#e2e0da;--accent:#c2410c;--accent-soft:#fff0e6;
--blue:#1d4ed8;--blue-soft:#e8efff;--ok:#047857;--ok-soft:#e5f5ee;--warn:#b45309;--warn-soft:#fff6e0;--chip:#eef0f3;
--label:#fbfbf9;--label-line:#cfd3d8;--shadow:0 1px 2px rgba(0,0,0,.04),0 6px 20px rgba(0,0,0,.06)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111316;--panel:#1a1d21;--ink:#e7e9ec;--mute:#9aa3ad;--line:#2b3036;
--accent:#fb923c;--accent-soft:#2d1d12;--blue:#8fb0ff;--blue-soft:#1a2440;--ok:#4ade80;--ok-soft:#12291e;--warn:#f5b54a;--warn-soft:#2d2412;
--chip:#252a30;--label:#e9ebee;--label-line:#9aa3ad;--shadow:none}}
:root[data-theme="dark"]{--bg:#111316;--panel:#1a1d21;--ink:#e7e9ec;--mute:#9aa3ad;--line:#2b3036;--accent:#fb923c;--accent-soft:#2d1d12;
--blue:#8fb0ff;--blue-soft:#1a2440;--ok:#4ade80;--ok-soft:#12291e;--warn:#f5b54a;--warn-soft:#2d2412;--chip:#252a30;--label:#e9ebee;--label-line:#9aa3ad;--shadow:none}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 "Segoe UI",system-ui,sans-serif}
header{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.hb{max-width:1320px;margin:0 auto;padding:10px 20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.logo{width:34px;height:34px;border-radius:8px;background:var(--accent);display:grid;place-items:center;color:#fff}
.ht{font-weight:650;line-height:1.2}.hs{font-size:12px;color:var(--mute)}
.tabs{display:flex;gap:6px;margin-left:auto;background:var(--chip);padding:4px;border-radius:10px}
.tabs button{border:0;background:transparent;color:var(--ink);font:600 14px inherit;font-family:inherit;padding:7px 16px;border-radius:7px;cursor:pointer}
.tabs button.on{background:var(--panel);color:var(--accent);box-shadow:var(--shadow)}
.lnk{font-size:13px;color:var(--mute);text-decoration:none;border:1px solid var(--line);padding:6px 10px;border-radius:8px;background:var(--panel)}
.tb{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 10px;cursor:pointer}
main{max-width:1320px;margin:0 auto;padding:22px 20px 40px}
.hero{display:flex;gap:20px;align-items:flex-end;justify-content:space-between;flex-wrap:wrap;margin-bottom:16px}
.hero h1{margin:0;font-size:34px;letter-spacing:-.02em}.hero .tag{color:var(--accent);font-weight:600;font-size:14px}
.hero p{margin:4px 0 0;color:var(--mute);max-width:640px}
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:22px}
.fact{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow);position:relative}
.fact span{display:block;font-size:12px;color:var(--mute)}.fact b{font-size:15px}
.fact a{position:absolute;top:10px;right:10px}
.rid{font:600 11px/1 ui-monospace,Consolas,monospace;color:var(--blue);background:var(--blue-soft);border-radius:5px;padding:4px 6px;text-decoration:none;white-space:nowrap}
.grid{display:grid;grid-template-columns:minmax(330px,420px) 1fr;gap:22px;align-items:start}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow);margin-bottom:22px}
.card h2{margin:0 0 4px;font-size:18px;display:flex;align-items:center;gap:8px}.card .sub{color:var(--mute);font-size:13px;margin:0 0 14px}
.h2i{width:26px;height:26px;border-radius:7px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-size:14px}
/* ---- etiket ---- */
.labelwrap{display:flex;justify-content:center;padding:6px 0 4px}
.label{width:300px;background:var(--label);border:2px solid var(--label-line);border-radius:6px;padding:16px 12px 14px;position:relative;color:#1b1f24;
box-shadow:inset 0 0 0 4px #fff,0 10px 30px rgba(0,0,0,.12)}
.label .screw{position:absolute;width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff,#9aa1a9);border:1px solid #8a9199}
.brand{text-align:center;font-weight:800;font-size:28px;color:#d4232b;letter-spacing:-.02em;line-height:1}
.brand small{display:block;font-size:9px;color:#333;letter-spacing:.08em;font-weight:700;margin-top:4px}
.lrow{display:grid;grid-template-columns:1fr 1fr 1fr;align-items:end;justify-items:center;margin-top:16px;gap:4px}
.lrow.wide{grid-template-columns:1fr}
.comp{display:flex;flex-direction:column;align-items:center;gap:5px;cursor:default;position:relative}
.comp .lt{font:700 8.5px/1.15 "Segoe UI",sans-serif;text-align:center;letter-spacing:.03em;max-width:92px;color:#222}
.comp.dim{opacity:.35}
.comp:hover .pop{display:block}
.pop{display:none;position:absolute;bottom:calc(100% + 6px);left:50%;transform:translateX(-50%);background:var(--panel);color:var(--ink);border:1px solid var(--line);
border-radius:10px;padding:8px;width:170px;z-index:30;box-shadow:0 10px 30px rgba(0,0,0,.2);font-size:11px;text-align:center}
.pop img{width:90px;height:90px;object-fit:contain;display:block;margin:0 auto 4px}
.pop code{font:600 11px ui-monospace,Consolas,monospace}
.estop{width:66px;height:66px;border-radius:50%;background:#f5c400;display:grid;place-items:center;box-shadow:inset 0 0 0 2px #c79f00}
.estop i{width:44px;height:44px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#ff6b6b,#c1121f 60%,#7d0a12);box-shadow:0 3px 6px rgba(0,0,0,.35)}
.btn{width:40px;height:40px;border-radius:50%;background:linear-gradient(#e9ecef,#9aa1a9);display:grid;place-items:center;box-shadow:0 2px 4px rgba(0,0,0,.25)}
.btn i{width:30px;height:30px;border-radius:50%;box-shadow:inset 0 -3px 6px rgba(0,0,0,.25),inset 0 3px 5px rgba(255,255,255,.5)}
.lamp{width:26px;height:26px;border-radius:50%;background:linear-gradient(#e9ecef,#9aa1a9);display:grid;place-items:center}
.lamp i{width:19px;height:19px;border-radius:50%;box-shadow:inset 0 2px 4px rgba(255,255,255,.6)}
.c-red{background:radial-gradient(circle at 40% 35%,#ff7b7b,#d00000)}.c-green{background:radial-gradient(circle at 40% 35%,#5fe08a,#0b8a3a)}
.c-blue{background:radial-gradient(circle at 40% 35%,#7cc8ff,#0a6fc2)}.c-white{background:radial-gradient(circle at 40% 35%,#fff,#d8dbe0)}
.twin{width:40px;height:62px;border-radius:20px;background:linear-gradient(#e9ecef,#9aa1a9);padding:4px;display:flex;flex-direction:column;gap:3px;box-shadow:0 2px 4px rgba(0,0,0,.25)}
.twin i{flex:1;border-radius:16px 16px 4px 4px}.twin i+i{border-radius:4px 4px 16px 16px}
.sel{width:40px;height:40px;border-radius:50%;background:linear-gradient(#e9ecef,#9aa1a9);display:grid;place-items:center;box-shadow:0 2px 4px rgba(0,0,0,.25)}
.sel i{width:30px;height:30px;border-radius:50%;background:radial-gradient(circle,#2fd36b,#0b7a33);position:relative}
.sel i::after{content:"";position:absolute;left:12px;top:3px;width:6px;height:24px;border-radius:3px;background:#0a5a26;transform:rotate(-30deg)}
.mandal{width:40px;height:40px;border-radius:50%;background:linear-gradient(#e9ecef,#9aa1a9);display:grid;place-items:center;box-shadow:0 2px 4px rgba(0,0,0,.25)}
.mandal i{width:30px;height:30px;border-radius:50%;background:#1d1f22;position:relative}
.mandal i::after{content:"";position:absolute;left:12px;top:3px;width:6px;height:24px;border-radius:3px;background:#555}
.disp{width:66px;height:66px;background:#111;border-radius:4px;border:2px solid #333;padding:4px;display:flex;flex-direction:column;justify-content:space-between}
.disp.big{width:150px;height:74px}
.disp em{font:700 8px sans-serif;color:#ddd;font-style:normal}.disp b{font:700 16px ui-monospace,monospace;color:#ff3b30;text-align:right;text-shadow:0 0 6px #ff3b30}
.hmi{width:170px;height:104px;background:#2a2d31;border-radius:6px;padding:7px}
.hmi i{display:block;height:100%;border-radius:3px;background:linear-gradient(135deg,#0e3a5c,#1f6fa8);position:relative}
.hmi i::after{content:"HMI";position:absolute;inset:0;display:grid;place-items:center;color:#cfe6ff;font:700 13px sans-serif;letter-spacing:.1em}
.pako{width:74px;height:74px;background:#f5c400;border-radius:4px;display:grid;place-items:center;box-shadow:inset 0 0 0 2px #c79f00}
.pako i{width:54px;height:54px;border-radius:50%;background:#d0191f;position:relative}
.pako i::after{content:"";position:absolute;left:22px;top:-2px;width:10px;height:58px;border-radius:5px;background:#e3262c;box-shadow:0 2px 3px rgba(0,0,0,.3)}
.tms{width:74px;height:74px;background:#3a3d42;border-radius:6px;display:grid;place-items:center}
.tms i{width:52px;height:52px;border-radius:50%;background:#16181b;position:relative}
.tms i::after{content:"";position:absolute;left:21px;top:0;width:10px;height:52px;border-radius:5px;background:#2b2e33}
.tapaB{width:40px;height:40px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#444,#0d0d0d)}
.tapaL{width:22px;height:22px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#444,#0d0d0d)}
.ciftel{display:grid;grid-template-columns:auto auto 1fr auto;margin-top:16px;align-items:center;border-top:1px dashed #b9bec5;padding:12px 4px 0;gap:6px}
.ciftel .gap{height:2px;border-top:2px dashed #b9bec5;margin:0 6px;position:relative}
.ciftel .gap span{position:absolute;top:-16px;left:50%;transform:translateX(-50%);font:700 8px sans-serif;color:#8a9199;white-space:nowrap}
.ciftel .col{display:flex;flex-direction:column;gap:46px;align-items:center}
.dimv{height:150px;width:2px;background:#d4232b;position:relative}
.dimv::before,.dimv::after{content:"";position:absolute;left:-5px;width:12px;height:2px;background:#d4232b}.dimv::before{top:0}.dimv::after{bottom:0}
.dimv{margin:0 58px 0 14px}
.dimv span{position:absolute;left:8px;top:50%;transform:translateY(-50%);font:700 9px sans-serif;color:#d4232b;white-space:nowrap}
.lnote{font-size:12px;color:var(--mute);margin-top:12px;text-align:center}
/* ---- opsiyonlar ---- */
.opts{display:grid;gap:10px}
.opt{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:start;border:1px solid var(--line);border-radius:12px;padding:12px 14px;cursor:pointer;transition:.15s}
.opt:hover{border-color:var(--accent)}.opt.on{background:var(--accent-soft);border-color:var(--accent)}
.sw{width:38px;height:22px;border-radius:11px;background:var(--line);position:relative;transition:.15s;margin-top:2px}
.sw::after{content:"";position:absolute;width:18px;height:18px;border-radius:50%;background:#fff;top:2px;left:2px;transition:.15s;box-shadow:0 1px 2px rgba(0,0,0,.3)}
.opt.on .sw{background:var(--accent)}.opt.on .sw::after{left:18px}
.opt b{display:block}.opt p{margin:2px 0 6px;color:var(--mute);font-size:13px}
.minis{display:flex;gap:6px;flex-wrap:wrap}
.mini{display:flex;align-items:center;gap:6px;background:var(--chip);border-radius:7px;padding:3px 8px 3px 3px;font-size:12px}
.mini img{width:24px;height:24px;object-fit:contain;background:#fff;border-radius:5px}
.kbbox{display:flex;gap:10px;margin-top:14px}
.kb{flex:1;border-radius:12px;padding:12px;text-align:center;border:1px solid var(--line)}
.kb b{display:block;font-size:30px;line-height:1.1;font-variant-numeric:tabular-nums}.kb span{font-size:12px;color:var(--mute)}
.kb.no{background:var(--ok-soft)}.kb.no b{color:var(--ok)}.kb.nc{background:var(--warn-soft)}.kb.nc b{color:var(--warn)}
/* ---- olmazsa olmazlar ---- */
.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.item{display:grid;grid-template-columns:64px 1fr;gap:10px;align-items:center;border:1px solid var(--line);border-radius:12px;padding:10px;background:var(--panel)}
.item .ph{width:64px;height:64px;border-radius:8px;background:#fff;display:grid;place-items:center;border:1px solid var(--line)}
.item .ph img{width:58px;height:58px;object-fit:contain}
.item .nm{font-size:13px;font-weight:600;line-height:1.3}
.item .meta{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-top:4px}
.code{font:600 11px ui-monospace,Consolas,monospace;background:var(--chip);border-radius:5px;padding:2px 6px}
.qty{font:700 12px sans-serif;color:#fff;background:var(--accent);border-radius:999px;padding:2px 8px}
.qty.txt{background:var(--chip);color:var(--ink);font-weight:600}
.item .nt{font-size:12px;color:var(--mute);margin-top:2px}
.item.series{border-style:dashed}
.item.opt-item{background:var(--accent-soft);border-color:var(--accent)}
.loads{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.load{border-left:4px solid var(--accent);background:var(--chip);border-radius:8px;padding:10px 12px}
.load b{display:block;font-size:14px}.load span{font-size:13px;color:var(--mute)}
table{width:100%;border-collapse:collapse;font-size:14px}
th{font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--mute);text-align:center;padding:8px;background:var(--chip)}
td{padding:7px 8px;border-top:1px solid var(--line);vertical-align:middle}
td.c{text-align:center;font-variant-numeric:tabular-nums}
td img{width:32px;height:32px;object-fit:contain;vertical-align:middle;background:#fff;border-radius:5px}
tr.o td{background:var(--accent-soft)}
.tw{border:1px solid var(--line);border-radius:10px;overflow:auto}
ul.rules{list-style:none;margin:0;padding:0}
li.rule{display:grid;grid-template-columns:64px 1fr;gap:10px;padding:8px 0;border-top:1px solid var(--line)}
li.rule:first-child{border-top:0}
li.rule .rid{text-align:center;height:max-content;margin-top:2px}
.rlabel{font-weight:650;margin-right:4px}.rlabel::after{content:" —";color:var(--mute);font-weight:400}
.chip{font:600 11px ui-monospace,Consolas,monospace;background:var(--chip);border:1px solid var(--line);border-radius:5px;padding:0 5px;white-space:nowrap}
.chip.nophoto{border-style:dashed}
.arrow{color:var(--accent);font-weight:700}
code{font:12px ui-monospace,Consolas,monospace;background:var(--chip);padding:1px 5px;border-radius:4px}
details summary{cursor:pointer;font-weight:600;color:var(--mute);margin-top:6px}
.cols2{display:grid;grid-template-columns:1fr 1fr;gap:22px}
footer{text-align:center;color:var(--mute);font-size:12px;padding:0 0 30px}
@media (max-width:980px){.grid,.cols2{grid-template-columns:1fr}.facts{grid-template-columns:repeat(2,1fr)}}
@media (max-width:560px){main{padding:16px}.hb{padding:10px 16px}.tabs{margin-left:0;width:100%}.tabs button{flex:1;padding:7px 4px}.hero h1{font-size:28px}}
</style></head>
<body>
<header><div class="hb">
<div class="logo"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="9" r="2.5"/><path d="M8 15h8M8 18h8"/></svg></div>
<div><div class="ht">Pano Modelleri</div><div class="hs">KURALLAR.md'den üretildi · {{STAMP}}</div></div>
<nav class="tabs" id="tabs"></nav>
<a class="lnk" href="kurallar.html">Tüm kurallar →</a>
<button class="tb" id="theme" title="Tema">◐</button>
</div></header>
<main id="main"></main>
<footer>Kaynak: kurallar/KURALLAR.md · üretici: <code>python kurallar/build_panolar.py</code></footer>
<script>
const D=/*DATA*/;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const nm=c=>D.names[c]||c, ph=c=>D.photos[c];
const R=id=>`<a class="rid" href="kurallar.html#${id}" title="Kuralı aç">${id}</a>`;
let cur=null, opts={};
const EXCL={io20:'io40',io40:'io20'}; // birbirini dışlayan opsiyonlar
try{cur=localStorage.getItem('pm');}catch(e){}
if(location.hash)cur=location.hash.slice(1);
if(!D.models.find(m=>m.id===cur))cur=D.models[0].id;

function comp(c,m){
  if(!c)return '<div></div>';
  let dim='';
  if(c.opt&&!opts[c.opt]){ if(c.off) c=Object.assign({},c.off,{l:c.l}); }
  const t=c.t; let g='';
  if(t==='estop')g='<div class="estop"><i></i></div>';
  else if(t==='btn')g=`<div class="btn"><i class="c-${c.c}"></i></div>`;
  else if(t==='lamp')g=`<div class="lamp"><i class="c-${c.c}"></i></div>`;
  else if(t==='twin')g='<div class="twin"><i class="c-green"></i><i class="c-red"></i></div>';
  else if(t==='sel')g='<div class="sel"><i></i></div>';
  else if(t==='mandal')g='<div class="mandal"><i></i></div>';
  else if(t==='disp')g=`<div class="disp${c.big?' big':''}"><em>${esc(c.txt||c.l)}</em><b>${c.big?'85°C':'10.0'}</b></div>`;
  else if(t==='hmi')g='<div class="hmi"><i></i></div>';
  else if(t==='pako')g='<div class="pako"><i></i></div>';
  else if(t==='tms')g='<div class="tms"><i></i></div>';
  else if(t==='tapaB')g='<div class="tapaB"></div>';
  else if(t==='tapaL')g='<div class="tapaL"></div>';
  let pop='';
  if(c.code){const p=ph(c.code);
    const kb=kbOf(c); const kbs=kb?`<div style="margin-top:3px">${kb[0]} NO · ${kb[1]} NC</div>`:'';
    pop=`<div class="pop">${p?`<img src="${p}">`:''}<div>${esc(nm(c.code))}</div><code>${esc(c.code)}</code>${kbs}</div>`;}
  else if(t.startsWith('tapa'))pop='<div class="pop">Tapa — opsiyon yok.<br>Depo listesine yazılmaz (R14.6).</div>';
  return `<div class="comp${dim}">${pop}<div class="lt">${esc(c.l)}</div>${g}</div>`;
}
function kbOf(c){ if(!c.kb)return null; let k=c.kb.slice(); if(c.kbOpt)for(const o in c.kbOpt)if(opts[o]){k[0]+=c.kbOpt[o][0];k[1]+=c.kbOpt[o][1];} return k;}
function labelHTML(m){
  const L=m.label; let h=`<div class="label">`;
  for(const [x,y] of [[6,6],[279,6],[6,'b'],[279,'b']]) h+=`<span class="screw" style="left:${x}px;${y==='b'?'bottom:6px':'top:6px'}"></span>`;
  h+=`<div class="brand">${esc(L.brand)}${L.sub?`<small>${esc(L.sub)}</small>`:''}</div>`;
  for(const row of L.rows){
    if(row==='CIFT_EL'){
      const a={t:'btn',c:'green',l:'KAPAK AÇ',code:'10 00273',kb:[1,1]}, k={t:'btn',c:'red',l:'KAPAK KAPAT',code:'10 00271',kb:[1,1]};
      h+=`<div class="ciftel"><div class="col">${comp(a)}${comp(a)}</div><div class="dimv"><span>≥ 25–30 cm</span></div><div class="gap"><span>yatay mesafe serbest</span></div><div class="col">${comp(k)}${comp(k)}</div></div>`;
      continue;}
    h+=`<div class="lrow">${row.map(c=>comp(c,m)).join('')}</div>`;
  }
  return h+'</div>';
}
function labelComps(m){
  const out=[];
  for(const row of m.label.rows){
    if(row==='CIFT_EL'){out.push({code:'10 00273',kb:[1,1]},{code:'10 00273',kb:[1,1]},{code:'10 00271',kb:[1,1]},{code:'10 00271',kb:[1,1]});continue;}
    for(let c of row){ if(!c)continue; if(c.opt&&!opts[c.opt])continue; out.push(c);}
  }
  return out;
}
function contacts(m){
  let no=0,nc=0;
  for(const c of labelComps(m)){const k=kbOf(c); if(k){no+=k[0];nc+=k[1];}}
  for(const o of m.options)if(opts[o.key]){no+=o.kb[0];nc+=o.kb[1];}
  return [no,nc];
}
function itemCard(it,extra){
  if(it.series){const p=ph(it.photo);
    return `<div class="item series"><div class="ph">${p?`<img src="${p}">`:''}</div><div><div class="nm">${esc(it.series)}</div>
    <div class="meta"><span class="qty txt">${esc(it.choices)}</span>${R(it.rule)}</div><div class="nt">${esc(it.note)}</div></div></div>`;}
  const p=ph(it.code), q=typeof it.qty==='number'?`<span class="qty">× ${it.qty}</span>`:`<span class="qty txt">${esc(it.qty)}</span>`;
  return `<div class="item${extra||''}"><div class="ph">${p?`<img src="${p}">`:''}</div><div><div class="nm">${esc(nm(it.code))}</div>
  <div class="meta"><span class="code">${esc(it.code)}</span>${q}${it.rule?R(it.rule):''}</div>${it.note?`<div class="nt">${esc(it.note)}</div>`:''}</div></div>`;
}
function depo(m){
  const rows=new Map();
  const add=(code,qty,src,o)=>{const r=rows.get(code)||{code,qty:0,txt:[],src:new Set(),o:false};
    if(typeof qty==='number')r.qty+=qty;else r.txt.push(qty); r.src.add(src); r.o=r.o||o; rows.set(code,r);};
  for(const it of m.standard)if(it.code)add(it.code,it.qty,'Standart',false);
  // etiket elemanları: pako/TMŞ seri olarak, ekran/ORDEL/GEMO standart listede zaten sayılır
  const lab={}, labOpt={};
  for(const c of labelComps(m)){
    if(!c.code||c.t==='pako'||c.t==='tms')continue;
    if(m.standard.some(s=>s.code===c.code))continue;
    lab[c.code]=(lab[c.code]||0)+1; if(c.opt)labOpt[c.code]=true;}
  for(const k in lab)add(k,lab[k],'Etiket',!!labOpt[k]);
  for(const o of m.options)if(opts[o.key])for(const [c,q] of o.items){ if(m.label.rows.flat().some(x=>x&&x.opt===o.key&&x.code===c))continue; add(c,q,o.title,true);}
  const [no,nc]=contacts(m); add('10 00267',no,'Kontak (R9)',false); add('10 00268',nc,'Kontak (R9)',false);
  let h='<div class="tw"><table><thead><tr><th>Foto</th><th>Malzeme</th><th>Kod</th><th>Adet</th><th>Kaynak</th></tr></thead><tbody>';
  for(const it of m.standard)if(it.series)h+=`<tr><td class="c">${ph(it.photo)?`<img src="${ph(it.photo)}">`:''}</td><td>${esc(it.series)} <span style="color:var(--mute)">(${esc(it.choices)})</span></td><td class="c">akıma göre</td><td class="c">${esc(it.note)}</td><td class="c">${R(it.rule)}</td></tr>`;
  for(const r of rows.values()){ if(!r.qty&&!r.txt.length)continue;
    const q=[r.qty?r.qty:null,...r.txt].filter(Boolean).join(' + ');
    h+=`<tr class="${r.o?'o':''}"><td class="c">${ph(r.code)?`<img src="${ph(r.code)}">`:''}</td><td>${esc(nm(r.code))}</td><td class="c"><span class="code">${esc(r.code)}</span></td><td class="c"><b>${esc(q)}</b></td><td class="c" style="font-size:12px;color:var(--mute)">${esc([...r.src].join(', '))}</td></tr>`;}
  return h+'</tbody></table></div>';
}
function render(){
  const m=D.models.find(x=>x.id===cur);
  document.getElementById('tabs').innerHTML=D.models.map(x=>`<button class="${x.id===cur?'on':''}" data-id="${x.id}">${esc(x.name)}</button>`).join('');
  const [no,nc]=contacts(m);
  let h=`<div class="hero"><div><div class="tag">${esc(m.tag)}</div><h1>${esc(m.name)}</h1><p>${esc(m.desc)}</p></div></div>`;
  h+='<div class="facts">'+m.facts.map(([k,v,r])=>`<div class="fact">${R(r)}<span>${esc(k)}</span><b>${esc(v)}</b></div>`).join('')+'</div>';
  h+=`<div class="grid"><div class="card"><h2><span class="h2i">▣</span>Pano etiketi</h2><p class="sub">Elemanın üzerine gel: malzeme, kod, kontak.</p>
     <div class="labelwrap">${labelHTML(m)}</div><div class="lnote">${esc(m.label.note)}</div></div><div>`;
  h+=`<div class="card"><h2><span class="h2i">⚙</span>Opsiyonlar</h2><p class="sub">Aç/kapat — etiket, depo listesi ve kontak sayısı birlikte güncellenir (R1.5).</p><div class="opts">`;
  for(const o of m.options){
    h+=`<div class="opt${opts[o.key]?' on':''}" data-opt="${o.key}"><div class="sw"></div><div><b>${esc(o.title)}</b><p>${esc(o.desc)}</p><div class="minis">`+
      o.items.map(([c,q])=>`<span class="mini">${ph(c)?`<img src="${ph(c)}">`:''}${esc(c)} × ${q}</span>`).join('')+`</div></div>${R(o.rule)}</div>`;}
  h+=`</div><div class="kbbox"><div class="kb no"><b>${no}</b><span>NO kontak blok · B1 10 00267</span></div><div class="kb nc"><b>${nc}</b><span>NC kontak blok · B2 10 00268</span></div></div></div>`;
  h+=`<div class="card"><h2><span class="h2i">⚡</span>Yük eşlemeleri</h2><p class="sub">Hangi yük nasıl sürülür.</p><div class="loads">`+
     m.loads.map(([a,b,r])=>`<div class="load"><b>${esc(a)} ${R(r)}</b><span>${esc(b)}</span></div>`).join('')+'</div></div></div></div>';
  h+=`<div class="card"><h2><span class="h2i">★</span>Olmazsa olmazlar</h2><p class="sub">Bu modelde her panoda bulunan standart malzemeler. Kesik çerçeve: akıma göre seriden seçilir.</p><div class="items">`+
     m.standard.map(it=>itemCard(it)).join('')+'</div></div>';
  h+=`<div class="card"><h2><span class="h2i">☰</span>Depo listesi önizleme</h2><p class="sub">Standart + etiket + seçili opsiyonlar. Turuncu satırlar opsiyondan gelir. Motor ve ısıtıcı kalemleri projeye göre eklenir.</p>${depo(m)}</div>`;
  h+=`<div class="cols2"><div class="card"><h2><span class="h2i">§</span>${esc(m.name)} kuralları</h2><p class="sub">Bu modeli doğrudan ilgilendiren kurallar.</p><ul class="rules">`+
     m.rules.map(r=>D.rules[r]).join('')+`</ul></div><div class="card"><h2><span class="h2i">◎</span>Her modelde ortak</h2><p class="sub">Tüm panolarda geçerli temel kurallar.</p><ul class="rules">`+
     D.shared.map(r=>D.rules[r]).join('')+'</ul></div></div>';
  document.getElementById('main').innerHTML=h;
}
document.addEventListener('click',e=>{
  const t=e.target.closest('#tabs button'); if(t){cur=t.dataset.id;opts={};try{localStorage.setItem('pm',cur)}catch(_){} history.replaceState(null,'','#'+cur); render();window.scrollTo({top:0});return;}
  const o=e.target.closest('.opt'); if(o&&!e.target.closest('a')){const k=o.dataset.opt;opts[k]=!opts[k];
    if(opts[k]&&EXCL[k])opts[EXCL[k]]=false; render();}
});
document.getElementById('theme').onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('kt',r.dataset.theme)}catch(e){}};
try{const t=localStorage.getItem('kt');if(t)document.documentElement.dataset.theme=t}catch(e){}
render();
</script>
</body></html>"""

if __name__ == "__main__":
    build()
