"""Generate a lightweight SVG chart without third-party plotting libraries."""
from __future__ import annotations

import csv
from pathlib import Path


def plot_results(summary_csv: Path, output_svg: Path) -> None:
    with summary_csv.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    width, height = 920, 540
    left, top, plot_w, plot_h = 230, 100, 600, 330
    bar_h, gap = 22, 18
    colors = {"completion_rate": "#3B82F6", "duplicate_side_effect_rate_on_ambiguous_non_idempotent": "#DC2626"}
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (width, height, width, height),
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="%d" y="38" font-family="Arial" font-size="23" font-weight="bold">AgentRetry: completion vs duplicate-side-effect risk</text>' % left,
        '<text x="%d" y="64" font-family="Arial" font-size="13" fill="#444">Synthetic baseline; duplicate risk denominator = ambiguous non-idempotent scenarios</text>' % left,
    ]
    for tick in range(0, 11, 2):
        x = left + plot_w * tick / 10
        svg.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#dddddd"/>' % (x, top, x, top + plot_h))
        svg.append('<text x="%.1f" y="%d" text-anchor="middle" font-family="Arial" font-size="11" fill="#444">%d%%</text>' % (x, top + plot_h + 20, tick * 10))
    for i, row in enumerate(rows):
        y = top + i * 76 + 5
        svg.append('<text x="%d" y="%d" text-anchor="end" font-family="Arial" font-size="13">%s</text>' % (left - 14, y + 24, row["policy"]))
        for j, key in enumerate(("completion_rate", "duplicate_side_effect_rate_on_ambiguous_non_idempotent")):
            value = float(row[key])
            by = y + j * (bar_h + 4)
            svg.append('<rect x="%d" y="%d" width="%.1f" height="%d" rx="3" fill="%s"/>' % (left, by, plot_w * max(0, min(1, value)), bar_h, colors[key]))
            svg.append('<text x="%.1f" y="%d" font-family="Arial" font-size="11" fill="#222">%.1f%%</text>' % (left + plot_w * max(0, min(1, value)) + 6, by + 15, value * 100))
    svg.append('<rect x="%d" y="%d" width="14" height="14" fill="%s"/>' % (left, 485, colors["completion_rate"]))
    svg.append('<text x="%d" y="497" font-family="Arial" font-size="12">Completion rate</text>' % (left + 20))
    svg.append('<rect x="%d" y="%d" width="14" height="14" fill="%s"/>' % (left + 190, 485, colors["duplicate_side_effect_rate_on_ambiguous_non_idempotent"]))
    svg.append('<text x="%d" y="497" font-family="Arial" font-size="12">Duplicate risk in ambiguous non-idempotent cases</text>' % (left + 210))
    svg.append('<text x="%d" y="526" font-family="Arial" font-size="11" fill="#555">Illustrative simulator only; not production-agent evidence.</text>' % left)
    svg.append("</svg>")
    output_svg.parent.mkdir(parents=True, exist_ok=True)
    output_svg.write_text("\n".join(svg) + "\n", encoding="utf-8")


if __name__ == "__main__":
    plot_results(Path("outputs/summary.csv"), Path("outputs/completion_vs_duplicate_risk.svg"))
