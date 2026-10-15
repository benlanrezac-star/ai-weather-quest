"""Hand-computed RPS / RPSS cases on tiny grids.

Climatology (0.2 each) has cumulative probabilities [0.2, 0.4, 0.6, 0.8, 1]:
- obs in quintile 1 (cum [1, 1, 1, 1, 1]): 0.64 + 0.36 + 0.16 + 0.04 = 1.2
- obs in quintile 3 (cum [0, 0, 1, 1, 1]): 0.04 + 0.16 + 0.16 + 0.04 = 0.4
- obs in quintile 5 (cum [0, 0, 0, 0, 1]): 0.04 + 0.16 + 0.36 + 0.64 = 1.2
Forecast [0, 1, 0, 0, 0] (cum [0, 1, 1, 1, 1]) with obs in quintile 1: 1.0
"""

import numpy as np
import pytest
import xarray as xr

from aiwq import rps

LAT = [60.0, 0.0]  # cos = 0.5, 1.0
LON = [0.0]
CLIM = [0.2] * 5
SHIFTED = [0.0, 1.0, 0.0, 0.0, 0.0]


def onehot(k):
    v = [0.0] * 5
    v[k] = 1.0
    return v


def field(per_lat, lat=LAT, quintile=(0.2, 0.4, 0.6, 0.8, 1.0)):
    """(quintile, latitude, longitude) DataArray from one 5-vector per latitude."""
    data = np.array(per_lat, dtype=float).T[:, :, None]
    return xr.DataArray(
        data,
        dims=("quintile", "latitude", "longitude"),
        coords={"quintile": list(quintile), "latitude": lat, "longitude": LON},
    )


def obs_field(per_lat, lat=LAT):
    # official obs use quintile labels 0..4, forecasts 0.2..1.0
    return field(per_lat, lat=lat, quintile=range(5))


@pytest.mark.parametrize("k, expected", [(0, 1.2), (2, 0.4), (4, 1.2)])
def test_climatology_rps_by_hand(k, expected):
    score = rps.rps(field([CLIM, CLIM]), obs_field([onehot(k), onehot(k)]))
    np.testing.assert_allclose(score.values, expected)


def test_shifted_forecast_rps_by_hand():
    score = rps.rps(field([SHIFTED, SHIFTED]), obs_field([onehot(0), onehot(1)]))
    np.testing.assert_allclose(score.values.ravel(), [1.0, 0.0])


def test_perfect_forecast_rpss_is_one():
    obs = obs_field([onehot(0), onehot(3)])
    fc = field([onehot(0), onehot(3)])
    assert rps.rpss(fc, obs) == pytest.approx(1.0)


def test_climatology_rpss_is_zero():
    obs = obs_field([onehot(1), onehot(4)])
    assert rps.rpss(field([CLIM, CLIM]), obs) == pytest.approx(0.0)


def test_cos_latitude_weighting():
    # lat 60 (w 0.5): RPS 1 ; lat 0 (w 1): RPS 0 ; clim RPS 1.2 at both.
    # weighted fc = 0.5 / 1.5 = 1/3 -> RPSS = 1 - (1/3) / 1.2 = 13/18
    obs = obs_field([onehot(0), onehot(0)])
    fc = field([SHIFTED, onehot(0)])
    assert rps.rpss(fc, obs) == pytest.approx(13 / 18)


@pytest.mark.parametrize("land, expected", [([0.3, 1.0], 1.0), ([1.0, 0.3], 1 - 1 / 1.2)])
def test_land_mask_keeps_points_with_half_land_or_more(land, expected):
    obs = obs_field([onehot(0), onehot(0)])
    fc = field([SHIFTED, onehot(0)])
    mask = xr.DataArray(
        np.array(land)[:, None], dims=("latitude", "longitude"),
        coords={"latitude": LAT, "longitude": LON},
    )
    assert rps.rpss(fc, obs, land_mask=mask) == pytest.approx(expected)


def test_boolean_land_mask():
    obs = obs_field([onehot(0), onehot(0)])
    fc = field([SHIFTED, onehot(0)])
    mask = xr.DataArray(
        np.array([[True], [False]]), dims=("latitude", "longitude"),
        coords={"latitude": LAT, "longitude": LON},
    )
    assert rps.rpss(fc, obs, land_mask=mask) == pytest.approx(1 - 1 / 1.2)


def test_nan_forecast_scored_as_zero_probability():
    # matches AI-WQ-package 3.32: cum fc [0]*5 vs obs cum [1]*5 -> RPS 5
    nan5 = [np.nan] * 5
    score = rps.rps(field([nan5, CLIM]), obs_field([onehot(0), onehot(0)]))
    np.testing.assert_allclose(score.values.ravel(), [5.0, 1.2])


def test_missing_observation_excluded():
    nan5 = [np.nan] * 5
    obs = obs_field([nan5, onehot(0)])
    fc = field([SHIFTED, onehot(0)])
    assert np.isnan(rps.rps(fc, obs).values[0, 0])
    assert rps.rpss(fc, obs) == pytest.approx(1.0)


def test_period_rpss_is_ratio_of_sums_not_mean_of_weeks():
    # week 1: obs q3, perfect fc (RPS 0, clim 0.4)
    # week 2: obs q1, shifted fc (RPS 1, clim 1.2)
    # ratio of sums: 1 - 1 / 1.6 = 0.375 (mean of weekly RPSS would be 0.583)
    lat = [0.0]
    w1_obs, w2_obs = obs_field([onehot(2)], lat=lat), obs_field([onehot(0)], lat=lat)
    w1_fc, w2_fc = field([onehot(2)], lat=lat), field([SHIFTED], lat=lat)
    obs = xr.concat([w1_obs, w2_obs], dim="week")
    fc = xr.concat([w1_fc, w2_fc], dim="week")
    assert rps.rpss(fc, obs) == pytest.approx(0.375)


def test_grid_mismatch_raises():
    obs = obs_field([onehot(0), onehot(0)], lat=[1.5, 0.0])
    with pytest.raises(ValueError):
        rps.rps(field([CLIM, CLIM]), obs)
