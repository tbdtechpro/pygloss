"""
layout.py — multi-column layout showcase using join, place, and borders.

A simplified port of examples/layout/main.go (omitting dependencies on
go-colorful / gamut that have no direct Python equivalent).

Run with:  python examples/layout.py
"""

import pygloss

# ── Constants ─────────────────────────────────────────────────────────────────

WIDTH = 96
COLUMN_WIDTH = 30

# ── Color tokens ──────────────────────────────────────────────────────────────

highlight = pygloss.AdaptiveColor(light="#874BFD", dark="#7D56F4")
special = pygloss.AdaptiveColor(light="#43BF6D", dark="#73F59F")
subtle = pygloss.AdaptiveColor(light="#D9DCCF", dark="#383838")

# ── Base styles ───────────────────────────────────────────────────────────────

base = pygloss.Style().foreground(pygloss.Color("#EEEEEE"))

divider = pygloss.Style().set_string("•").padding(0, 1).foreground(subtle).render()

# ── Tab styles ────────────────────────────────────────────────────────────────

from pygloss.borders import Border  # noqa: E402

active_tab_border = Border(
    top="─",
    bottom=" ",
    left="│",
    right="│",
    top_left="╭",
    top_right="╮",
    bottom_left="┘",
    bottom_right="└",
)

tab_border = Border(
    top="─",
    bottom="─",
    left="│",
    right="│",
    top_left="╭",
    top_right="╮",
    bottom_left="┴",
    bottom_right="┴",
)

tab_style = pygloss.Style().border_style(tab_border).border_foreground(highlight).padding(0, 1)

active_tab_style = tab_style.border_style(active_tab_border)

tab_gap_style = tab_style.border_top(False).border_left(False).border_right(False)

# ── Title styles ──────────────────────────────────────────────────────────────

title_style = (
    pygloss.Style()
    .margin_left(1)
    .margin_right(5)
    .padding(0, 1)
    .italic(True)
    .foreground(pygloss.Color("#FFF7DB"))
)

desc_style = base.margin_top(1)

info_style = base.border_style(pygloss.normal_border()).border_top(True).border_foreground(subtle)

# ── Dialog styles ─────────────────────────────────────────────────────────────

dialog_box_style = (
    pygloss.Style()
    .border(pygloss.rounded_border())
    .border_foreground(pygloss.Color("#874BFD"))
    .padding(1, 0)
)

button_style = (
    pygloss.Style()
    .foreground(pygloss.Color("#FFF7DB"))
    .background(pygloss.Color("#888B7E"))
    .padding(0, 3)
    .margin_top(1)
)

active_button_style = (
    button_style.foreground(pygloss.Color("#FFF7DB"))
    .background(pygloss.Color("#F25D94"))
    .margin_right(2)
    .underline(True)
)

# ── List styles ───────────────────────────────────────────────────────────────

list_style = (
    pygloss.Style()
    .border(pygloss.normal_border(), False, True, False, False)
    .border_foreground(subtle)
    .margin_right(2)
    .height(8)
    .width(COLUMN_WIDTH + 1)
)

list_header = (
    base.border_style(pygloss.normal_border())
    .border_bottom(True)
    .border_foreground(subtle)
    .margin_right(2)
    .render
)

list_item = base.padding_left(2).render

check_mark = pygloss.Style().set_string("✓").foreground(special).padding_right(1).render()


def list_done(s: str) -> str:
    return check_mark + (
        pygloss.Style()
        .strikethrough(True)
        .foreground(pygloss.AdaptiveColor(light="#969B86", dark="#696969"))
        .render(s)
    )


# ── Status bar styles ─────────────────────────────────────────────────────────

status_nugget = pygloss.Style().foreground(pygloss.Color("#FFFDF5")).padding(0, 1)

status_bar_style = (
    pygloss.Style()
    .foreground(pygloss.AdaptiveColor(light="#343433", dark="#C1C6B2"))
    .background(pygloss.AdaptiveColor(light="#D9DCCF", dark="#353533"))
)

status_style = (
    pygloss.Style()
    .inherit(status_bar_style)
    .foreground(pygloss.Color("#FFFDF5"))
    .background(pygloss.Color("#FF5F87"))
    .padding(0, 1)
    .margin_right(1)
)

encoding_style = status_nugget.background(pygloss.Color("#A550DF")).align(pygloss.Right)
status_text = pygloss.Style().inherit(status_bar_style)
fish_cake_style = status_nugget.background(pygloss.Color("#6124DF"))

doc_style = pygloss.Style().padding(1, 2, 1, 2)

# ── History ───────────────────────────────────────────────────────────────────

history_style = (
    pygloss.Style()
    .align(pygloss.Left)
    .foreground(pygloss.Color("#FAFAFA"))
    .background(highlight)
    .margin(1, 3, 0, 0)
    .padding(1, 2)
    .height(7)
    .width(COLUMN_WIDTH)
)

HISTORY_A = (
    "The Romans learned from the Greeks that quinces slowly cooked with honey "
    'would "set" when cool. The Apicius gives a recipe for preserving whole quinces '
    "in a bath of honey diluted with defrutum: Roman marmalade."
)
HISTORY_B = (
    "Medieval quince preserves, which went by the French name cotignac, began to "
    "lose their medieval seasoning of spices in the 16th century. La Varenne provided "
    "recipes for both thick and clear cotignac."
)
HISTORY_C = (
    'In 1524, Henry VIII received a "box of marmalade" from Mr. Hull of Exeter. '
    "This was probably marmelada, a solid quince paste from Portugal, still made "
    "and sold in southern Europe today."
)


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parts: list[str] = []

    # Tabs
    row = pygloss.join_horizontal(
        pygloss.Top,
        active_tab_style.render("Lip Gloss"),
        tab_style.render("Blush"),
        tab_style.render("Eye Shadow"),
        tab_style.render("Mascara"),
        tab_style.render("Foundation"),
    )
    gap_width = max(0, WIDTH - pygloss.width(row) - 2)
    gap = tab_gap_style.render(" " * gap_width)
    row = pygloss.join_horizontal(pygloss.Bottom, row, gap)
    parts.append(row + "\n")

    # Title + description
    title = title_style.render("Lip Gloss")
    desc = pygloss.join_vertical(
        pygloss.Left,
        desc_style.render("Style Definitions for Nice Terminal Layouts"),
        info_style.render("From Charm" + divider + "https://github.com/charmbracelet/lipgloss"),
    )
    parts.append(pygloss.join_horizontal(pygloss.Top, title, desc) + "\n")

    # Dialog
    ok_button = active_button_style.render("Yes")
    cancel_button = button_style.render("Maybe")
    question = (
        pygloss.Style()
        .width(50)
        .align(pygloss.Center)
        .render("Are you sure you want to eat marmalade?")
    )
    buttons = pygloss.join_horizontal(pygloss.Top, ok_button, cancel_button)
    ui = pygloss.join_vertical(pygloss.Center, question, buttons)
    dialog = pygloss.place(
        WIDTH,
        9,
        pygloss.Center,
        pygloss.Center,
        dialog_box_style.render(ui),
        pygloss.whitespace_chars("猫咪"),
        pygloss.whitespace_foreground(subtle),
    )
    parts.append(dialog + "\n")

    # Lists
    lists = pygloss.join_horizontal(
        pygloss.Top,
        list_style.render(
            pygloss.join_vertical(
                pygloss.Left,
                list_header("Citrus Fruits to Try"),
                list_done("Grapefruit"),
                list_done("Yuzu"),
                list_item("Citron"),
                list_item("Kumquat"),
                list_item("Pomelo"),
            )
        ),
        list_style.width(COLUMN_WIDTH).render(
            pygloss.join_vertical(
                pygloss.Left,
                list_header("Actual Lip Gloss Vendors"),
                list_item("Glossier"),
                list_item("Claire's Boutique"),
                list_done("Nyx"),
                list_item("Mac"),
                list_done("Milk"),
            )
        ),
    )
    parts.append(lists)

    # History
    history = pygloss.join_horizontal(
        pygloss.Top,
        history_style.align(pygloss.Right).render(HISTORY_A),
        history_style.align(pygloss.Center).render(HISTORY_B),
        history_style.margin_right(0).render(HISTORY_C),
    )
    parts.append("\n\n" + history + "\n\n")

    # Status bar
    status_key = status_style.render("STATUS")
    encoding = encoding_style.render("UTF-8")
    fish_cake = fish_cake_style.render("🍥 Fish Cake")
    remaining = (
        WIDTH - pygloss.width(status_key) - pygloss.width(encoding) - pygloss.width(fish_cake)
    )
    status_val = status_text.width(remaining).render("Ravishing")
    bar = pygloss.join_horizontal(pygloss.Top, status_key, status_val, encoding, fish_cake)
    parts.append(status_bar_style.width(WIDTH).render(bar))

    print(doc_style.render("\n".join(parts)))


if __name__ == "__main__":
    main()
