# Attribution

pygloss is designed, directed and maintained by Matt Phelps ([@tbdtechpro](https://github.com/tbdtechpro)),
and built with AI-assisted development using Claude ([Anthropic](https://anthropic.com)).

---

## Original Go Library

All credit for the design, architecture, and reference implementation belongs to the
[Charm](https://charm.sh) team.

> **Lip Gloss** — Style definitions for nice terminal layouts
> <https://github.com/charmbracelet/lipgloss>

The upstream Go source served as the reference implementation during the port. It was removed from
this repository once the Python port reached feature parity, and it remains Charm's copyright.

**Charm team members and contributors:** see
<https://github.com/charmbracelet/lipgloss/graphs/contributors>

The Go Lip Gloss library is licensed under the MIT License. See [LICENSE](LICENSE) for the
full license text (which covers both the original Go code and the Python port).

---

## Tooling

| Tool | Role |
|------|------|
| **Claude** (Anthropic) | AI pair-programmer: Go-to-Python translation, test writing and documentation, under my direction and review |

---

## Dependencies

The Python port depends on the following open-source packages:

| Package | License | Purpose |
|---------|---------|---------|
| [wcwidth](https://github.com/jquast/wcwidth) | MIT | ANSI-aware string width measurement |
| [pytest](https://pytest.org) | MIT | Test runner |
| [pytest-cov](https://pytest-cov.readthedocs.io) | MIT | Coverage reporting |
| [black](https://black.readthedocs.io) | MIT | Code formatting |
| [isort](https://pycli.readthedocs.io/projects/isort) | MIT | Import sorting |
| [flake8](https://flake8.pycqa.org) | MIT | Linting |
| [mypy](https://mypy-lang.org) | MIT | Static type checking |

---

## Design Goals

- Translate a non-trivial, idiomatic Go library into *idiomatic* Python, not a line-by-line transliteration
- Hold the port to the bar of full feature parity and a real test suite
- Develop a repeatable, review-gated process for AI-assisted porting work

I set the porting strategy and API design, directed the implementation, and reviewed the output.
Claude did much of the line-level translation, test writing and documentation.

---

*Charm热爱开源 • Charm loves open source*
