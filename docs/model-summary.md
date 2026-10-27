# AI Weather Quest — Model summary questionnaire (draft)

Team `SoleWQ` · Model `MetoceanML` · Variable: `tas` · Period: DJF 2026/27

> **Draft, 27/10/2026.** Answers describe the method as designed (decisions D-001 to D-010 in `decisions.md`).
> Items marked `[TO CONFIRM]` depend on work not done yet. They must be filled in from actual results before submission.
> Submission window: the final four weeks of the DJF period. Summaries are published on the team's public page.

---

### 1. Overarching design (multiple choices allowed)
- **a. Post-processing of numerical weather prediction (NWP) data**: yes.
- **c. Statistical model focused on generating quintile probabilities**: yes.
- **f. Ensemble-based model**: yes. The ECMWF ensemble distribution (mean and spread) is the main input to the calibration.

### 2. Initialisation
The model has no initial conditions of its own. It post-processes the ECMWF IFS extended-range ensemble initialised on the competition Thursday at 00 UTC from the ECMWF operational analysis. Only data valid at or before Thursday 00 UTC are used.

### 3. Data used in real time
- ECMWF S2S real-time ensemble (control + 100 perturbed members), daily-mean 2 m temperature, 1.5° global grid, lead days 19–32. It is retrieved from the ECMWF Data Store (ECDS) after the 48-hour S2S delay.
- The ECMWF S2S reforecasts produced for the same model version date: 20 past years, control + 10 members, same lead times.
- Fallback: if the IFS data cannot be retrieved before the submission deadline, a climatological forecast (0.2 per quintile) is submitted under the same model name.

### 4. Training datasets
- **NWP outputs**: ECMWF S2S reforecasts (2 m temperature) for the model version date of each forecast week.
- **Reanalysis**: ERA5 weekly-mean 2 m temperature, retrieved through the AI-WQ package, as the verifying target. Quintile boundaries follow the competition definition: 20-year ERA5 climatology, sample widened over ±4 days.
- No observational station data and no satellite data.

### 5. Model architecture
- **Preprocessing**:
  - average the daily means into the two target weeks (Monday–Sunday: days 19–25 and 26–32 after the Thursday initialisation);
  - express each forecast relative to the model's own reforecast climate, which removes the lead-dependent bias of the IFS.
- **Calibration**:
  - refitted every week on the reforecast/ERA5 pairs of the same model version date, so that training always matches the current IFS cycle and the current season (on-the-fly calibration);
  - predictors: ensemble-mean anomaly and ensemble spread. Algorithm: `[TO CONFIRM: e.g. multinomial or ordinal logistic regression, pooling over grid points]`.
- **Ensemble size**: the reforecasts have 11 members and the real-time ensemble 101. Predictors are computed in a way that is robust to this difference `[TO CONFIRM: method]`.
- **Post-processing**: probabilities are clipped to [0, 1] and renormalised to sum to 1. There are no missing values (format check stricter than the official one).
- **Frameworks**: Python, xarray, scikit-learn. The chain runs automatically every week on GitHub Actions.

### 6. Publications / presentations
No publication. The code and the method notes are public: https://github.com/benlanrezac-star/ai-weather-quest

### 7. Validation before submission
- Leave-one-year-out cross-validation over the 20 reforecast years. The ERA5 quintile boundaries are recomputed without the held-out year, to avoid leakage.
- Score: RPSS against climatology, with the same convention as the competition: cos(latitude) weights, land points ≥ 50 %, period score taken as a ratio of summed RPS. Our scoring code was checked against the AI-WQ package.
- Baselines: climatology, and raw IFS quintile probabilities. The raw IFS is used for validation only and is never submitted.
- Results: `[TO CONFIRM: validation RPSS for weeks 3 and 4, vs raw IFS]`. `[TO CONFIRM: offline check on winter 2025/26]`.

### 8. Challenges and how they were addressed
- **Reforecasts are produced on the fly with the current IFS cycle, and the cycle changed in 2026.** No winter reforecast of the current cycle existed before the competition, hence the weekly on-the-fly calibration.
- **Data latency.** The S2S data have a 48 h delay, and the ECDS queue was measured at over an hour for a single request. The weekly job therefore runs on Saturday, retries on Sunday, and falls back to climatology. `[TO CONFIRM: final scheduling]`
- **Ensemble size differs** between real time (101 members) and reforecasts (11 members); see question 5.

### 9. Limitations and future work
- One variable only (`tas`). No `mslp` or `pr`, and no MJO or tropical cyclone products.
- Small training sample per week (20 years × 11 members), so the model has few parameters.
- No large-scale drivers (MJO, ENSO, stratosphere) used as predictors yet.
- The model depends on the ECDS service. If it is unavailable, the submission falls back to climatology (zero skill that week).

### 10. Other components or innovations
- Fully automated, reproducible weekly chain: data retrieval, calibration, format checks, submission and storage of the scores in a public repository.
- Explicit controls against data leakage: data cut-off at initialisation time, reforecast version date on or before the initialisation, year-held-out quintile boundaries.

### 11. Contributors
- **Benjamin Lanrezac**: everything (data preparation, model design, validation, automation).
- `[TO CONFIRM: whether to mention the use of an AI coding assistant]`
