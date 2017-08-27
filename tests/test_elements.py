from hydrogen.core.wheater.statistics.elements import RainGauge


def test_rain_gauge_level():
    pluviometer = RainGauge(10.2332, 9)
    assert pluviometer.level == 10.2332
    assert pluviometer.day == 9

def test_rain_gauge_peak_day():
    pass