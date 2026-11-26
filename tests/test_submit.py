"""Submission wrapper, without network: official calls are replaced by fakes."""

import pytest

from aiwq import grid, submit


def no_check(fc, start, period):
    pass


def no_registration():
    pass


def test_parse_start_date_accepts_thursday():
    assert submit.parse_start_date("20261029").isoformat() == "2026-10-29"


@pytest.mark.parametrize("value", ["20261028", "2026-10-29", "20261332"])
def test_parse_start_date_rejects_non_thursday_or_bad_format(value):
    with pytest.raises(ValueError):
        submit.parse_start_date(value)


def test_build_forecasts_two_valid_periods():
    forecasts = submit.build_forecasts()
    assert set(forecasts) == {"1", "2"}
    for fc in forecasts.values():
        grid.check_submission_array(fc)


def test_dry_run_never_uploads():
    def uploader(*args):
        raise AssertionError("upload called in dry run")

    names = submit.run("20261029", False, None, no_check, no_registration, uploader)
    assert names == [
        "tas_20261029_p1_SoloWQ_MetoceanML.nc",
        "tas_20261029_p2_SoloWQ_MetoceanML.nc",
    ]


def test_submit_uploads_both_periods_with_password():
    calls = []
    submit.run(
        "20261029", True, "pw", no_check, no_registration,
        lambda fc, start, period, pw: calls.append((start, period, pw)),
    )
    assert calls == [("20261029", "1", "pw"), ("20261029", "2", "pw")]


def test_submit_without_password_raises():
    with pytest.raises(RuntimeError):
        submit.run("20261029", True, None, no_check, no_registration, lambda *a: None)


def test_failed_check_stops_before_upload():
    def bad_check(fc, start, period):
        raise ValueError("bad")

    with pytest.raises(ValueError):
        submit.run("20261029", True, "pw", bad_check, no_registration,
                   lambda *a: pytest.fail("uploaded"))


@pytest.mark.parametrize(
    "today, expected",
    [
        ("2026-11-26", "2026-11-26"),  # Thursday itself
        ("2026-11-27", "2026-11-26"),  # Friday
        ("2026-11-29", "2026-11-26"),  # Sunday, last day of the window
        ("2026-12-02", "2026-11-26"),  # Wednesday before the next one
    ],
)
def test_latest_thursday(today, expected):
    from datetime import date

    assert submit.latest_thursday(date.fromisoformat(today)).isoformat() == expected


def test_all_submitted_needs_both_periods():
    assert submit.all_submitted("20261126", "pw", lambda s, p, pw: True)
    assert not submit.all_submitted("20261126", "pw", lambda s, p, pw: p == "1")


def test_append_log_writes_header_once(tmp_path):
    from datetime import datetime, timezone

    log = tmp_path / "submissions.csv"
    t = datetime(2026, 11, 26, 9, 13, tzinfo=timezone.utc)
    submit.append_log(log, "20261126", "submitted", t)
    submit.append_log(log, "20261126", "already_submitted", t)
    assert log.read_text(encoding="utf-8").splitlines() == [
        "fc_start_date,status,logged_utc",
        "20261126,submitted,2026-11-26T09:13:00Z",
        "20261126,already_submitted,2026-11-26T09:13:00Z",
    ]


def test_get_password_from_env_file(tmp_path, monkeypatch):
    monkeypatch.delenv("AIWQ_PASSWORD", raising=False)
    env = tmp_path / ".env"
    env.write_text("# comment\n\nAIWQ_PASSWORD=secret\nECDS_KEY=k\n", encoding="utf-8")
    assert submit.get_password(env) == "secret"


def test_environment_overrides_env_file(tmp_path, monkeypatch):
    monkeypatch.setenv("AIWQ_PASSWORD", "from-ci")
    env = tmp_path / ".env"
    env.write_text("AIWQ_PASSWORD=local\n", encoding="utf-8")
    assert submit.get_password(env) == "from-ci"


def test_missing_password_raises(tmp_path, monkeypatch):
    monkeypatch.delenv("AIWQ_PASSWORD", raising=False)
    with pytest.raises(RuntimeError):
        submit.get_password(tmp_path / "missing.env")
