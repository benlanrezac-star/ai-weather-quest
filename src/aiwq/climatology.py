"""Climatological quintile forecast: 0.2 in every quintile.

Used as the RPSS reference, as the validation baseline and as the fallback
submission when IFS data are missing (same team and model name).
"""

import xarray as xr

from aiwq import grid


def climatology_forecast() -> xr.DataArray:
    """Climatological forecast on the submission grid (RPSS = 0 by definition)."""
    return grid.empty_forecast(fill=1.0 / len(grid.QUINTILES))
