"""Ranked probability score (RPS) and skill score (RPSS) for quintile forecasts.

Follows AI-WQ-package 3.32 (forecast_evaluation.py):
- RPS = sum over the 5 quintiles of the squared difference of cumulative
  probabilities (not divided by K - 1; the last term is 0 for valid data);
- NaN forecast probabilities count as 0 (official cumsum skips NaN), so a
  NaN point gets the worst score instead of being dropped;
- points where the observation is all-NaN are excluded;
- optional land mask: points with land fraction >= 0.5 are kept;
- area weights cos(latitude);
- RPSS = 1 - sum(w * RPS_fc) / sum(w * RPS_clim) over every point and every
  leading dimension (e.g. weeks), i.e. the period score is a ratio of sums,
  not a mean of weekly RPSS.

Inputs are DataArrays with dims 'quintile', 'latitude', 'longitude' and any
extra leading dims. Quintile coordinates are ignored (the official obs use
0..4, forecasts 0.2..1.0); quintiles are matched by position.
"""

import numpy as np
import xarray as xr

QDIM = "quintile"
LAND_THRESHOLD = 0.5


def _drop_quintile_coord(da: xr.DataArray) -> xr.DataArray:
    if QDIM not in da.dims:
        raise ValueError(f"missing dimension '{QDIM}' in {da.dims}")
    return da.drop_vars(QDIM, errors="ignore")


def rps(fc: xr.DataArray, obs: xr.DataArray) -> xr.DataArray:
    """Per-point RPS. ``obs`` is one-hot over quintiles (all-NaN = no data)."""
    fc, obs = xr.align(_drop_quintile_coord(fc), _drop_quintile_coord(obs), join="exact")
    fc_cum = fc.fillna(0.0).cumsum(QDIM)
    obs_cum = obs.cumsum(QDIM, skipna=False)
    score = ((fc_cum - obs_cum) ** 2).sum(QDIM, skipna=False)
    return score.where(obs.notnull().any(QDIM))


def _weights(score: xr.DataArray, land_mask: xr.DataArray | None) -> xr.DataArray:
    w = np.cos(np.deg2rad(score["latitude"]))
    if land_mask is not None:
        land_mask, _ = xr.align(land_mask, score, join="exact")
        w = w * (land_mask >= LAND_THRESHOLD)
    return w.broadcast_like(score).where(score.notnull(), 0.0)


def weighted_rps(score: xr.DataArray, land_mask: xr.DataArray | None = None) -> float:
    """Area-weighted mean of a per-point RPS over all points and leading dims."""
    w = _weights(score, land_mask)
    total = float(w.sum())
    if total == 0.0:
        raise ValueError("no valid point to score")
    return float((score.fillna(0.0) * w).sum()) / total


def rpss(
    fc: xr.DataArray, obs: xr.DataArray, land_mask: xr.DataArray | None = None
) -> float:
    """RPSS of ``fc`` against the climatological forecast (0.2 per quintile).

    ``land_mask`` is a land fraction (or boolean) on (latitude, longitude);
    pass the AI-WQ land-sea mask for tas to reproduce the official score.
    """
    clim = xr.full_like(fc, 1.0 / fc.sizes[QDIM], dtype=float)
    rps_fc = weighted_rps(rps(fc, obs), land_mask)
    rps_clim = weighted_rps(rps(clim, obs), land_mask)
    return 1.0 - rps_fc / rps_clim
