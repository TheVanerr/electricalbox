# -*- coding: utf-8 -*-
"""Shared pano layout SVG builder — row2 band from tallest item + 20 mm üst/alt."""
from __future__ import annotations

SCALE = 1.55
PANO, TAVA, DUCT = 710, 630, 40
MARGIN, RAIL_H, GAP_DEF, GROUP_GAP = 20, 35, 2, 4
LC1K, LR2K = (45, 58), (45, 58)
ASSEMBLY_H, OVERLAP = 94, LC1K[1] + LR2K[1] - 94
RELAY = (22, 72)
BARA_W = 10
INNER_W = TAVA - 2 * DUCT


def fit_gap(boxes, inner_w, group_after=None):
    n = len(boxes)
    if n <= 1:
        return 0
    base = sum(boxes) + GROUP_GAP * len(group_after or [])
    return max(0.4, min(GAP_DEF, (inner_w - base) / (n - 1)))


def row2_geometry(row2_top_mm: float, tail_blocks: list[tuple]) -> tuple[float, float, float]:
    """
    tail_blocks: (w, h) for items centered on kontaktör Y (MDR, G9, vb.)
    Returns cy2_mm, asm_top_mm, row2_band_mm relative to row2_top_mm=0 baseline.
    """
    half_tails = [h / 2 for _, h in tail_blocks]
    max_half = max([LC1K[1] / 2] + half_tails) if half_tails else LC1K[1] / 2
    # cy so tallest centered item has top at MARGIN
    cy = MARGIN + max_half
    asm_top = cy - LC1K[1] / 2
    stack_bottom = asm_top + ASSEMBLY_H
    # all centered tails
    for _, h in tail_blocks:
        stack_bottom = max(stack_bottom, cy + h / 2)
    row2_band = MARGIN + stack_bottom + MARGIN
    return cy, asm_top, row2_band


def build_terminals(motor_names: list[str]):
    items = []
    for i in range(5):
        items.append({"w": 12, "h": 55, "fill": "#b8ddb0", "stroke": "#2d6b2d", "tag": f"L{i+1}", "group_end": False})
    for mi, m in enumerate(motor_names):
        for j in range(4):
            items.append({"w": 5.2, "h": 48, "fill": "#a8c8f0", "stroke": "#1a5088", "tag": m if j == 0 else "", "group_end": j == 3 and mi < len(motor_names) - 1})
    for hi, h in enumerate(["Isı.1", "Isı.2"]):
        for j in range(3):
            items.append({"w": 6.2, "h": 52, "fill": "#ffc896", "stroke": "#b85800", "tag": h if j == 0 else "", "group_end": j == 2 and hi == 0})
    for i in range(20):
        items.append({"w": 5.2, "h": 48, "fill": "#c8b8e8", "stroke": "#503080", "tag": str(i + 1) if i % 10 == 0 else "", "group_end": False})
    return items


def build_svg(
    title: str,
    sub: str,
    row1: list,
    row2_motors: list,
    row2_heaters: list,
    row2_centered: list,
    row2_mdr,
    motor_klem_names: list[str],
):
    inner_w_px = INNER_W * SCALE
    h1_max = max(b[3] for b in row1)
    inv_h = row1[-1][3]
    row1_band = h1_max + 2 * MARGIN

    tail_h = [(b[2], b[3]) for b in row2_centered] + [(row2_mdr[2], row2_mdr[3])]
    _, _, row2_band = row2_geometry(0, tail_h)

    row3_band = TAVA - 4 * DUCT - row1_band - row2_band

    pad = 24
    vb_w = PANO * SCALE + pad * 2
    vb_h = PANO * SCALE + pad * 2 + 56
    ox, oy = pad, pad + 28
    pano_px, tava_px = PANO * SCALE, TAVA * SCALE
    tava_x = ox + (pano_px - tava_px) / 2
    tava_y = oy + (pano_px - tava_px) / 2
    inner_x = tava_x + DUCT * SCALE

    def R(x, yy, w, h, fill, stroke="#1a1a1a", dash=None, sw=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<rect x="{x:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

    def rail(y_rail, label):
        return [R(inner_x, y_rail, inner_w_px, RAIL_H * SCALE, "#aeb8c8", "#4a5568", sw=1.2),
                f'<text x="{inner_x + 6:.1f}" y="{y_rail + 11:.1f}" font-size="7" fill="#2a3040">{label}</text>']

    lines = [
        f'<svg class="pano-layout-svg" viewBox="0 0 {vb_w:.1f} {vb_h:.1f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Pano dizilimi">',
        f'<text x="{ox}" y="{pad + 14}" font-size="11" font-weight="650">{title}</text>',
        R(ox, oy, pano_px, pano_px, "#e0e0e0"), R(tava_x, tava_y, tava_px, tava_px, "#fff", dash="4 3"),
        R(tava_x, tava_y, DUCT * SCALE, tava_px, "#b0b0b0", "#707070"),
        R(tava_x + tava_px - DUCT * SCALE, tava_y, DUCT * SCALE, tava_px, "#b0b0b0", "#707070"),
    ]
    y = tava_y
    lines.append(R(inner_x, y, inner_w_px, DUCT * SCALE, "#a8a8a8", "#606060"))
    y += DUCT * SCALE

    row1_top = y
    lines.append(R(inner_x, row1_top, inner_w_px, row1_band * SCALE, "none", "#ccc", dash="2 2"))
    cy1 = row1_top + (MARGIN + inv_h / 2) * SCALE
    lines.extend(rail(cy1 - RAIL_H * SCALE / 2, "DIN 35 — satır 1"))
    g1 = fit_gap([b[2] for b in row1], INNER_W)
    x = inner_x
    for code, label, w, h, fill, stroke in row1:
        bw, bh = w * SCALE, h * SCALE
        lines.append(R(x, cy1 - bh / 2, bw, bh, fill, stroke, sw=1.1))
        cx = x + bw / 2
        tc = "#fff" if fill == "#3a3a3a" else "#1a1a1a"
        lines.append(f'<text x="{cx:.1f}" y="{cy1 - 5:.1f}" text-anchor="middle" font-size="6" fill="{tc}">{label}</text>')
        lines.append(f'<text x="{cx:.1f}" y="{cy1 + 6:.1f}" text-anchor="middle" font-size="5.5" fill="{tc}">{code}</text>')
        x += bw + g1 * SCALE
    y += row1_band * SCALE
    lines.append(R(inner_x, y, inner_w_px, DUCT * SCALE, "#a8a8a8", "#606060"))
    y += DUCT * SCALE

    row2_top = y
    cy2_mm, asm_top_mm, _ = row2_geometry(0, tail_h)
    cy2 = row2_top + cy2_mm * SCALE
    asm_top = row2_top + asm_top_mm * SCALE

    lines.append(R(inner_x, row2_top, inner_w_px, row2_band * SCALE, "none", "#ccc", dash="2 2"))
    lines.extend(rail(cy2 - RAIL_H * SCALE / 2, "DIN 35 — satır 2"))

    row2_ws = [LC1K[0]] * (len(row2_motors) + len(row2_heaters))
    for b in row2_centered:
        row2_ws.append(b[2])
    row2_ws.append(row2_mdr[2])
    g2 = fit_gap(row2_ws, INNER_W)

    x = inner_x
    kw, kh = LC1K[0] * SCALE, LC1K[1] * SCALE
    tw, th = LR2K[0] * SCALE, LR2K[1] * SCALE
    for mot, kc, kl, tc, tl, has_term in row2_motors:
        if has_term:
            k_top = asm_top
            t_top = asm_top + (LC1K[1] - OVERLAP) * SCALE
            lines.append(R(x, k_top, kw, kh, "#8cb4e8", "#1a4080", sw=1.1))
            lines.append(R(x, t_top, tw, th, "#f0a8a8", "#802020", sw=1.1))
            cx = x + kw / 2
            lines.append(f'<text x="{cx:.1f}" y="{k_top+kh/2+2:.1f}" text-anchor="middle" font-size="5.5">{kl}</text>')
            lines.append(f'<text x="{cx:.1f}" y="{t_top+th/2+2:.1f}" text-anchor="middle" font-size="5.5">{tl}</text>')
            lines.append(f'<text x="{cx:.1f}" y="{t_top+th-7:.1f}" text-anchor="middle" font-size="5">{mot}</text>')
        x += kw + g2 * SCALE

    for mot, kc, kl, *_ in row2_heaters:
        lines.append(R(x, cy2 - kh / 2, kw, kh, "#e8a848", "#804000", sw=1.1))
        lines.append(f'<text x="{x+kw/2:.1f}" y="{cy2+2:.1f}" text-anchor="middle" font-size="6">{kl}</text>')
        lines.append(f'<text x="{x+kw/2:.1f}" y="{cy2+12:.1f}" text-anchor="middle" font-size="5.5">{mot}</text>')
        x += kw + g2 * SCALE

    for code, label, w, h, fill, stroke in row2_centered:
        bw, bh = w * SCALE, h * SCALE
        lines.append(R(x, cy2 - bh / 2, bw, bh, fill, stroke, sw=1.1))
        lines.append(f'<text x="{x+bw/2:.1f}" y="{cy2-4:.1f}" text-anchor="middle" font-size="6">{label}</text>')
        lines.append(f'<text x="{x+bw/2:.1f}" y="{cy2+8:.1f}" text-anchor="middle" font-size="5.5">{code}</text>')
        x += bw + g2 * SCALE

    code, label, mw, mh, fill, stroke = row2_mdr
    lines.append(R(x, cy2 - mh * SCALE / 2, mw * SCALE, mh * SCALE, fill, stroke, sw=1.1))
    lines.append(f'<text x="{x+mw*SCALE/2:.1f}" y="{cy2+2:.1f}" text-anchor="middle" font-size="6">{label}</text>')

    gap_y = asm_top + ASSEMBLY_H * SCALE
    lines.append(f'<line x1="{inner_x:.1f}" y1="{gap_y:.1f}" x2="{inner_x+inner_w_px:.1f}" y2="{gap_y:.1f}" stroke="#999" stroke-width="0.6" stroke-dasharray="3 3"/>')

    y = row2_top + row2_band * SCALE
    lines.append(R(inner_x, y, inner_w_px, DUCT * SCALE, "#a8a8a8", "#606060"))
    y += DUCT * SCALE

    row3_top = y
    lines.append(R(inner_x, row3_top, inner_w_px, row3_band * SCALE, "none", "#ccc", dash="2 2"))
    cy3 = row3_top + row3_band * SCALE / 2
    lines.extend(rail(cy3 - RAIL_H * SCALE / 2, "DIN 35 — klemens"))
    terms = build_terminals(motor_klem_names)
    ws = [t["w"] for t in terms]
    ga = [i for i, t in enumerate(terms) if t.get("group_end")]
    g3 = fit_gap(ws, INNER_W, ga)
    x = inner_x
    for t in terms:
        bw, bh = t["w"] * SCALE, t["h"] * SCALE
        lines.append(R(x, cy3 - bh / 2, bw, bh, t["fill"], t["stroke"], sw=1.1))
        if t["tag"]:
            lines.append(f'<text x="{x+bw/2:.1f}" y="{cy3+bh/2+9:.1f}" text-anchor="middle" font-size="5" fill="#333">{t["tag"]}</text>')
        x += bw + g3 * SCALE
        if t.get("group_end"):
            x += GROUP_GAP * SCALE

    bottom_y = tava_y + (TAVA - DUCT) * SCALE
    lines.append(R(inner_x, bottom_y, inner_w_px, DUCT * SCALE, "#a8a8a8", "#606060"))
    lines.append("</svg>")
    return "\n".join(lines), row2_band, row3_band
