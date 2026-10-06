import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.fonttype"] = "none"
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = r"C:\Users\CKP2\OneDrive\Desktop\AI_Chatbot\docs"

C = {
    "io": "#4C72B0",
    "llm": "#8172B2",
    "tool": "#55A868",
    "decision": "#DD8452",
    "storage": "#C44E52",
    "flow": "#7A8B99",
    "auto": "#B25D9C",
}


def draw_workflow():
    fig, ax = plt.subplots(figsize=(11, 15))
    ax.set_xlim(0, 13)
    ax.set_ylim(0.6, 45)
    ax.axis("off")

    def box(cx, cy, w, h, text, color, fs=9.5):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0.06,rounding_size=0.15",
                                    linewidth=0, facecolor=color))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
                color="white", weight="bold", linespacing=1.35)

    def diamond(cx, cy, w, h, text, color, fs=9):
        ax.add_patch(plt.Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2),
                                  (cx - w / 2, cy)], closed=True, facecolor=color, linewidth=0))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
                color="white", weight="bold", linespacing=1.3)

    def arrow(p1, p2, label=None, color="#555555", off=(0.25, 0.0)):
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                     color=color, linewidth=1.5))
        if label:
            ax.text((p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1], label,
                    fontsize=9, color=color, style="italic", va="center")

    X = 6.5
    box(X, 43.5, 2.6, 1.0, "USER", C["io"])
    box(X, 41.2, 4.6, 1.2, "Telegram Bot\nReceive research request (Step 1)", C["io"])
    box(X, 38.9, 4.6, 1.2, "Set variables\nchatId + researchTopic (Step 2)", C["flow"])
    box(X, 36.5, 5.0, 1.4, "Gemini - Understand question\ncreate search query (Step 3)", C["llm"])
    box(X, 34.0, 4.6, 1.2, "Tavily Web Search\nfind candidate sources (Step 4)", C["tool"])
    box(X, 31.6, 5.0, 1.4, "Gemini - Evaluate every source\nscore + KEEP / REJECT (Step 5)", C["llm"])
    diamond(X, 28.5, 5.6, 2.6, "AI DECISION 1\nKeep or reject\neach source?", C["decision"])
    box(11.2, 28.5, 3.0, 1.2, "REJECT\nsource dropped", "#9AA0A6", fs=9)
    box(X, 25.2, 5.4, 1.4, "Iterator + filter (KEEP only)\nArray aggregator (Step 6)", C["flow"])
    diamond(X, 22.0, 6.0, 2.8, "AUTONOMOUS DECISION\nEnough sources?\n(3 or more kept)", C["decision"])

    # YES branch (left)
    box(3.0, 18.4, 4.4, 1.4, "Gemini - Write research\nintro (Step 7)", C["llm"])
    box(1.7, 15.2, 3.0, 1.3, "Google Sheets\nlog every source", C["storage"], fs=9)
    box(5.0, 15.2, 3.2, 1.3, "Text aggregator\nfull source list", C["flow"], fs=9)
    box(5.0, 12.3, 3.2, 1.2, "Google Drive\nsave notes file", C["storage"], fs=9)
    box(5.0, 9.4, 3.8, 1.3, "Telegram reply\nintro + all sources", C["io"], fs=9)

    # NO branch (right) - autonomous change of workflow
    box(10.3, 18.4, 4.4, 1.4, "AUTONOMOUS ACTION\nGemini suggests narrower topics", C["auto"], fs=9)
    box(10.3, 14.8, 4.4, 1.3, "Telegram asks user for\nmore detail", C["io"], fs=9)

    box(X, 5.0, 2.6, 1.0, "USER", C["io"])

    arrow((X, 43.0), (X, 41.85))
    arrow((X, 40.6), (X, 39.5))
    arrow((X, 38.3), (X, 37.25))
    arrow((X, 35.8), (X, 34.6))
    arrow((X, 33.4), (X, 32.35))
    arrow((X, 30.9), (X, 29.8))
    arrow((X + 2.8, 28.5), (9.7, 28.5), label="Reject", off=(-0.6, 0.6))
    arrow((X, 27.2), (X, 25.9), label="Keep")
    arrow((X, 24.5), (X, 23.4))
    arrow((X - 3.0, 22.0), (3.0, 19.1), label="Yes", off=(-0.9, 0.4))
    arrow((X + 3.0, 22.0), (10.3, 19.1), label="No", off=(0.2, 0.4))
    arrow((2.4, 17.7), (1.7, 15.85))
    arrow((3.6, 17.7), (5.0, 15.85))
    arrow((5.0, 14.55), (5.0, 12.9))
    arrow((5.0, 11.7), (5.0, 10.05))
    arrow((10.3, 17.7), (10.3, 15.45))
    ax.plot([10.3, 10.3], [14.15, 5.0], color="#555555", linewidth=1.5)
    arrow((10.3, 5.0), (X + 1.3, 5.0))
    ax.plot([5.0, 5.0], [8.75, 5.0], color="#555555", linewidth=1.5)
    arrow((5.0, 5.0), (X - 1.3, 5.0))

    leg = [("User / Telegram", C["io"]), ("Gemini LLM", C["llm"]), ("External tool", C["tool"]),
           ("Decision", C["decision"]), ("Storage", C["storage"]),
           ("Make.com logic", C["flow"]), ("Autonomous action", C["auto"])]
    ax.text(0.3, 3.45, "Legend", fontsize=10, weight="bold")
    for i, (lab, col) in enumerate(leg):
        x = 0.3 + (i % 4) * 3.2
        y = 2.85 - (i // 4) * 0.7
        ax.add_patch(FancyBboxPatch((x, y - 0.18), 0.4, 0.36,
                                    boxstyle="round,pad=0.02,rounding_size=0.05",
                                    linewidth=0, facecolor=col))
        ax.text(x + 0.55, y, lab, fontsize=8.5, va="center")

    ax.set_title("AI Research Paper Assistant Agent - Workflow Diagram (Make.com)",
                 fontsize=13, weight="bold", pad=10)
    plt.tight_layout()
    plt.savefig(OUT + r"\workflow_diagram_make.png", dpi=200, bbox_inches="tight")
    plt.savefig(OUT + r"\workflow_diagram_make.svg", bbox_inches="tight")
    plt.close(fig)


def draw_architecture():
    fig, ax = plt.subplots(figsize=(10, 8.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 15)
    ax.axis("off")

    def layer(cy, h, title, color):
        ax.add_patch(FancyBboxPatch((0.4, cy - h / 2), 11.2, h,
                                    boxstyle="round,pad=0.05,rounding_size=0.15",
                                    linewidth=1.4, edgecolor=color, facecolor=color, alpha=0.12))
        ax.text(0.75, cy + h / 2 - 0.3, title, fontsize=11.5, weight="bold", color=color, va="top")

    def node(cx, cy, w, h, text, color, fs=9.5):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                    boxstyle="round,pad=0.06,rounding_size=0.14",
                                    linewidth=0, facecolor=color))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color="white",
                weight="bold", linespacing=1.3)

    def varrow(x, y1, y2):
        ax.add_patch(FancyArrowPatch((x, y1), (x, y2), arrowstyle="<|-|>", mutation_scale=15,
                                     color="#555555", linewidth=1.6))

    layer(13.6, 1.7, "User Layer", C["io"])
    layer(11.3, 1.7, "Communication Layer - Telegram", C["io"])
    layer(8.8, 2.3, "Orchestration Layer - Make.com", "#B08D57")
    layer(5.6, 3.6, "Reasoning + Search Layer", C["llm"])
    layer(2.4, 2.0, "Storage Layer", C["storage"])

    node(6, 13.35, 3.4, 0.85, "User (student / researcher)", C["io"])
    node(6, 11.05, 4.8, 0.85, "Telegram Bot\nreceives request, sends results", C["io"])
    node(6, 8.7, 8.4, 1.1,
         "Make.com scenario: routers, iterator, filter, aggregators,\nbranching on 'enough' vs 'not enough' sources",
         "#B08D57", fs=9)
    node(3.2, 6.15, 4.8, 1.2, "Gemini LLM (Google AI)\nunderstand - evaluate - decide - write", C["llm"], fs=9.5)
    node(8.8, 6.15, 4.8, 1.2, "Tavily Web Search API\nretrieves candidate sources", C["tool"], fs=9.5)
    node(6, 4.4, 6.4, 0.85, "AI decisions: KEEP/REJECT, enough sources?, ask for detail", C["decision"], fs=9)
    node(3.2, 2.25, 4.8, 1.0, "Google Sheets\nsource + evaluation records", C["storage"], fs=9.5)
    node(8.8, 2.25, 4.8, 1.0, "Google Drive\nresearch notes file", C["storage"], fs=9.5)

    varrow(6, 12.9, 11.5)
    varrow(6, 10.6, 9.25)
    varrow(5.0, 8.15, 6.8)
    varrow(10.2, 8.15, 6.8)
    varrow(6, 5.55, 4.85)
    varrow(3.2, 3.9, 2.75)
    varrow(8.8, 3.9, 2.75)

    ax.set_title("AI Research Paper Assistant Agent - System Architecture",
                 fontsize=14, weight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(OUT + r"\architecture_diagram_make.png", dpi=200, bbox_inches="tight")
    plt.savefig(OUT + r"\architecture_diagram_make.svg", bbox_inches="tight")
    plt.close(fig)


draw_workflow()
draw_architecture()
print("saved")
