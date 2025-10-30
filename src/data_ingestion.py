import argparse
import os
import re
from typing import Dict, List

import pandas as pd
import yaml


def load_raw_data(config: Dict) -> Dict[str, pd.DataFrame]:
	paths = config.get("data", {})
	dfs: Dict[str, pd.DataFrame] = {}
	for name, path in paths.get("external", {}).items():
		if not os.path.exists(path):
			raise FileNotFoundError(f"Missing input file for {name}: {path}")
		df = pd.read_csv(path)
		dfs[name] = df
	return dfs


def basic_text_clean(series: pd.Series) -> pd.Series:
	cleaned = (
		series.fillna("")
		.str.replace(r"\s+", " ", regex=True)
		.str.replace(r"http\S+", "", regex=True)
		.str.strip()
	)
	return cleaned


def clean_text_data(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
	result: Dict[str, pd.DataFrame] = {}
	if "social" in dfs:
		df = dfs["social"].copy()
		text_cols = [c for c in df.columns if c.lower() in {"text", "title", "content"}]
		for c in text_cols:
			df[c] = basic_text_clean(df[c])
		result["social"] = df
	if "reviews" in dfs:
		df = dfs["reviews"].copy()
		text_cols = [c for c in df.columns if c.lower() in {"text", "title", "content"}]
		for c in text_cols:
			df[c] = basic_text_clean(df[c])
		result["reviews"] = df
	return result


def write_interim(cleaned: Dict[str, pd.DataFrame], config: Dict) -> None:
	interim_dir = config.get("data", {}).get("interim_dir", "data/interim")
	os.makedirs(interim_dir, exist_ok=True)
	for name, df in cleaned.items():
		out_path = os.path.join(interim_dir, f"{name}.parquet")
		df.to_parquet(out_path, index=False)


def main() -> None:
	parser = argparse.ArgumentParser(description="Ingest and clean raw datasets")
	parser.add_argument("--config", required=True, help="Path to YAML config")
	args = parser.parse_args()

	with open(args.config, "r", encoding="utf-8") as f:
		config = yaml.safe_load(f)

	dfs = load_raw_data(config)
	cleaned = clean_text_data(dfs)
	write_interim(cleaned, config)
	print("Wrote interim cleaned datasets.")


if __name__ == "__main__":
	main()
