from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # ยัง
        print(title, content)

    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True)