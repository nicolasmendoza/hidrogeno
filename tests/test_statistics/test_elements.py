from ..test_fixtures import rain_gauge_20_30


def test_rain_gauge_level(rain_gauge_20_30):
    pluviometer = rain_gauge_20_30
    pluviometer.gather(90, 90)
    assert pluviometer.level == 90
    assert pluviometer.day == 90

def test_rain_gauge_peak_day():
    pass