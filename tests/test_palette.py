import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from mangrove_palette_spectrum import hex_to_rgb, rgb_to_hsl, delta_h


def test_hex_to_rgb_red():
    assert hex_to_rgb("#ff0000") == (255, 0, 0)


def test_hex_to_rgb_black():
    assert hex_to_rgb("#000000") == (0, 0, 0)


def test_hex_to_rgb_white():
    assert hex_to_rgb("#ffffff") == (255, 255, 255)


def test_rgb_to_hsl_red():
    h, s, l = rgb_to_hsl(255, 0, 0)
    assert abs(h - 0.0) < 0.1
    assert abs(s - 100.0) < 0.1
    assert abs(l - 50.0) < 0.1


def test_rgb_to_hsl_achromatic():
    _, s, _ = rgb_to_hsl(128, 128, 128)
    assert s == 0.0


def test_delta_h_same():
    assert delta_h(100.0, 100.0) == 0.0


def test_delta_h_opposite():
    assert abs(delta_h(0.0, 180.0) - 180.0) < 0.01


def test_delta_h_symmetric():
    assert delta_h(10.0, 350.0) == delta_h(350.0, 10.0)
