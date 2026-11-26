"""Weekly submission of tas quintile forecasts to the AI Weather Quest (ECBox).

Dry run (default) only reads: local format checks + the official local
checks of AI-WQ-package, and the public list of registered teams/models.
``--submit`` uploads to ECBox. Note that the official
AI_WQ_create_empty_dataarray also writes to ECBox (identifier table), so it
is only reached in submit mode.

Usage:
    uv run --group submit python -m aiwq.submit --date 20261029          # dry run
    uv run --group submit python -m aiwq.submit --date 20261029 --submit
"""

import argparse
import os
import sys
from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import xarray as xr

from aiwq import grid
from aiwq.climatology import climatology_forecast

TEAM = "SoloWQ"
MODEL = "MetoceanML"
VARIABLE = "tas"
PERIODS = ("1", "2")
PASSWORD_VAR = "AIWQ_PASSWORD"


def parse_start_date(value: str) -> date:
    """Parse YYYYMMDD and require a Thursday (AI-WQ initialisation day)."""
    d = datetime.strptime(value, "%Y%m%d").date()
    if d.weekday() != 3:
        raise ValueError(f"{value} is not a Thursday")
    return d


def load_env(path: Path) -> dict[str, str]:
    """Minimal KEY=VALUE reader for a local .env (comments and blanks skipped)."""
    if not path.exists():
        return {}
    pairs = (
        line.split("=", 1)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#") and "=" in line
    )
    return {k.strip(): v.strip() for k, v in pairs}


def get_password(env_file: Path) -> str:
    """Password from the environment (CI secret) or, locally, from .env."""
    password = os.environ.get(PASSWORD_VAR) or load_env(env_file).get(PASSWORD_VAR)
    if not password:
        raise RuntimeError(f"{PASSWORD_VAR} not set (environment or {env_file})")
    return password


def build_forecasts() -> dict[str, xr.DataArray]:
    """Forecast per period. v0: climatology for both periods (also the fallback)."""
    forecasts = {p: climatology_forecast() for p in PERIODS}
    for fc in forecasts.values():
        grid.check_submission_array(fc)
    return forecasts


def official_local_checks(fc: xr.DataArray, start: str, period: str) -> None:
    """Official AI-WQ checks that do not write anywhere."""
    from AI_WQ_package import check_fc_submission as cfs

    da = cfs.check_and_flip_latitudes(fc)
    da = cfs.check_and_convert_longitudes(da)
    da = cfs.check_quintile_range(da)
    cfs.check_data_characteristics(da, VARIABLE, start, period)


def check_registration() -> None:
    """Read-only check of team and model names against the public registry."""
    from AI_WQ_package import check_fc_submission as cfs

    cfs.check_registered_teamname(TEAM)
    cfs.check_registered_modelname(MODEL)


def upload(fc: xr.DataArray, start: str, period: str, password: str) -> None:
    """Upload one period to ECBox, then confirm the file is there."""
    from AI_WQ_package import forecast_submission as fs

    fs.AI_WQ_forecast_submission(fc, VARIABLE, start, period, TEAM, MODEL, password)
    fs.AI_WQ_check_submission(VARIABLE, start, period, TEAM, MODEL, password)


def run(
    start: str,
    submit: bool,
    password: str | None,
    checks: Callable[[xr.DataArray, str, str], None] = official_local_checks,
    registration: Callable[[], None] = check_registration,
    uploader: Callable[[xr.DataArray, str, str, str], None] = upload,
) -> list[str]:
    """Check (and, if ``submit``, upload) both periods. Returns the file names."""
    parse_start_date(start)
    forecasts = build_forecasts()
    for period, fc in forecasts.items():
        checks(fc, start, period)
    registration()
    names = [f"{VARIABLE}_{start}_p{p}_{TEAM}_{MODEL}.nc" for p in forecasts]
    if submit:
        if not password:
            raise RuntimeError("password required to submit")
        for period, fc in forecasts.items():
            uploader(fc, start, period, password)
    return names


def latest_thursday(today: date) -> date:
    """Most recent Thursday on or before ``today`` (current submission week)."""
    return today - timedelta(days=(today.weekday() - 3) % 7)


def is_submitted(start: str, period: str, password: str) -> bool:
    """True if the official check finds this period's file on ECBox (read-only)."""
    from AI_WQ_package import forecast_submission as fs

    try:
        fs.AI_WQ_check_submission(VARIABLE, start, period, TEAM, MODEL, password)
    except FileNotFoundError:
        return False
    return True


def all_submitted(
    start: str, password: str, checker: Callable[[str, str, str], bool] = is_submitted
) -> bool:
    return all(checker(start, p, password) for p in PERIODS)


def append_log(log_file: Path, start: str, status: str, now: datetime) -> None:
    """Append one CSV line (start date, status, UTC time) to the submission log."""
    new = not log_file.exists()
    with log_file.open("a", encoding="utf-8") as f:
        if new:
            f.write("fc_start_date,status,logged_utc\n")
        f.write(f"{start},{status},{now:%Y-%m-%dT%H:%M:%SZ}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--date", help="initialisation Thursday, YYYYMMDD (default: latest Thursday, UTC)")
    parser.add_argument("--submit", action="store_true", help="upload to ECBox (default: dry run)")
    parser.add_argument("--skip-if-submitted", action="store_true",
                        help="with --submit: do nothing if both periods are already on ECBox")
    parser.add_argument("--log", type=Path, help="append the outcome to this CSV file")
    parser.add_argument("--env-file", type=Path, default=Path(".env"))
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc)
    start = args.date or f"{latest_thursday(now.date()):%Y%m%d}"
    password = get_password(args.env_file) if args.submit else None

    if args.submit and args.skip_if_submitted and all_submitted(start, password):
        status = "already_submitted"
        print(f"ALREADY SUBMITTED: {start}, nothing uploaded")
    else:
        names = run(start, args.submit, password)
        status = "submitted" if args.submit else "dry_run"
        mode = "SUBMITTED" if args.submit else "DRY RUN OK (nothing uploaded)"
        print(f"{mode}: {', '.join(names)}")
    if args.log:
        append_log(args.log, start, status, now)
    return 0


if __name__ == "__main__":
    sys.exit(main())
