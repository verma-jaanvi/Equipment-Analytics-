import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):

        # ✅ Modern Professional Figure
        self.figure = Figure(figsize=(8, 5), dpi=100)
        super().__init__(self.figure)
        self.setParent(parent)

        # ✅ Light Theme Colors (Matches UI)
        self.bg = "#ffffff"
        self.card = "#f8fafc"
        self.grid = "#cbd5e1"
        self.text = "#0f172a"

        # ✅ Dashboard Accent Palette
        self.colors = [
            "#2563eb",  # Blue
            "#22c55e",  # Green
            "#f97316",  # Orange
            "#ef4444",  # Red
            "#a855f7",  # Purple
            "#14b8a6",  # Teal
            "#facc15",  # Yellow
        ]

    # =====================================================
    # ✅ MAIN DASHBOARD CHARTS (Bar + Pie)
    # =====================================================
    def plot_all_charts(self, summary):

        self.figure.clear()

        # ✅ Extract Equipment Type Distribution
        types = list(summary["type_distribution"].keys())
        counts = list(summary["type_distribution"].values())

        bar_colors = [self.colors[i % len(self.colors)] for i in range(len(types))]

        # ✅ Layout: Bar + Pie Side-by-Side
        ax1 = self.figure.add_subplot(121)
        ax2 = self.figure.add_subplot(122)

        # ✅ Figure Background
        self.figure.patch.set_facecolor(self.bg)

        for ax in [ax1, ax2]:
            ax.set_facecolor(self.card)
            ax.tick_params(colors=self.text)

            # Remove borders
            for spine in ax.spines.values():
                spine.set_visible(False)

        # =====================================================
        # ✅ BAR CHART
        # =====================================================
        bars = ax1.bar(
            types,
            counts,
            color=bar_colors,
            alpha=0.9,
            width=0.6
        )

        # ✅ Value Labels
        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.3,
                f"{int(height)}",
                ha="center",
                fontsize=11,
                fontweight="bold",
                color=self.text
            )

        ax1.set_title(
            "Equipment Distribution",
            fontsize=15,
            fontweight="bold",
            color=self.text,
            pad=15
        )

        ax1.set_xlabel("Equipment Type", fontsize=11, color=self.text)
        ax1.set_ylabel("Count", fontsize=11, color=self.text)

        ax1.grid(axis="y", linestyle="--", alpha=0.3, color=self.grid)
        ax1.tick_params(axis="x", rotation=25)

        # =====================================================
        # ✅ PIE CHART (DONUT STYLE)
        # =====================================================
        wedges, _, _ = ax2.pie(
            counts,
            autopct="%1.1f%%",
            startangle=90,
            colors=bar_colors,
            pctdistance=0.75,
            textprops={"fontsize": 10, "color": self.text}
        )

        # ✅ Donut Hole
        ax2.add_artist(
            plt.Circle((0, 0), 0.55, fc=self.card)
        )

        ax2.set_title(
            "Type Share (%)",
            fontsize=15,
            fontweight="bold",
            color=self.text,
            pad=15
        )

        # ✅ Legend
        ax2.legend(
            wedges,
            types,
            title="Equipment Types",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=10
        )

        # ✅ Layout Fit
        self.figure.tight_layout(pad=3)

        # ✅ Render
        self.draw()

    # =====================================================
    # ✅ BACKWARD COMPATIBILITY
    # =====================================================
    def plot_type_distribution(self, summary):
        self.plot_all_charts(summary)

    # =====================================================
    # ✅ HISTOGRAM SUPPORT
    # =====================================================
    def plot_histogram(self, values, title="Histogram"):

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        self.figure.patch.set_facecolor(self.bg)
        ax.set_facecolor(self.card)

        ax.hist(
            values,
            bins=8,
            color="#2563eb",
            alpha=0.85,
            edgecolor="white"
        )

        ax.set_title(title, fontsize=16, fontweight="bold", color=self.text, pad=15)
        ax.grid(axis="y", linestyle="--", alpha=0.3, color=self.grid)

        ax.tick_params(colors=self.text)

        for spine in ax.spines.values():
            spine.set_visible(False)

        self.figure.tight_layout()
        self.draw()