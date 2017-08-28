from hydrogen.core.wheater.statistics.elements import RainGauge
from hydrogen.core.galaxy.planet import Planet, ClockWise
import pytest


@pytest.fixture()
def rain_gauge_20_30():
    """Rain gauge fixture"""
    return RainGauge(20, 30)


def test_fixture_rain_gauge_20_30(rain_gauge_20_30):
    assert rain_gauge_20_30.level ==  20
    assert rain_gauge_20_30.day == 30

@pytest.fixture()
def clockwise_counterclock():
    return ClockWise.COUNTERCLOCK.value


def test_fixture_clockwise_counterclock(clockwise_counterclock):
    assert clockwise_counterclock == 1


@pytest.fixture()
def clockwise_anticlock():
    return ClockWise.ANTICLOCK.value


def test_fixture_clockwise_anticlock(clockwise_anticlock):
    assert clockwise_anticlock == -1


@pytest.fixture()
def ferengi_planet():
    """Ferengi fixture"""
    return Planet.new_ferengi()

def test_fixture_ferengi_planet(ferengi_planet, clockwise_counterclock):
    assert ferengi_planet._velocity == 1 * clockwise_counterclock
    assert ferengi_planet._sun_distance == 500


@pytest.fixture()
def vulcano_planet():
    """Fixture planeta vulcano"""
    return Planet.new_vulcano()

def test_fixture_vulcano_planet(vulcano_planet, clockwise_anticlock ):
    assert vulcano_planet._velocity == 5 * clockwise_anticlock
    assert vulcano_planet._sun_distance == 1000
