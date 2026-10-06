---
name: notebook-to-streamlit
description: Use when turning the analysis logic in a Jupyter notebook
  into a Streamlit app, such as the delivery-promise notebook for Rosa.
  Covers extracting notebook functions into a module, mapping notebook
  inputs to widgets, and rerun-safe state. Not for building a Streamlit
  app from scratch, not for changes to the notebook alone.
---


## Step 1 — Extract pure core
Read the notebook and copy its working logic (`total_cost`,
`net_profit`, `best_promise`) into `logic.py`. That module has no
printing, no Streamlit imports and no hard-coded costs: every
function takes `costs` as an argument. Import `delivery_times`,
`ZONES`, `TIME_BLOCKS`, `COSTS` and `PROMISE` from `starter.py`.
Read the real key names in `COSTS` from `starter.py`; do not guess
them. Keep `seed=1` in every `delivery_times()` call so the app
matches the notebook.

Before building any UI, run `best_promise` from `logic.py` for
Far West, Fri/Sat eve, promises 5 to 80 in steps of 5, with `COSTS`,
and confirm it returns the same promise and net profit as the
notebook.

## Step 2 — Map the interface

| Notebook | Streamlit |
|---|---|
| zone argument | `st.selectbox` over `ZONES` |
| time block argument | `st.selectbox` over `TIME_BLOCKS` |
| `promises = list(range(5, 85, 5))` | number inputs for minimum, maximum and step; defaults 5, 80, 5 |
| `COSTS` values | one `st.number_input` each for profit margin per order, churn per late order and refund cost per late order; defaults from `COSTS` |
| calling `best_promise(...)` | runs only when the user clicks a "Find best promise" button |
| `print(...)` of the result | `st.metric` / `st.write`, outside the button block |
| invalid input | `st.error(...)` then `st.stop()` |

Defaults must match the notebook's, so the app gives the notebook's
answer out of the box.

Validate before computing: the minimum promise must be above 0, the
maximum must be greater than the minimum, and the step must be
positive. Build the costs dictionary from the widget values using
the same keys as `COSTS`, and pass it to `best_promise`.

## Step 3 — State discipline

Streamlit reruns the whole script on every widget interaction.

- The `if st.button(...)` block should **mutate state only**: run
  `best_promise` and save the result, plus the inputs it was run
  with, in `st.session_state`.
- Rendering happens outside that block, reading from
  `st.session_state` unconditionally.
- Show which zone, time block, range and costs the displayed result
  came from, so a result is never mistaken for one from changed
  inputs.
- If the best promise equals the minimum or maximum of the range,
  show a warning that the range should be widened (the edge check
  from the notebook).

## Step 4 — Ready to deploy

- The app file is `app.py` in the repository root, next to
  `starter.py` and `logic.py`.
- `requirements.txt` lists `streamlit` and `numpy`.
- No absolute file paths anywhere.

## Done when

- [ ] `logic.py` gives the same result as the notebook for Far West,
      Fri/Sat eve with the default inputs
- [ ] `streamlit run app.py` works locally
- [ ] The app has been tested: click the button, then change another
      widget, and confirm the result doesn't disappear
- [ ] An invalid range shows an error instead of crashing
