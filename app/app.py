from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def index():
	return render_template("index.html")


@app.get("/dashboard")
def dashboard():
	# Data can later be loaded from data/processed; using sample for now
	labels = ["iPhone", "iPad", "Mac", "Watch", "AirPods"]
	values = [120, 60, 85, 40, 55]
	return render_template("dashboard.html", labels=labels, values=values)


@app.get("/healthz")
def healthz():
	return {"status": "ok"}


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000, debug=False)
