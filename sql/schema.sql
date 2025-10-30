-- Staging tables
CREATE TABLE IF NOT EXISTS stg_social (
	platform TEXT,
	post_id TEXT,
	author TEXT,
	timestamp TIMESTAMP,
	text TEXT,
	engagements INT
);

CREATE TABLE IF NOT EXISTS stg_reviews (
	source TEXT,
	review_id TEXT,
	timestamp TIMESTAMP,
	rating FLOAT,
	title TEXT,
	text TEXT
);

CREATE TABLE IF NOT EXISTS stg_web_analytics (
	session_id TEXT,
	user_id TEXT,
	timestamp TIMESTAMP,
	utm_source TEXT,
	utm_medium TEXT,
	utm_campaign TEXT,
	event TEXT,
	product TEXT
);

CREATE TABLE IF NOT EXISTS stg_transactions (
	order_id TEXT,
	user_id TEXT,
	timestamp TIMESTAMP,
	product TEXT,
	price FLOAT,
	qty INT,
	channel TEXT
);

CREATE TABLE IF NOT EXISTS stg_campaigns (
	campaign_id TEXT,
	channel TEXT,
	start TIMESTAMP,
	end TIMESTAMP,
	budget FLOAT,
	target_product TEXT
);

-- Modeled tables (examples)
CREATE TABLE IF NOT EXISTS dim_users (
	user_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS fct_orders (
	order_id TEXT PRIMARY KEY,
	user_id TEXT,
	order_ts TIMESTAMP,
	product TEXT,
	revenue FLOAT,
	qty INT,
	channel TEXT
);

CREATE TABLE IF NOT EXISTS fct_sentiment_daily (
	date DATE,
	source TEXT,
	avg_sentiment FLOAT,
	post_count INT
);
