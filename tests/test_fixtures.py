from hydrogen.core.wheater.statistics.elements import RainGauge
from hydrogen.core.galaxy.planet import Planet
import pytest


@pytest.fixture()
def rain_gauge_20_30():
    """Rain gauge fixture"""
    return RainGauge(20, 30)


def test_fixture_rain_gauge_20_30(rain_gauge_20_30):
    assert rain_gauge_20_30.level ==  20
    assert rain_gauge_20_30.day == 30


@pytest.fixture()
def ferengi_planet():
    """Ferengi fixture"""
    return Planet.new_ferengi()

def test_fixture_ferengi_planet(ferengi_planet):
    assert ferengi_planet.velocity == 1
    assert ferengi_planet.sun_distancie == 500