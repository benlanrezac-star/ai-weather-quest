"""AI Weather Quest submission grid (1.5 deg global) and format check.

Format (AI-WQ-package 3.32, check_fc_submission.py): DataArray of shape
(5, 121, 240), dims (quintile, latitude, longitude), quintile labels
0.2 .. 1.0, latitude 90 -> -90, longitude 0 -> 358.5.

The official check sums with skipna, so an all-NaN point sums to 0 and is
rejected; it is also scored RPS = 5 (worst). This check is therefore
stricter than the official one: NaN is never accepted.
"""

import numpy as np
import xarray as xr

QUINTILES = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
LATITUDES = np.linspace(90.0, -90.0, 121)
LONGITUDES = np.arange(240) * 1.5
DIMS = ("quintile", "latitude", "longitude")
SHAPE = (len(QUINTILES), len(LATITUDES), len(LONGITUDES))

SUM_ATOL = 1e-6
RANGE_TOL = 1e-6


def coords() -> dict[str, np.ndarray]:
    """Coordinates of the submission grid."""
    return {"quintile": QUINTILES, "latitude": LATITUDES, "longitude": LONGITUDES}


def empty_forecast(fill: float = np.nan) -> xr.DataArray:
    """DataArray on the submission grid filled with ``fill``."""
    return xr.DataArray(np.full(SHAPE, fill), dims=DIMS, coords=coords(), name="tas")


def check_submission_array(fc: xr.DataArray | np.ndarray) -> None:
    """Raise ValueError if ``fc`` is not a valid quintile forecast.

    Checks shape (5, 121, 240), no NaN, values in [0, 1] and probabilities
    summing to 1 over the quintile axis (axis 0). For a DataArray, also
    checks dimension order and coordinate values.
    """
    if isinstance(fc, xr.DataArray):
        if fc.dims != DIMS:
            raise ValueError(f"dims are {fc.dims}, expected {DIMS}")
        for name, expected in coords().items():
            if name not in fc.coords:
                raise ValueError(f"missing coordinate '{name}'")
            if not np.allclose(fc[name].values, expected):
                raise ValueError(f"coordinate '{name}' does not match the submission grid")
        values = fc.values
    else:
        values = np.asarray(fc)

    if values.shape != SHAPE:
        raise ValueError(f"shape is {values.shape}, expected {SHAPE}")
    n_nan = int(np.isnan(values).sum())
    if n_nan:
        raise ValueError(f"{n_nan} NaN values (scored as zero probability by AI-WQ)")
    if values.min() < -RANGE_TOL or values.max() > 1 + RANGE_TOL:
        raise ValueError(f"values outside [0, 1]: min {values.min()}, max {values.max()}")
    max_dev = float(np.abs(values.sum(axis=0) - 1.0).max())
    if max_dev > SUM_ATOL:
        raise ValueError(f"quintile probabilities do not sum to 1 (max deviation {max_dev:.2e})")
