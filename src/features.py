from typing import Tuple

import pandas as pd


def build_purchase_features(orders: pd.DataFrame) -> pd.DataFrame:
	orders = orders.copy()
	orders["order_ts"] = pd.to_datetime(orders["order_ts"]) if "order_ts" in orders else pd.to_datetime(orders["timestamp"])  # type: ignore
	orders["revenue"] = orders.get("revenue", orders.get("price", 0)) * orders.get("qty", 1)
	orders["order_date"] = orders["order_ts"].dt.date
	daily = (
		orders.groupby(["order_date"]).agg(orders=("order_id", "nunique"), revenue=("revenue", "sum")).reset_index()
	)
	return daily


def build_cohorts(orders: pd.DataFrame) -> pd.DataFrame:
	orders = orders.copy()
	orders["order_ts"] = pd.to_datetime(orders["order_ts"]) if "order_ts" in orders else pd.to_datetime(orders["timestamp"])  # type: ignore
	orders["order_month"] = orders["order_ts"].dt.to_period("M").dt.to_timestamp()
	first_purchase = orders.groupby("user_id")["order_month"].min().rename("cohort_month")
	orders = orders.join(first_purchase, on="user_id")
	orders["months_since"] = ((orders["order_month"].dt.year - orders["cohort_month"].dt.year) * 12 + (orders["order_month"].dt.month - orders["cohort_month"].dt.month))
	cohort = orders.groupby(["cohort_month", "months_since"]).agg(users=("user_id", "nunique")).reset_index()
	return cohort
