# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from _layout_common import RELAY, BARA_W, build_svg  # noqa: E402

ROW2_MDR = ("10 02772", "MDR 100/24", 45, 90, "#f0e0ff", "#604080")

KSYSTEM_ROW1 = [
    ("10 00304", "Kaçak 40A", 72, 86, "#d4e4ff", "#2a5080"),
    ("10 02664", "Aşırı 40A", 72, 86, "#d4e4ff", "#2a5080"),
    ("10 00302", "1×3 kumanda", 18, 85, "#eef2ff", "#405080"),
    ("10 01421", "1×6 sepet", 18, 85, "#eef2ff", "#405080"),
    ("10 03578", "Bara 4×7", BARA_W, 90, "#d0d0d0", "#606060"),
    ("10 00258", "MKS-03", 36, 90, "#fff0c8", "#806020"),
    ("10 04538", "G9SP-N20S", 130, 90, "#ffe0c0", "#804000"),
    ("10 16319", "VFD004EL", 108, 142, "#3a3a3a", "#f0a030"),
]
KSYSTEM_ROW2_M = [
    ("Yık.1", "10 01331", "LC1K09", "10 00249", "LR2K0316", True),
    ("Yık.2", "10 01331", "LC1K09", "10 00249", "LR2K0314", True),
    ("Egzoz", "10 02314", "LC1K06", "10 00244", "LR2K0306", True),
]
KSYSTEM_ROW2_H = [("Isı.1", "10 01332", "LC1K16")]
KSYSTEM_ROW2_H.append(("Isı.2", "10 01332", "LC1K16"))
KSYSTEM_ROW2_C = [
    ("10 01398", "RXM BD R1", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
    ("10 00294", "RXM 220 R2", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
    ("10 00294", "RXM 220 R3", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
]

KURSAN_ROW1 = [
    ("10 00287", "PAKO 3×63", 105, 85, "#e6d4a8", "#8a6b2a"),
    ("10 00305", "Kaçak 63A", 72, 86, "#d4e4ff", "#2a5080"),
    ("10 04732", "Aşırı 63A", 72, 86, "#d4e4ff", "#2a5080"),
    ("10 00302", "1×3 kumanda", 18, 85, "#eef2ff", "#405080"),
    ("10 01421", "1×6 sepet", 18, 85, "#eef2ff", "#405080"),
    ("10 03578", "Bara 4×7", BARA_W, 90, "#d0d0d0", "#606060"),
    ("10 00258", "MKS-03", 36, 90, "#fff0c8", "#806020"),
    ("10 01398", "RXM BD R1", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
    ("10 00294", "RXM 220 R2", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
    ("10 00294", "RXM 220 R3", RELAY[0], RELAY[1], "#d8f5d8", "#308030"),
    ("10 16319", "VFD004EL", 108, 142, "#3a3a3a", "#f0a030"),
]
KURSAN_ROW2_M = [
    ("Yık.1", "10 01331", "LC1K09", "10 01359", "LR2K0316", True),
    ("Yık.2", "10 01331", "LC1K09", "10 01359", "LR2K0316", True),
    ("Üst noz.", "10 02314", "LC1K06", "10 00244", "LR2K0306", True),
    ("Alt noz.", "10 02314", "LC1K06", "10 00244", "LR2K0306", True),
    ("Egzoz", "10 02314", "LC1K06", "10 00244", "LR2K0306", True),
    ("Yağ", "10 02314", "LC1K06", "10 00243", "LR2K0305", True),
]
KURSAN_ROW2_H = [("Isı.1", "10 01332", "LC1K16"), ("Isı.2", "10 01332", "LC1K16")]
KURSAN_ROW2_C = []  # röleler satır 1 Kürsan


def patch(html_path: Path, title, sub, r1, r2m, r2h, r2c, klem_motors):
    svg, r2b, r3b = build_svg(title, sub, r1, r2m, r2h, r2c, ROW2_MDR, klem_motors)
    section = f"""
    <section class="pano-layout">
      <h2>PANO İÇ DİZİLİM (DIN 35)</h2>
      <p class="sub">{sub}</p>
      {svg}
    </section>
"""
    html = html_path.read_text(encoding="utf-8")
    html = re.sub(r"\s*<section class=\"pano-layout\">.*?</section>\s*", "\n" + section + "\n", html, count=1, flags=re.S)
    html_path.write_text(html, encoding="utf-8")
    print(html_path.name, "row2_band", r2b, "row3_band", r3b)


def main():
    patch(
        ROOT / "0326069-KSYSTE-KBN 1B 1850" / "0326069.html",
        "0326069 KSYSTEM — KBN 1B 1850 · tava 630 mm · ray 550 mm",
        "Satır 2 bandı en yüksek parçaya (MDR 90 mm) göre; üst/alt 20 mm. Satır 1 değişmedi.",
        KSYSTEM_ROW1, KSYSTEM_ROW2_M, KSYSTEM_ROW2_H, KSYSTEM_ROW2_C,
        ["Yık.1", "Yık.2", "Egzoz"],
    )
    patch(
        ROOT / "0326072-KÜRSAN-KBN 1B 2050" / "0326072.html",
        "0326072 KÜRSAN — tava 630 mm · ray 550 mm",
        "Satır 2 bandı MDR yüksekliğine göre; üst/alt 20 mm. Bara 10 mm ray genişliği.",
        KURSAN_ROW1, KURSAN_ROW2_M, KURSAN_ROW2_H, KURSAN_ROW2_C,
        ["Yık.1", "Yık.2", "Üst", "Alt", "Egzoz", "Yağ"],
    )


if __name__ == "__main__":
    main()
