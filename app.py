from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = "database.db"

def get_db():
    """Get database connection with row_factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if title and content:
            conn = get_db()
            cursor = conn.cursor()
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO posts (title, content, created_at, views) VALUES (?, ?, ?, ?)",
                (title, content, created_at, 0)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
    
    return render_template("create.html")

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Fetch the post
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    
    if post is None:
        conn.close()
        return "Post not found", 404
    
    #view count +1
    cursor.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (post_id,))
    conn.commit()
    
    # Fetch updated post with new view count
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    
    conn.close()
    return render_template("post_detail.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)