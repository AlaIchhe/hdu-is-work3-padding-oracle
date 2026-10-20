"""Generate the CBC and attack-digraph figures used in the report."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "Segoe UI",
        "font.size": 11,
        "figure.dpi": 220,
        "savefig.dpi": 220,
    }
)

NAVY = "#10243e"
BLUE = "#1f5a94"
ORANGE = "#b45309"
GREEN = "#166534"
RED = "#991b1b"
GREY = "#64748b"
LIGHT = "#f8fafc"


def box(ax, x, y, w, h, title, subtitle, edge, fill="white"):
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.18,rounding_size=0.55",
        linewidth=1.8,
        edgecolor=edge,
        facecolor=fill,
        zorder=3,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y + 0.55,
        title,
        ha="center",
        va="center",
        color=NAVY,
        fontsize=10.5,
        fontweight="bold",
        zorder=4,
    )
    ax.text(
        x,
        y - 0.8,
        subtitle,
        ha="center",
        va="center",
        color="#334155",
        fontsize=8.7,
        zorder=4,
    )
    return patch


def arrow(ax, start, end, label, *, rad=0.0, color=GREY, style="-", lx=0, ly=0):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=14,
        linewidth=1.6,
        linestyle=style,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
        zorder=2,
    )
    ax.add_patch(patch)
    if label:
        mx = (start[0] + end[0]) / 2 + lx
        my = (start[1] + end[1]) / 2 + ly
        ax.text(
            mx,
            my,
            label,
            ha="center",
            va="center",
            fontsize=7.5,
            color="#334155",
            bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.94},
            zorder=5,
        )


def make_attack_graph():
    fig, ax = plt.subplots(figsize=(12.2, 6.9))
    ax.set_xlim(-3, 117)
    ax.set_ylim(0, 66)
    ax.axis("off")

    positions = {
        "S0": (6, 56, "S0  Idle system", "no attacker influence"),
        "S1": (26, 56, "S1  Cookie captured", "IV || C in hand"),
        "S2": (46, 56, "S2  Oracle observed", "CBC + PKCS#7 detected"),
        "S3": (66, 56, "S3  Ciphertext probed", "modified predecessor block"),
        "S4": (88, 56, "S4  Padding-valid reply", "one-bit side channel"),
        "S5": (88, 37, "S5  Byte recovered", "I[j] = g XOR pad"),
        "S6": (66, 37, "S6  Block recovered", "I = D_K(C)"),
        "S7": (46, 37, "S7  Plaintext assembled", "P_i = I_i XOR C_i-1"),
        "K1": (24, 37, "K1  Information theft", "confidentiality loss"),
        "S8": (66, 19, "S8  Forgery built", "C* = I XOR P*"),
        "S9": (88, 19, "S9  Forgery accepted", "valid padding, no MAC"),
        "K2": (88, 5, "K2  Access / data changed", "integrity + authority loss"),
        "K3": (108, 37, "K3  Lockout / denial", "conditional availability loss"),
    }
    colors = {
        "S0": BLUE,
        "S1": ORANGE,
        "S2": ORANGE,
        "S3": ORANGE,
        "S4": ORANGE,
        "S5": GREEN,
        "S6": GREEN,
        "S7": GREEN,
        "S8": ORANGE,
        "S9": ORANGE,
        "K1": RED,
        "K2": RED,
        "K3": RED,
    }
    fills = {
        "S0": "#eff6ff",
        "S1": "#fff7ed",
        "S2": "#fff7ed",
        "S3": "#fff7ed",
        "S4": "#fff7ed",
        "S5": "#f0fdf4",
        "S6": "#f0fdf4",
        "S7": "#f0fdf4",
        "S8": "#fff7ed",
        "S9": "#fff7ed",
        "K1": "#fef2f2",
        "K2": "#fef2f2",
        "K3": "#fef2f2",
    }

    for key, (x, y, title, subtitle) in positions.items():
        box(ax, x, y, 17.6, 7.2, title, subtitle, colors[key], fills[key])

    arrow(ax, (14.8, 56), (17.2, 56), "network access", ly=4.1)
    arrow(ax, (34.8, 56), (37.2, 56), "GET /session", ly=4.1)
    arrow(ax, (54.8, 56), (57.2, 56), "flip + observe", ly=4.1)
    arrow(ax, (74.8, 56), (79.2, 56), "submit C' || C", ly=4.1)
    arrow(ax, (88, 52.4), (88, 40.6), "valid padding", lx=3.2)
    arrow(ax, (79.2, 37), (74.8, 37), "derive byte", ly=4.0)
    arrow(ax, (57.2, 37), (54.8, 37), "repeat / next block", ly=4.0)
    arrow(ax, (37.2, 37), (32.8, 37), "all blocks", ly=4.0)
    arrow(ax, (66, 33.4), (66, 22.6), "choose target block", lx=4.7)
    arrow(ax, (74.8, 19), (79.2, 19), "valid padding", ly=4.0)
    arrow(ax, (92.2, 15.4), (92.2, 8.6), "accepted", lx=3.2)
    arrow(ax, (96.8, 37), (99.2, 37), "probe storm", ly=4.0)

    loop = FancyArrowPatch(
        (62, 59.8),
        (70, 59.8),
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.4,
        linestyle="--",
        color=ORANGE,
        connectionstyle="arc3,rad=-0.8",
        zorder=2,
    )
    ax.add_patch(loop)
    ax.text(66, 64.2, "next guess", ha="center", va="center", fontsize=7.5, color=ORANGE)

    legend_y = 0.8
    for x, color, text in (
        (7, BLUE, "normal"),
        (23, ORANGE, "attacker / oracle"),
        (45, GREEN, "recovered secret"),
        (67, RED, "loss state"),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x, legend_y - 0.7),
                2.2,
                1.4,
                boxstyle="round,pad=0.1,rounding_size=0.25",
                facecolor="white",
                edgecolor=color,
                linewidth=1.4,
            )
        )
        ax.text(x + 3, legend_y, text, va="center", ha="left", fontsize=8, color="#334155")

    ax.text(
        108,
        62,
        "Every edge is an action or an observable system response.",
        ha="right",
        va="center",
        fontsize=8.5,
        color="#475569",
    )
    fig.tight_layout(pad=0.2)
    output = ASSETS / "attack-digraph.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {output}")


def make_cbc_diagram():
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 48)
    ax.axis("off")

    blocks = [("IV", 16, "#64748b"), ("C0", 38, NAVY), ("C1", 60, NAVY), ("C2", 82, NAVY)]
    for label, x, color in blocks:
        ax.add_patch(
            FancyBboxPatch(
                (x - 7, 38),
                14,
                5.5,
                boxstyle="round,pad=0.15,rounding_size=0.5",
                facecolor="white",
                edgecolor=color,
                linewidth=2,
            )
        )
        ax.text(x, 40.75, label, ha="center", va="center", fontsize=12, fontweight="bold", color=color)

    for x, cipher in ((38, "C0"), (60, "C1"), (82, "C2")):
        ax.add_patch(
            FancyBboxPatch(
                (x - 7, 22),
                14,
                6.5,
                boxstyle="round,pad=0.15,rounding_size=0.45",
                facecolor="#eff6ff",
                edgecolor=BLUE,
                linewidth=1.6,
            )
        )
        ax.text(x, 25.25, f"$D_K$({cipher})", ha="center", va="center", fontsize=10, color=NAVY)
        ax.annotate(
            "",
            xy=(x, 28.7),
            xytext=(x, 37.8),
            arrowprops={"arrowstyle": "-|>", "lw": 1.5, "color": GREY},
        )
        ax.add_patch(
            plt.Circle((x, 15.3), 1.65, fill=False, edgecolor=ORANGE, linewidth=1.6)
        )
        ax.text(x, 15.3, "XOR", ha="center", va="center", fontsize=7.4, color=ORANGE, fontweight="bold")
        ax.annotate(
            "",
            xy=(x, 16.95),
            xytext=(x, 21.8),
            arrowprops={"arrowstyle": "-|>", "lw": 1.5, "color": GREY},
        )

    for source, target, label in (
        (16, 38, "IV"),
        (38, 60, "C0"),
        (60, 82, "C1"),
    ):
        ax.annotate(
            "",
            xy=(target - 1.8, 15.3),
            xytext=(source + 7.2, 15.3),
            arrowprops={"arrowstyle": "-|>", "lw": 1.5, "color": GREY, "connectionstyle": "arc3,rad=0"},
        )

    for x, label in ((38, "P0"), (60, "P1"), (82, "P2")):
        ax.add_patch(
            FancyBboxPatch(
                (x - 7, 4),
                14,
                5.5,
                boxstyle="round,pad=0.15,rounding_size=0.5",
                facecolor="#f0fdf4",
                edgecolor=GREEN,
                linewidth=1.8,
            )
        )
        ax.text(x, 6.75, label, ha="center", va="center", fontsize=12, fontweight="bold", color=GREEN)
        ax.annotate(
            "",
            xy=(x, 9.7),
            xytext=(x, 13.6),
            arrowprops={"arrowstyle": "-|>", "lw": 1.5, "color": GREY},
        )

    ax.text(50, 0.8, "$P_i = D_K(C_i) \\oplus C_{i-1}$", ha="center", va="center", fontsize=14, color=NAVY)
    fig.tight_layout(pad=0.2)
    output = ASSETS / "cbc-decryption.png"
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {output}")


if __name__ == "__main__":
    make_attack_graph()
    make_cbc_diagram()
