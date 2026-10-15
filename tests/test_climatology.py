import numpy as np
import xarray as xr

from aiwq import grid, rps
from aiwq.climatology import climatology_forecast


def test_climatology_is_valid_submission():
    fc = climatology_forecast()
    grid.check_submission_array(fc)
    np.testing.assert_allclose(fc.values, 0.2)


def test_climatology_rpss_is_zero_on_full_grid():
    rng = np.random.default_rng(0)
    category = rng.integers(0, 5, size=(121, 240))
    obs = xr.DataArray(
        (np.arange(5)[:, None, None] == category).astype(float),
        dims=grid.DIMS,
        coords={**grid.coords(), "quintile": np.arange(5)},
    )
    assert rps.rpss(climatology_forecast(), obs) == 0.0
