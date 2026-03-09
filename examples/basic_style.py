"""
basic_style.py — demonstrates core Style properties.

Run with:  python examples/basic_style.py
"""

import pygloss

# ── Colors ────────────────────────────────────────────────────────────────────

highlight = pygloss.AdaptiveColor(light="#874BFD", dark="#7D56F4")
special = pygloss.AdaptiveColor(light="#43BF6D", dark="#73F59F")
subtle = pygloss.AdaptiveColor(light="#D9DCCF", dark="#383838")

# ── Styles ────────────────────────────────────────────────────────────────────

title_style = (
    pygloss.Style()
    .bold(True)
    .foreground(pygloss.Color("#FAFAFA"))
    .background(highlight)
    .padding(0, 2)
    .margin_bottom(1)
)

keyword_style = pygloss.Style().bold(True).foreground(special)

subtle_style = pygloss.Style().foreground(subtle)

bordered = (
    pygloss.Style()
    .border_style(pygloss.rounded_border())
    .border_foreground(highlight)
    .padding(1, 2)
)

status_bar = (
    pygloss.Style()
    .foreground(pygloss.Color("#FFFDF5"))
    .background(pygloss.Color("#FF5F87"))
    .padding(0, 1)
)

# ── Render ────────────────────────────────────────────────────────────────────


def main() -> None:
    print(title_style.render("Lip Gloss  ✨"))
    print()

    # Inline formatting
    print(
        "Terminal styling with "
        + keyword_style.render("bold")
        + ", "
        + pygloss.Style().italic(True).foreground(special).render("italic")
        + ", and "
        + pygloss.Style().underline(True).foreground(special).render("underlined")
        + " text."
    )
    print()

    # Bordered box
    content = pygloss.join_vertical(
        pygloss.Left,
        keyword_style.render("Foreground") + subtle_style.render(" — set the text colour"),
        keyword_style.render("Background") + subtle_style.render(" — set the background colour"),
        keyword_style.render("Border") + subtle_style.render(" — draw a box around content"),
        keyword_style.render("Padding") + subtle_style.render(" — inner spacing"),
        keyword_style.render("Margin") + subtle_style.render(" — outer spacing"),
        keyword_style.render("Align") + subtle_style.render(" — horizontal / vertical alignment"),
        keyword_style.render("Width") + subtle_style.render(" — minimum width"),
        keyword_style.render("Height") + subtle_style.render(" — minimum height"),
    )
    print(bordered.render(content))
    print()

    # Colors
    swatches = [
        "#F25D94",
        "#EDFF82",
        "#643AFF",
        "#14F9D5",
        "#FF5F87",
        "#A550DF",
        "#6124DF",
        "#73F59F",
    ]
    swatch_row = "".join(
        pygloss.Style().background(pygloss.Color(c)).render("  ") for c in swatches
    )
    print(subtle_style.render("Colour swatches:"), swatch_row)
    print()

    # Status bar nugget
    print(status_bar.render("STATUS") + "  " + subtle_style.render("Everything looks good."))
    print()


if __name__ == "__main__":
    main()
