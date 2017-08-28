from hydrogen.core.wheater.statistics.elements import RainGauge
from hydrogen.core.galaxy.planet import Planet, ClockWise
from hydrogen.core.galaxy.simulator import PlanetPosition
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
    """ClockWise.COUNTERCLOCK fixture"""
    return ClockWise.COUNTERCLOCK.value


def test_fixture_clockwise_counterclock(clockwise_counterclock):
    assert clockwise_counterclock == 1


@pytest.fixture()
def clockwise_anticlock():
    """ClockWise.ANTICLOCK fixture.."""
    return ClockWise.ANTICLOCK.value


def test_fixture_clockwise_anticlock(clockwise_anticlock):
    assert clockwise_anticlock == -1


@pytest.fixture()
def ferengi_planet():
    """Fixture Ferengi planet"""
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


@pytest.fixture
def betasoide_planet():
    """Betasoide planet fixture"""
    return Planet.new_betasoide()

def test_fixture_betasoide_planet(betasoide_planet):
    assert betasoide_planet._velocity == 3 * clockwise_anticlock
    assert betasoide_planet._sun_distance == 2000

@pytest.fixture
def planet_position_are_aligned():
    """Fixture planets position. are aligned"""
    return PlanetPosition.are_aligned.value


def test_planet_position_are_aligned(planet_position_are_aligned):
    assert planet_position_are_aligned == 'planets_are_aligned'
   

@pytest.fixture()
def planet_position_are_aligned_with_sun():
    """Fixture Planet position, are aligned with sun"""
    return PlanetPosition.are_aligned_with_sun.value

def test_planet_position_are_aligned_with_sun(planet_position_are_aligned_with_sun):
    assert planet_position_are_aligned_with_sun == 'planet_and_sun_are_aligned'