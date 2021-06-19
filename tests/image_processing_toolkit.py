from src.toolkit.image_processing import hex_to_bgr


def test_hex_to_bgr():
    hex_value = '#000000'
    black = [0, 0, 0]
    assert hex_to_bgr(hex_value) == black

    hex_value = '#ffffff'
    white = [255, 255, 255]
    assert hex_to_bgr(hex_value) == white

    hex_value = '#ff0000'
    red = [0, 0, 255]
    assert hex_to_bgr(hex_value) == red
