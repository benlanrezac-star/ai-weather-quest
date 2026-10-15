import numpy as np
import pytest

from aiwq import grid


def valid_forecast():
    return grid.empty_forecast(fill=0.2)


def test_grid_coordinates():
    assert grid.LATITUDES.shape == (121,)
    assert grid.LATITUDES[0] == 90.0 and grid.LATITUDES[-1] == -90.0
    np.testing.assert_allclose(np.diff(grid.LATITUDES), -1.5)
    assert grid.LONGITUDES.shape == (240,)
    assert grid.LONGITUDES[0] == 0.0 and grid.LONGITUDES[-1] == 358.5
    np.testing.assert_allclose(np.diff(grid.LONGITUDES), 1.5)
    np.testing.assert_allclose(grid.QUINTILES, [0.2, 0.4, 0.6, 0.8, 1.0])


def test_empty_forecast_layout():
    fc = grid.empty_forecast()
    assert fc.dims == ("quintile", "latitude", "longitude")
    assert fc.shape == (5, 121, 240)
    assert bool(fc.isnull().all())


def test_valid_dataarray_and_ndarray_pass():
    fc = valid_forecast()
    grid.check_submission_array(fc)
    grid.check_submission_array(fc.values)


def test_non_uniform_valid_forecast_passes():
    fc = valid_forecast()
    fc[:, 10, 20] = [0.0, 0.1, 0.2, 0.3, 0.4]
    grid.check_submission_array(fc)


def test_wrong_shape_rejected():
    with pytest.raises(ValueError, match="shape"):
        grid.check_submission_array(np.full((5, 121, 239), 0.2))


def test_nan_rejected():
    fc = valid_forecast()
    fc[:, 0, 0] = np.nan
    with pytest.raises(ValueError, match="NaN"):
        grid.check_submission_array(fc)


def test_value_out_of_range_rejected():
    fc = valid_forecast()
    fc[:, 5, 5] = [-0.1, 0.3, 0.3, 0.3, 0.2]
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        grid.check_submission_array(fc)


def test_sum_not_one_rejected():
    fc = valid_forecast()
    fc[0, 5, 5] = 0.25
    with pytest.raises(ValueError, match="sum to 1"):
        grid.check_submission_array(fc)


def test_ascending_latitudes_rejected():
    fc = valid_forecast().sortby("latitude")
    with pytest.raises(ValueError, match="latitude"):
        grid.check_submission_array(fc)


def test_wrong_dim_order_rejected():
    fc = valid_forecast().transpose("latitude", "longitude", "quintile")
    with pytest.raises(ValueError, match="dims"):
        grid.check_submission_array(fc)
