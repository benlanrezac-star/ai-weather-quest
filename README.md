# ai-weather-quest

Submission chain of team `SoloWQ`, model `MetoceanML`, for the
[ECMWF AI Weather Quest](https://aiweatherquest.ecmwf.int/).

Approach: statistical post-processing (calibration) of ECMWF S2S ensemble
forecasts into quintile probabilities of weekly-mean 2 m temperature (`tas`).

## Development

```powershell
uv sync
uv run pytest
```

## Layout

- `src/aiwq/grid.py` — 1.5° submission grid and format check.
- `src/aiwq/rps.py` — RPS / RPSS (cos-latitude weights, optional land mask).
- `src/aiwq/climatology.py` — climatological forecast (0.2 everywhere), baseline and fallback.
