from typing import Iterable, List, Optional

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

try:
	from transformers import AutoModelForSequenceClassification, AutoTokenizer
	import torch
	extras_available = True
except Exception:
	extras_available = False


_vader = SentimentIntensityAnalyzer()


def score_sentiment_vader(texts: Iterable[str]) -> List[float]:
	scores: List[float] = []
	for t in texts:
		res = _vader.polarity_scores(t or "")
		scores.append(res["compound"])
	return scores


def score_sentiment_transformer(texts: Iterable[str], model_name: str) -> List[float]:
	if not extras_available:
		raise RuntimeError("transformers/torch not available. Install extras to use.")
	tokenizer = AutoTokenizer.from_pretrained(model_name)
	model = AutoModelForSequenceClassification.from_pretrained(model_name)
	model.eval()
	results: List[float] = []
	with torch.no_grad():
		for t in texts:
			inputs = tokenizer(t or "", return_tensors="pt", truncation=True)
			outputs = model(**inputs)
			logits = outputs.logits
			probs = torch.softmax(logits, dim=-1)[0]
			# Map to a signed score: (pos - neg)
			if probs.numel() == 3:
				score = float(probs[2] - probs[0])
			else:
				score = float(probs[-1] - probs[0])
			results.append(score)
	return results


def attach_sentiment(df: pd.DataFrame, text_col: str, method: str = "vader", model_name: Optional[str] = None) -> pd.DataFrame:
	out = df.copy()
	if method == "vader":
		out["sentiment"] = score_sentiment_vader(out[text_col].astype(str))
	elif method == "transformer":
		mn = model_name or "cardiffnlp/twitter-roberta-base-sentiment"
		out["sentiment"] = score_sentiment_transformer(out[text_col].astype(str), mn)
	else:
		raise ValueError(f"Unknown method: {method}")
	return out
