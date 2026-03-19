from manim import *
import numpy as np

# ------------------------------------------------------------
# Manim CE video: Correlation, Covariance, Correlation Coefficient
# Language: Mongolian
# Target duration: ~3 minutes (180 seconds)
# Based on textbook Chapter 2.1 "Корреляци"
#
# Features:
# - Detailed paper-style worked example with calculation table (A dataset)
# - Step-by-step practice problem (B dataset)
# - Visual scatter plots with trend lines
# - Formula explanations with color coding
# ------------------------------------------------------------

config.background_color = "#1a1a2e"

FONT = "Segoe UI"
X_COLOR = "#4fc3f7"      # light blue
Y_COLOR = "#ffb74d"      # warm orange
POS_COLOR = "#66bb6a"    # green
NEG_COLOR = "#ef5350"    # red
NEUTRAL_COLOR = "#9e9e9e"  # gray
DOT_COLOR = "#80deea"    # cyan dots
ACCENT = "#ce93d8"       # purple accent
TITLE_COLOR = "#e1bee7"  # light purple
TEXT_COLOR = "#e0e0e0"   # light gray text
FORMULA_COLOR = "#ffffff"
CARD_BG = "#16213e"
CARD_BORDER = "#0f3460"
HIGHLIGHT = "#ffd54f"    # yellow highlight


def mn_text(text, size=30, color=None, weight=NORMAL):
    if color is None:
        color = TEXT_COLOR
    return Text(text, font=FONT, font_size=size, color=color, weight=weight)


def section_header(text):
    """Create a styled section header with underline accent."""
    header = mn_text(text, size=36, color=TITLE_COLOR, weight=BOLD)
    underline = Line(LEFT * 2.5, RIGHT * 2.5, color=ACCENT, stroke_width=3)
    underline.next_to(header, DOWN, buff=0.1)
    return VGroup(header, underline)


def build_axes(x_range=(0, 100, 25), y_range=(0, 100, 25),
               x_length=4.8, y_length=4.2,
               x_label="X", y_label="Y"):
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={
            "color": TEXT_COLOR,
            "include_numbers": True,
            "font_size": 20,
            "numbers_to_exclude": [],
        },
        tips=False,
    )
    xl = axes.get_x_axis_label(
        mn_text(x_label, size=22, color=X_COLOR), edge=RIGHT, direction=DOWN
    )
    yl = axes.get_y_axis_label(
        mn_text(y_label, size=22, color=Y_COLOR), edge=UP, direction=LEFT
    )
    return VGroup(axes, xl, yl)


def scatter_dots(axes, xs, ys, color=DOT_COLOR, radius=0.055):
    return VGroup(*[
        Dot(axes.c2p(x, y), radius=radius, color=color,
            fill_opacity=0.9)
        for x, y in zip(xs, ys)
    ])


def make_card(width=4.0, height=4.5, fill_color=CARD_BG, border_color=CARD_BORDER):
    return RoundedRectangle(
        corner_radius=0.15, width=width, height=height,
        fill_color=fill_color, fill_opacity=0.85,
        stroke_color=border_color, stroke_width=2,
    )


# ── Datasets from textbook (Table 1) ──
A_X = [35, 80, 45, 85, 95, 67, 52, 59, 73, 70]
A_Y = [50, 90, 38, 68, 88, 80, 70, 54, 69, 45]

B_X = [10, 18, 26, 34, 42, 50, 58, 66, 74, 82]
B_Y = [90, 79, 79, 55, 60, 55, 50, 40, 25, 10]

C_X = [10, 70, 24, 71, 87, 70, 30, 41, 43, 19]
C_Y = [31, 46, 53, 70, 74, 19, 60, 11, 48, 25]


class CorrelationVideo(Scene):
    """
    Full 3-minute educational video on Correlation.
    Scenes are designed to total ~180 seconds of animation + wait time.
    """

    def construct(self):
        # Scene 1: Title & hook                          ~7s
        self.scene1_title()
        # Scene 2: What is bivariate data?               ~10s
        self.scene2_two_variables()
        # Scene 3: Types of correlation (3 plots)        ~15s
        self.scene3_types_of_correlation()
        # Scene 4: Mean point & quadrants                ~12s
        self.scene4_mean_point()
        # Scene 5: Covariance concept & formula          ~15s
        self.scene5_covariance()
        # Scene 6: Correlation coefficient formula       ~13s
        self.scene6_correlation_coefficient()
        # Scene 7: Detailed paper example A (table)      ~25s
        self.scene7_paper_example_A()
        # Scene 8: Practice problem B (step by step)     ~22s
        self.scene8_practice_B()
        # Scene 9: Interpreting r values                 ~10s
        self.scene9_interpretation()
        # Scene 10: Summary & closing                    ~8s
        self.scene10_summary()

    # ── helpers ──────────────────────────────────────────────

    def clear_scene(self, t=0.6):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=t)

    def add_progress_bar(self, fraction):
        """Small progress indicator at bottom."""
        bar_bg = Rectangle(width=12, height=0.06, fill_color=GRAY,
                           fill_opacity=0.3, stroke_width=0).to_edge(DOWN, buff=0.08)
        bar_fg = Rectangle(width=12 * fraction, height=0.06,
                           fill_color=ACCENT, fill_opacity=0.7,
                           stroke_width=0).to_edge(DOWN, buff=0.08).align_to(bar_bg, LEFT)
        return VGroup(bar_bg, bar_fg)

    # ── SCENE 1: Title ─────────────────────────────────── ~10s

    def scene1_title(self):
        # Chapter badge
        badge = RoundedRectangle(
            corner_radius=0.12, width=2.0, height=0.5,
            fill_color=ACCENT, fill_opacity=0.3,
            stroke_color=ACCENT, stroke_width=1.5,
        )
        badge_text = mn_text("2.1", size=24, color=ACCENT)
        badge_text.move_to(badge)
        badge_group = VGroup(badge, badge_text).to_edge(UP, buff=0.8)

        title = mn_text("Корреляци", size=52, color=WHITE, weight=BOLD)
        subtitle = mn_text(
            "Хоёр хувьсагчийн хамаарлыг хэрхэн хэмжих вэ?",
            size=28, color=ACCENT
        )
        group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)

        self.play(FadeIn(badge_group, shift=DOWN * 0.3), run_time=0.7)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.play(Write(subtitle), run_time=1.2)
        self.wait(2.0)
        self.clear_scene()

    # ── SCENE 2: Bivariate data ────────────────────────── ~14s

    def scene2_two_variables(self):
        header = section_header("Хоёр хэмжээст өгөгдөл")
        header.to_edge(UP, buff=0.4)

        # Explanation
        ex1 = mn_text("• Нэг ангийн 10 оюутан", size=26)
        ex2 = mn_text("• X = Математикийн оноо", size=26, color=X_COLOR)
        ex3 = mn_text("• Y = Япон хэлний оноо", size=26, color=Y_COLOR)
        exg = VGroup(ex1, ex2, ex3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        exg.next_to(header, DOWN, buff=0.35).to_edge(LEFT, buff=1.2)

        # Build a graph
        graph = build_axes(x_length=5.0, y_length=3.8)
        axes = graph[0]
        graph.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.5)
        dots = scatter_dots(axes, A_X, A_Y)

        label = mn_text(
            "Цэгэн диаграмм (scatter plot)",
            size=24, color=HIGHLIGHT
        ).next_to(graph, DOWN, buff=0.25)

        self.play(Write(header), run_time=0.8)
        self.play(LaggedStart(FadeIn(ex1), FadeIn(ex2), FadeIn(ex3),
                              lag_ratio=0.25), run_time=1.5)
        self.play(Create(axes), FadeIn(graph[1], graph[2]), run_time=0.8)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08),
            run_time=1.5
        )
        self.play(FadeIn(label, shift=UP * 0.2), run_time=0.7)
        self.wait(2.5)
        self.clear_scene()

    # ── SCENE 3: Types of correlation ──────────────────── ~22s

    def _mini_scatter(self, title_str, xs, ys, label_str, label_color,
                      line_type="none"):
        card = make_card(width=4.0, height=4.6)
        title = mn_text(title_str, size=24, weight=BOLD, color=WHITE)
        title.next_to(card.get_top(), DOWN, buff=0.18)

        g = build_axes(x_length=3.0, y_length=2.6)
        g.move_to(card.get_center() + DOWN * 0.1)
        ax = g[0]
        dots = scatter_dots(ax, xs, ys, radius=0.045)

        extras = VGroup()
        if line_type == "positive":
            extras.add(
                Line(ax.c2p(20, 35), ax.c2p(90, 85),
                     color=POS_COLOR, stroke_width=2.5)
            )
        elif line_type == "negative":
            extras.add(
                Line(ax.c2p(15, 88), ax.c2p(85, 15),
                     color=NEG_COLOR, stroke_width=2.5)
            )

        lbl = mn_text(label_str, size=20, color=label_color)
        lbl.next_to(card.get_bottom(), UP, buff=0.15)

        return VGroup(card, title, g, dots, extras, lbl)

    def scene3_types_of_correlation(self):
        header = section_header("Корреляцийн төрлүүд")
        header.to_edge(UP, buff=0.35)

        g1 = self._mini_scatter("(A)", A_X, A_Y, "Эерэг корреляци",
                                POS_COLOR, "positive")
        g2 = self._mini_scatter("(B)", B_X, B_Y, "Сөрөг корреляци",
                                NEG_COLOR, "negative")
        g3 = self._mini_scatter("(C)", C_X, C_Y, "Хамааралгүй",
                                NEUTRAL_COLOR, "none")
        plots = VGroup(g1, g2, g3).arrange(RIGHT, buff=0.35).scale(0.82)
        plots.next_to(header, DOWN, buff=0.35)

        note1 = mn_text("X ↑  Y ↑  →  эерэг", size=22, color=POS_COLOR)
        note2 = mn_text("X ↑  Y ↓  →  сөрөг", size=22, color=NEG_COLOR)
        note3 = mn_text("Тодорхой хандлагагүй  →  хамааралгүй", size=22,
                         color=NEUTRAL_COLOR)
        notes = VGroup(note1, note2, note3).arrange(DOWN, aligned_edge=LEFT,
                                                     buff=0.12)
        notes.to_edge(DOWN, buff=0.3)

        self.play(Write(header), run_time=0.8)
        self.play(
            LaggedStart(
                FadeIn(g1, shift=UP * 0.3),
                FadeIn(g2, shift=UP * 0.3),
                FadeIn(g3, shift=UP * 0.3),
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )
        self.wait(2.0)
        self.play(
            LaggedStart(FadeIn(note1), FadeIn(note2), FadeIn(note3),
                        lag_ratio=0.25),
            run_time=1.5,
        )
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 4: Mean point & quadrants ────────────────── ~18s

    def scene4_mean_point(self):
        header = section_header("Дундаж цэг ба 4 квадрант")
        header.to_edge(UP, buff=0.35)

        graph = build_axes(x_length=6.0, y_length=4.6)
        graph.next_to(header, DOWN, buff=0.3).shift(LEFT * 0.5)
        axes = graph[0]
        dots = scatter_dots(axes, A_X, A_Y, radius=0.06)

        xbar, ybar = 66.1, 65.2
        mean_dot = Dot(axes.c2p(xbar, ybar), color=HIGHLIGHT, radius=0.09)
        mean_label = MathTex(r"(\bar{x}, \bar{y})", color=HIGHLIGHT,
                             font_size=28).next_to(mean_dot, UR, buff=0.1)

        vline = DashedLine(
            axes.c2p(xbar, 0), axes.c2p(xbar, 100),
            color=HIGHLIGHT, stroke_width=1.5, dash_length=0.08
        )
        hline = DashedLine(
            axes.c2p(0, ybar), axes.c2p(100, ybar),
            color=HIGHLIGHT, stroke_width=1.5, dash_length=0.08
        )

        # Quadrant labels
        q1 = mn_text("+", size=30, color=POS_COLOR).move_to(
            axes.c2p(83, 83))
        q2 = mn_text("−", size=30, color=NEG_COLOR).move_to(
            axes.c2p(40, 83))
        q3 = mn_text("+", size=30, color=POS_COLOR).move_to(
            axes.c2p(40, 40))
        q4 = mn_text("−", size=30, color=NEG_COLOR).move_to(
            axes.c2p(83, 40))

        side_note = VGroup(
            mn_text("(xᵢ−x̄)(yᵢ−ȳ)", size=22, color=WHITE),
            mn_text("нь квадрант бүрт", size=22),
            mn_text("+ эсвэл − утгатай", size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        side_note.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)

        self.play(Write(header), run_time=0.7)
        self.play(Create(axes), FadeIn(graph[1], graph[2]), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.8) for d in dots], lag_ratio=0.05),
            run_time=1.0,
        )
        self.play(
            Create(vline), Create(hline),
            FadeIn(mean_dot), Write(mean_label),
            run_time=1.0,
        )
        self.play(FadeIn(q1, q2, q3, q4), run_time=0.8)
        self.play(FadeIn(side_note), run_time=0.8)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 5: Covariance ────────────────────────────── ~22s

    def scene5_covariance(self):
        header = section_header("Ковариац")
        header.to_edge(UP, buff=0.35)

        # Main formula
        formula = MathTex(
            r"c_{xy}", r"=", r"\frac{1}{n}",
            r"\sum_{i=1}^{n}", r"(x_i - \bar{x})", r"(y_i - \bar{y})",
            color=FORMULA_COLOR, font_size=40,
        ).next_to(header, DOWN, buff=0.45)
        # color-code parts
        formula[0].set_color(ACCENT)
        formula[4].set_color(X_COLOR)
        formula[5].set_color(Y_COLOR)

        # Alternative formula
        alt = MathTex(
            r"c_{xy} = \overline{xy} - \bar{x}\cdot\bar{y}",
            color=FORMULA_COLOR, font_size=36,
        ).next_to(formula, DOWN, buff=0.4)

        # Interpretation
        card1 = make_card(width=5.0, height=1.2)
        card1_text = mn_text("cₓᵧ > 0 → X, Y хамт өсдөг",
                             size=24, color=POS_COLOR)
        card1_text.move_to(card1)
        cg1 = VGroup(card1, card1_text)

        card2 = make_card(width=5.0, height=1.2)
        card2_text = mn_text("cₓᵧ < 0 → X өсөж Y буурдаг",
                             size=24, color=NEG_COLOR)
        card2_text.move_to(card2)
        cg2 = VGroup(card2, card2_text)

        cards = VGroup(cg1, cg2).arrange(RIGHT, buff=0.4)
        cards.next_to(alt, DOWN, buff=0.45)

        note = mn_text(
            "Гэхдээ ковариац нь нэгж хэмжээнээс хамаарна!",
            size=22, color=HIGHLIGHT,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(header), run_time=0.7)
        self.play(Write(formula), run_time=2.0)
        self.wait(1.0)
        self.play(FadeIn(alt, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeIn(cg1, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(cg2, shift=UP * 0.2), run_time=0.7)
        self.play(Write(note), run_time=0.8)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 6: Correlation coefficient ───────────────── ~20s

    def scene6_correlation_coefficient(self):
        header = section_header("Корреляцийн коэффициент")
        header.to_edge(UP, buff=0.35)

        formula = MathTex(
            r"r_{xy}", r"=", r"\frac{c_{xy}}{s_x \cdot s_y}",
            r"=",
            r"\frac{\overline{xy} - \bar{x}\bar{y}}"
            r"{\sqrt{\overline{x^2}-\bar{x}^2}"
            r"\cdot\sqrt{\overline{y^2}-\bar{y}^2}}",
            color=FORMULA_COLOR, font_size=36,
        ).next_to(header, DOWN, buff=0.45)
        formula[0].set_color(ACCENT)

        # Scale explanation
        scale_line = NumberLine(
            x_range=[-1, 1, 0.5],
            length=8,
            include_numbers=True,
            color=TEXT_COLOR,
            font_size=22,
        ).shift(DOWN * 0.5)

        minus_lbl = mn_text("Сөрөг", size=16, color=NEG_COLOR)
        minus_lbl.next_to(scale_line.n2p(-0.75), DOWN, buff=0.45)
        zero_lbl = mn_text("Сул", size=16, color=NEUTRAL_COLOR)
        zero_lbl.next_to(scale_line.n2p(0), DOWN, buff=0.65)
        plus_lbl = mn_text("Эерэг", size=16, color=POS_COLOR)
        plus_lbl.next_to(scale_line.n2p(0.75), DOWN, buff=0.45)

        # Bullet points
        bullets = VGroup(
            mn_text("• −1 ≤ r ≤ 1", size=24, color=WHITE),
            mn_text("• |r| ≥ 0.7  →  хүчтэй хамааралтай", size=23),
            mn_text("• |r| < 0.2  →  сул хамааралтай", size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        bullets.to_edge(DOWN, buff=0.35)

        self.play(Write(header), run_time=0.7)
        self.play(Write(formula), run_time=2.0)
        self.wait(1.0)
        self.play(Create(scale_line), run_time=0.8)
        self.play(FadeIn(minus_lbl), FadeIn(zero_lbl), FadeIn(plus_lbl),
                  run_time=0.7)
        self.play(FadeIn(bullets), run_time=1.0)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 7: Detailed Paper Example A ─────────────── ~35s

    def scene7_paper_example_A(self):
        """
        Цаасны бодлого: (A) датасэт дээр дэлгэрэнгүй хүснэгтээр бодох
        """
        # Part 1: Problem statement
        header = section_header("Бодлого: (A) өгөгдлийн корреляци")
        header.to_edge(UP, buff=0.3)

        problem_text = VGroup(
            mn_text("10 оюутны математик (X) ба япон хэл (Y)-ийн оноо өгөгдөв.", size=22),
            mn_text("Корреляцийн коэффициент rₓᵧ -ийг ол.", size=22, color=HIGHLIGHT),
        ).arrange(DOWN, buff=0.1)
        problem_text.next_to(header, DOWN, buff=0.25)

        self.play(Write(header), run_time=0.7)
        self.play(FadeIn(problem_text), run_time=0.8)
        self.wait(2.0)

        # Part 2: Show data table
        self.play(FadeOut(problem_text), run_time=0.4)

        # Create proper data table
        table_header = VGroup(
            mn_text("№", size=18, color=NEUTRAL_COLOR),
            mn_text("X", size=18, color=X_COLOR),
            mn_text("Y", size=18, color=Y_COLOR),
            mn_text("X²", size=18, color=X_COLOR),
            mn_text("Y²", size=18, color=Y_COLOR),
            mn_text("XY", size=18, color=ACCENT),
        ).arrange(RIGHT, buff=0.5)
        table_header.next_to(header, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)

        # Table data rows
        rows = VGroup()
        x_vals = A_X
        y_vals = A_Y
        for i in range(10):
            row = VGroup(
                mn_text(f"{i+1}", size=16, color=NEUTRAL_COLOR),
                mn_text(f"{x_vals[i]}", size=16, color=X_COLOR),
                mn_text(f"{y_vals[i]}", size=16, color=Y_COLOR),
                mn_text(f"{x_vals[i]**2}", size=16, color=X_COLOR),
                mn_text(f"{y_vals[i]**2}", size=16, color=Y_COLOR),
                mn_text(f"{x_vals[i]*y_vals[i]}", size=16, color=ACCENT),
            ).arrange(RIGHT, buff=0.5)
            rows.add(row)
        rows.arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        rows.next_to(table_header, DOWN, buff=0.15, aligned_edge=LEFT)

        # Sum row
        sum_x = sum(x_vals)
        sum_y = sum(y_vals)
        sum_x2 = sum(x**2 for x in x_vals)
        sum_y2 = sum(y**2 for y in y_vals)
        sum_xy = sum(x*y for x, y in zip(x_vals, y_vals))

        sum_line = Line(LEFT * 3, RIGHT * 3, color=HIGHLIGHT, stroke_width=1.5)
        sum_line.next_to(rows, DOWN, buff=0.1)

        sum_row = VGroup(
            mn_text("Σ", size=18, color=HIGHLIGHT, weight=BOLD),
            mn_text(f"{sum_x}", size=18, color=X_COLOR, weight=BOLD),
            mn_text(f"{sum_y}", size=18, color=Y_COLOR, weight=BOLD),
            mn_text(f"{sum_x2}", size=18, color=X_COLOR, weight=BOLD),
            mn_text(f"{sum_y2}", size=18, color=Y_COLOR, weight=BOLD),
            mn_text(f"{sum_xy}", size=18, color=ACCENT, weight=BOLD),
        ).arrange(RIGHT, buff=0.5)
        sum_row.next_to(sum_line, DOWN, buff=0.1, aligned_edge=LEFT)

        table_group = VGroup(table_header, rows, sum_line, sum_row)
        table_group.scale(0.85).next_to(header, DOWN, buff=0.3)

        self.play(FadeIn(table_header), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=0.08),
            run_time=1.5,
        )
        self.play(Create(sum_line), FadeIn(sum_row), run_time=0.8)
        self.wait(2.5)
        self.clear_scene(0.5)

        # Part 3: Calculations step by step
        header2 = section_header("Алхам алхмаар бодолт")
        header2.to_edge(UP, buff=0.35)

        # Step 1: Means
        step1_title = mn_text("Алхам 1: Дундажуудыг ол", size=24, color=HIGHLIGHT, weight=BOLD)
        step1_calc = VGroup(
            MathTex(r"\bar{x} = \frac{\Sigma x}{n} = \frac{661}{10} = 66.1",
                    color=FORMULA_COLOR, font_size=28),
            MathTex(r"\bar{y} = \frac{\Sigma y}{n} = \frac{652}{10} = 65.2",
                    color=FORMULA_COLOR, font_size=28),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        step1 = VGroup(step1_title, step1_calc).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Step 2: Variances (squared means)
        step2_title = mn_text("Алхам 2: x², y², xy-ийн дундаж", size=24, color=HIGHLIGHT, weight=BOLD)
        step2_calc = VGroup(
            MathTex(r"\overline{x^2} = \frac{47019}{10} = 4701.9",
                    color=FORMULA_COLOR, font_size=26),
            MathTex(r"\overline{y^2} = \frac{45174}{10} = 4517.4",
                    color=FORMULA_COLOR, font_size=26),
            MathTex(r"\overline{xy} = \frac{45173}{10} = 4517.3",
                    color=FORMULA_COLOR, font_size=26),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        step2 = VGroup(step2_title, step2_calc).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        steps_group = VGroup(step1, step2).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        steps_group.next_to(header2, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)

        self.play(Write(header2), run_time=0.6)
        self.play(FadeIn(step1_title), run_time=0.5)
        self.play(Write(step1_calc), run_time=1.5)
        self.wait(1.5)
        self.play(FadeIn(step2_title), run_time=0.5)
        self.play(Write(step2_calc), run_time=1.5)
        self.wait(2.0)
        self.clear_scene(0.5)

        # Part 4: Final calculation
        header3 = section_header("Корреляцийн коэффициент")
        header3.to_edge(UP, buff=0.35)

        # Step 3: Covariance
        step3_title = mn_text("Алхам 3: Ковариац", size=24, color=HIGHLIGHT, weight=BOLD)
        step3_formula = MathTex(
            r"c_{xy} = \overline{xy} - \bar{x}\bar{y}",
            color=FORMULA_COLOR, font_size=30
        )
        step3_calc = MathTex(
            r"c_{xy} = 4517.3 - 66.1 \times 65.2 = 4517.3 - 4309.72 = 207.58",
            color=FORMULA_COLOR, font_size=28
        )
        step3 = VGroup(step3_title, step3_formula, step3_calc).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # Step 4: Standard deviations
        step4_title = mn_text("Алхам 4: Стандарт хазайлт", size=24, color=HIGHLIGHT, weight=BOLD)
        step4_calc = VGroup(
            MathTex(r"s_x = \sqrt{\overline{x^2} - \bar{x}^2} = \sqrt{4701.9 - 66.1^2} = \sqrt{311.09} = 17.64",
                    color=FORMULA_COLOR, font_size=24),
            MathTex(r"s_y = \sqrt{\overline{y^2} - \bar{y}^2} = \sqrt{4517.4 - 65.2^2} = \sqrt{266.36} = 16.32",
                    color=FORMULA_COLOR, font_size=24),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        step4 = VGroup(step4_title, step4_calc).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        # Step 5: Correlation coefficient
        r_a_val = float(np.corrcoef(A_X, A_Y)[0, 1])
        step5_title = mn_text("Алхам 5: Корреляцийн коэффициент", size=24, color=HIGHLIGHT, weight=BOLD)
        step5_formula = MathTex(
            r"r_{xy} = \frac{c_{xy}}{s_x \cdot s_y} = \frac{207.58}{17.64 \times 16.32} = \frac{207.58}{287.93}",
            color=FORMULA_COLOR, font_size=28
        )
        step5_result = MathTex(
            rf"r_{{xy}} \approx {r_a_val:.2f}",
            color=POS_COLOR, font_size=40
        )
        step5 = VGroup(step5_title, step5_formula, step5_result).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        all_steps = VGroup(step3, step4, step5).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        all_steps.scale(0.8).next_to(header3, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)

        # Conclusion box
        conclusion_box = make_card(width=10, height=1.3)
        conclusion_box.to_edge(DOWN, buff=0.25)
        conclusion_text = VGroup(
            mn_text(f"Хариу: r = {r_a_val:.2f}", size=26, color=WHITE, weight=BOLD),
            mn_text("→ Нэлээд хүчтэй эерэг хамааралтай (0.7-оос их)", size=22, color=POS_COLOR),
        ).arrange(DOWN, buff=0.1)
        conclusion_text.move_to(conclusion_box)

        self.play(Write(header3), run_time=0.6)
        self.play(FadeIn(step3), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(step4), run_time=1.2)
        self.wait(1.0)
        self.play(FadeIn(step5), run_time=1.2)

        result_box = SurroundingRectangle(step5_result, color=POS_COLOR, buff=0.12, corner_radius=0.1)
        self.play(Create(result_box), run_time=0.6)
        self.play(FadeIn(conclusion_box), Write(conclusion_text), run_time=1.0)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 8: Practice Problem B ─────────────────────── ~30s

    def scene8_practice_B(self):
        """
        Дасгал бодлого: (B) датасэт дээр оюутанд зориулсан бодолт
        """
        # Part 1: Present the problem
        header = section_header("Дасгал бодлого: (B) өгөгдөл")
        header.to_edge(UP, buff=0.35)

        problem_card = make_card(width=12, height=2.0)
        problem_card.next_to(header, DOWN, buff=0.3)
        problem_text = VGroup(
            mn_text("Дараах (B) өгөгдлийн корреляцийн коэффициентийг ол:", size=22),
            mn_text("X: 10  18  26  34  42  50  58  66  74  82", size=20, color=X_COLOR),
            mn_text("Y: 90  79  79  55  60  55  50  40  25  10", size=20, color=Y_COLOR),
        ).arrange(DOWN, buff=0.15)
        problem_text.move_to(problem_card)

        think_text = mn_text("Эхлээд бодож үзээрэй! 🤔", size=26, color=HIGHLIGHT)
        think_text.next_to(problem_card, DOWN, buff=0.5)

        self.play(Write(header), run_time=0.6)
        self.play(FadeIn(problem_card), Write(problem_text), run_time=1.0)
        self.play(FadeIn(think_text), run_time=0.6)
        self.wait(2.5)
        self.play(FadeOut(think_text), run_time=0.4)

        # Part 2: Show solution step by step
        solution_title = mn_text("Бодолт:", size=28, color=HIGHLIGHT, weight=BOLD)
        solution_title.next_to(problem_card, DOWN, buff=0.3).to_edge(LEFT, buff=0.8)

        # Pre-compute values
        bx = np.array(B_X, dtype=float)
        by = np.array(B_Y, dtype=float)
        n = len(bx)
        sum_x = bx.sum()
        sum_y = by.sum()
        sum_x2 = (bx**2).sum()
        sum_y2 = (by**2).sum()
        sum_xy = (bx * by).sum()
        xbar = bx.mean()
        ybar = by.mean()
        x2bar = (bx**2).mean()
        y2bar = (by**2).mean()
        xybar = (bx * by).mean()
        cov = xybar - xbar * ybar
        sx = np.sqrt(x2bar - xbar**2)
        sy = np.sqrt(y2bar - ybar**2)
        r = cov / (sx * sy)

        # Step 1: Sums and means
        calc1 = VGroup(
            MathTex(rf"\Sigma x = {int(sum_x)}, \quad \Sigma y = {int(sum_y)}",
                    color=FORMULA_COLOR, font_size=24),
            MathTex(rf"\bar{{x}} = {xbar:.1f}, \quad \bar{{y}} = {ybar:.1f}",
                    color=FORMULA_COLOR, font_size=24),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)

        # Step 2: Squared sums
        calc2 = VGroup(
            MathTex(rf"\Sigma x^2 = {int(sum_x2)}, \quad \Sigma y^2 = {int(sum_y2)}, \quad \Sigma xy = {int(sum_xy)}",
                    color=FORMULA_COLOR, font_size=22),
        )

        # Step 3: Covariance
        calc3 = MathTex(
            rf"c_{{xy}} = {xybar:.1f} - {xbar:.1f} \times {ybar:.1f} = {cov:.2f}",
            color=FORMULA_COLOR, font_size=24
        )

        # Step 4: Standard deviations
        calc4 = MathTex(
            rf"s_x = {sx:.2f}, \quad s_y = {sy:.2f}",
            color=FORMULA_COLOR, font_size=24
        )

        # Step 5: Final result
        calc5 = MathTex(
            rf"r_{{xy}} = \frac{{{cov:.2f}}}{{{sx:.2f} \times {sy:.2f}}} = {r:.2f}",
            color=NEG_COLOR, font_size=32
        )

        all_calcs = VGroup(calc1, calc2, calc3, calc4, calc5).arrange(
            DOWN, buff=0.18, aligned_edge=LEFT
        )
        all_calcs.scale(0.9).next_to(solution_title, DOWN, buff=0.2, aligned_edge=LEFT)

        self.play(Write(solution_title), run_time=0.5)
        self.play(FadeIn(calc1), run_time=0.8)
        self.play(FadeIn(calc2), run_time=0.8)
        self.play(FadeIn(calc3), run_time=0.8)
        self.play(FadeIn(calc4), run_time=0.8)
        self.play(FadeIn(calc5), run_time=1.0)

        result_box = SurroundingRectangle(calc5, color=NEG_COLOR, buff=0.12, corner_radius=0.1)
        self.play(Create(result_box), run_time=0.6)

        # Part 3: Show scatter plot with interpretation
        graph = build_axes(x_length=4.5, y_length=3.5)
        axes = graph[0]
        graph.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.0)
        dots = scatter_dots(axes, B_X, B_Y, radius=0.05)
        trend = Line(axes.c2p(10, 88), axes.c2p(85, 15), color=NEG_COLOR, stroke_width=2.5)

        self.play(Create(axes), FadeIn(graph[1], graph[2]), run_time=0.7)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.06),
            run_time=0.8
        )
        self.play(Create(trend), run_time=0.5)

        # Conclusion
        conclusion = mn_text(
            f"Хариу: r ≈ {r:.2f} → Хүчтэй сөрөг хамааралтай!",
            size=24, color=NEG_COLOR, weight=BOLD
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(conclusion), run_time=0.8)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 9: Interpreting r values ─────────────────── ~14s

    def scene9_interpretation(self):
        header = section_header("r-ийн утгыг хэрхэн ойлгох вэ?")
        header.to_edge(UP, buff=0.35)

        # Visual scale
        scale = NumberLine(
            x_range=[-1, 1, 0.25],
            length=10,
            include_numbers=True,
            color=TEXT_COLOR,
            font_size=20,
        ).shift(UP * 0.5)

        # Gradient colored regions
        regions = VGroup()
        # Strong negative
        r1 = Rectangle(width=2.5, height=0.3, fill_color=NEG_COLOR,
                        fill_opacity=0.4, stroke_width=0)
        r1.move_to(scale.n2p(-0.75)).shift(UP * 0.3)
        # Weak
        r2 = Rectangle(width=5.0, height=0.3, fill_color=NEUTRAL_COLOR,
                        fill_opacity=0.3, stroke_width=0)
        r2.move_to(scale.n2p(0)).shift(UP * 0.3)
        # Strong positive
        r3 = Rectangle(width=2.5, height=0.3, fill_color=POS_COLOR,
                        fill_opacity=0.4, stroke_width=0)
        r3.move_to(scale.n2p(0.75)).shift(UP * 0.3)
        regions.add(r1, r2, r3)

        # Mark examples on scale
        r_a_val = float(np.corrcoef(A_X, A_Y)[0, 1])
        dot_a = Dot(scale.n2p(r_a_val), color=POS_COLOR, radius=0.1)
        lbl_a = mn_text(f"A: {r_a_val:.2f}", size=20, color=POS_COLOR)
        lbl_a.next_to(dot_a, UP, buff=0.3)

        r_b_val = float(np.corrcoef(B_X, B_Y)[0, 1])
        dot_b = Dot(scale.n2p(r_b_val), color=NEG_COLOR, radius=0.1)
        lbl_b = mn_text(f"B: {r_b_val:.2f}", size=20, color=NEG_COLOR)
        lbl_b.next_to(dot_b, UP, buff=0.3)

        # Important note
        note_card = make_card(width=11, height=1.8)
        note_card.shift(DOWN * 1.8)
        note_text = VGroup(
            mn_text("⚠ Корреляци ≠ шалтгаан-үр дагавар", size=24,
                     color=HIGHLIGHT, weight=BOLD),
            mn_text(
                "Хамааралтай ≠ нэг нь нөгөөгийн шалтгаан",
                size=22,
            ),
        ).arrange(DOWN, buff=0.12)
        note_text.move_to(note_card)

        self.play(Write(header), run_time=0.7)
        self.play(Create(scale), FadeIn(regions), run_time=0.8)
        self.play(FadeIn(dot_a, scale=1.5), Write(lbl_a), run_time=0.7)
        self.play(FadeIn(dot_b, scale=1.5), Write(lbl_b), run_time=0.7)
        self.play(FadeIn(note_card), Write(note_text), run_time=1.2)
        self.wait(3.0)
        self.clear_scene()

    # ── SCENE 10: Summary ─────────────────────────────── ~10s

    def scene10_summary(self):
        title = mn_text("Дүгнэлт", size=44, color=WHITE, weight=BOLD)

        points = VGroup(
            mn_text("① Цэгэн диаграмм хамаарлыг нүдээр харуулна",
                     size=26, color=TEXT_COLOR),
            mn_text("② Ковариац нь чиглэлийг тодорхойлно",
                     size=26, color=TEXT_COLOR),
            mn_text("③ Корреляцийн коэффициент r нь хүч ба чиглэлийг хэмжинэ",
                     size=26, color=TEXT_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        group = VGroup(title, points).arrange(DOWN, buff=0.5)

        thanks = mn_text("Баярлалаа!", size=40, color=HIGHLIGHT, weight=BOLD)
        thanks.next_to(group, DOWN, buff=0.5)

        credit = mn_text("КУ5-Баттүвшин", size=22, color=NEUTRAL_COLOR)
        credit.to_edge(DOWN, buff=0.3)

        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.7)
        self.play(
            LaggedStart(*[FadeIn(p, shift=LEFT * 0.3) for p in points],
                        lag_ratio=0.3),
            run_time=2.0,
        )
        self.play(FadeIn(thanks, scale=1.3), run_time=0.8)
        self.play(FadeIn(credit), run_time=0.5)
        self.wait(2.5)


# ── Render commands ──
# Low quality preview:
#   manim -pql correlation_manim_video.py CorrelationVideo
# High quality (1080p):
#   manim -pqh correlation_manim_video.py CorrelationVideo
# Production (4K):
#   manim -pqk correlation_manim_video.py CorrelationVideo
