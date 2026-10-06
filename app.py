"""Rosa's Pizza: find the most profitable delivery promise for a zone and time block.

Run with:  streamlit run app.py
"""
import streamlit as st

from logic import COSTS, TIME_BLOCKS, ZONES, best_promise

st.set_page_config(page_title="Rosa's Delivery Promise", page_icon="🍕")
st.title("🍕 Rosa's Delivery Promise")
st.write(
    "Pick a zone and time block, choose which promised delivery times to try, "
    "and set the costs. The app finds the promise that gives the highest net "
    "profit over four weeks of simulated orders."
)

# --- Inputs -----------------------------------------------------------------
col1, col2 = st.columns(2)
zone = col1.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
time_block = col2.selectbox("Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve"))

st.subheader("Promised times to try (minutes)")
col1, col2, col3 = st.columns(3)
p_min = col1.number_input("Minimum", value=5, step=1)
p_max = col2.number_input("Maximum", value=80, step=1)
p_step = col3.number_input("Step", value=5, step=1)

st.subheader("Costs")
col1, col2, col3 = st.columns(3)
margin = col1.number_input(
    "Profit margin per order ($)", min_value=0.0, value=COSTS["margin"], step=0.5
)
churn_orders = col2.number_input(
    "Churn per late order (future orders lost)",
    min_value=0.0, value=COSTS["churn_orders"], step=0.1,
)
refund = col3.number_input(
    "Refund cost per late order ($)", min_value=0.0, value=COSTS["refund"], step=0.5
)

# --- Validation -------------------------------------------------------------
if p_min <= 0:
    st.error("The minimum promise must be above 0 minutes.")
    st.stop()
if p_max <= p_min:
    st.error("The maximum promise must be greater than the minimum.")
    st.stop()
if p_step <= 0:
    st.error("The step must be a positive number of minutes.")
    st.stop()

promises = list(range(int(p_min), int(p_max) + 1, int(p_step)))
costs = {"refund": refund, "churn_orders": churn_orders, "margin": margin}
inputs = {
    "zone": zone,
    "time_block": time_block,
    "promises": promises,
    "step": int(p_step),
    "costs": costs,
}

# --- Compute (mutates state only) -------------------------------------------
if st.button("Find best promise", type="primary"):
    best_p, best_profit = best_promise(zone, time_block, promises, costs)
    st.session_state["result"] = {
        "best_p": best_p,
        "best_profit": best_profit,
        "inputs": inputs,
    }

# --- Render -----------------------------------------------------------------
result = st.session_state.get("result")
if result is None:
    st.info("Set the inputs above, then click **Find best promise**.")
else:
    used = result["inputs"]
    used_promises = used["promises"]
    used_costs = used["costs"]

    st.divider()
    st.subheader(f"Result for {used['zone']} – {used['time_block']}")
    col1, col2 = st.columns(2)
    col1.metric("Recommended promise", f"{result['best_p']} min")
    col2.metric("Net profit (4 weeks)", f"${result['best_profit']:,.2f}")

    if result["best_p"] in (used_promises[0], used_promises[-1]):
        st.warning(
            f"The best promise ({result['best_p']} min) is at the edge of the range "
            f"tried ({used_promises[0]}–{used_promises[-1]} min). Widen the range "
            "and run again: a better promise may lie outside it."
        )

    st.caption(
        f"Computed for zone **{used['zone']}**, time block **{used['time_block']}**, "
        f"promises {used_promises[0]} to {used_promises[-1]} min "
        f"(step {used['step']}, "
        f"{len(used_promises)} values tried), margin ${used_costs['margin']:,.2f}/order, "
        f"churn {used_costs['churn_orders']:g} orders/late order, "
        f"refund ${used_costs['refund']:,.2f}/late order."
    )

    if used != inputs:
        st.info(
            "The inputs have changed since this result was computed. "
            "Click **Find best promise** to update it."
        )
