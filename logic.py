"""Pure decision logic for Rosa's delivery promise, extracted from Assignment1.ipynb.

No printing, no Streamlit and no hard-coded costs: every function takes
`costs` (a dict with the same keys as starter.COSTS) as an argument.
"""
import numpy as np

from starter import COSTS, PROMISE, TIME_BLOCKS, ZONES, delivery_times

__all__ = ["COSTS", "PROMISE", "TIME_BLOCKS", "ZONES", "total_cost", "net_profit", "best_promise"]


def total_cost(costs):
    """Total cost of one late order: refund plus lost future margin."""
    return costs["refund"] + costs["churn_orders"] * costs["margin"]


def net_profit(z, t_b, p, costs):
    """Net profit for zone `z`, time block `t_b` and promise `p` minutes."""
    order_times = delivery_times(z, t_b, p, seed=1)
    late_orders = np.sum(order_times > p)
    sales = costs["margin"] * len(order_times)
    late_costs = late_orders * total_cost(costs)
    return float(sales - late_costs)


def best_promise(z, t_b, promise_list, costs):
    """Return (best promise, its net profit) over the promises in `promise_list`."""
    best_p = None
    best_profit = float("-inf")
    for p in promise_list:
        profit = net_profit(z, t_b, p, costs)
        if profit > best_profit:
            best_profit = profit
            best_p = p
    return best_p, best_profit
