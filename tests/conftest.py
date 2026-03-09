"""Shared pytest fixtures for pygloss tests."""

from __future__ import annotations

import io

import pytest

import pygloss
from pygloss.renderer import ColorProfile, Renderer


@pytest.fixture()
def truecolor_renderer() -> Renderer:
    """A renderer with TrueColor forced — gives deterministic ANSI output."""
    r = Renderer(io.StringIO())
    r.set_color_profile(ColorProfile.TRUE_COLOR)
    return r


@pytest.fixture()
def ansi256_renderer() -> Renderer:
    r = Renderer(io.StringIO())
    r.set_color_profile(ColorProfile.ANSI256)
    return r


@pytest.fixture()
def ansi_renderer() -> Renderer:
    r = Renderer(io.StringIO())
    r.set_color_profile(ColorProfile.ANSI)
    return r


@pytest.fixture()
def ascii_renderer() -> Renderer:
    r = Renderer(io.StringIO())
    r.set_color_profile(ColorProfile.ASCII)
    return r


@pytest.fixture()
def style(truecolor_renderer: Renderer) -> pygloss.Style:
    """An empty Style bound to the TrueColor renderer."""
    return truecolor_renderer.new_style()
