from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


def sentiment_trend_plot(df: pd.DataFrame, date_col: str = "date", sentiment_col: str = "avg_sentiment", launch_dates: Optional[list] = None):
	fig, ax = plt.subplots(figsize=(10, 4))
	df = df.sort_values(date_col)
	ax.plot(df[date_col], df[sentiment_col], label="Avg Sentiment")
	if launch_dates:
		for d in launch_dates:
			ax.axvline(pd.to_datetime(d), color="red", linestyle="--", alpha=0.6)
	ax.set_title("Sentiment Over Time")
	ax.legend()
	plt.tight_layout()
	return fig, ax


def funnel_plot(stages: pd.Series):
	fig, ax = plt.subplots(figsize=(6, 4))
	stages.plot(kind="bar", ax=ax)
	ax.set_title("Conversion Funnel")
	plt.tight_layout()
	return fig, ax
