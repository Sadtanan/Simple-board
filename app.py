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

PER_PAGE = 10

@app.route("/")
def index():
    conn = get_db()
    cursor = conn.cursor()
    
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "latest")
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    
    # Base filter for search
    if q:
        search_arg = f"%{q}%"
        where = "WHERE title LIKE ? OR content LIKE ?"
        count_args = (search_arg, search_arg)
        list_args = (search_arg, search_arg)
    else:
        where = ""
        count_args = ()
        list_args = ()
    
    # Total count (with search)
    cursor.execute(f"SELECT COUNT(*) FROM posts {where}", count_args)
    total = cursor.fetchone()[0]
    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = min(page, total_pages)
    offset = (page - 1) * PER_PAGE
    
    # Sort order
    order = {
        "latest": "id DESC",
        "oldest": "id ASC",
        "views": "views DESC",
        "title": "title ASC",
    }.get(sort, "id DESC")
    
    cursor.execute(
        f"SELECT * FROM posts {where} ORDER BY {order} LIMIT ? OFFSET ?",
        list_args + (PER_PAGE, offset),
    )
    posts = cursor.fetchall()
    conn.close()
    
    return render_template(
        "index.html",
        posts=posts,
        page=page,
        total_pages=total_pages,
        total=total,
        q=q,
        sort=sort,
    )

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

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        # Same validation as create
        if title and content:
            cursor.execute(
                "UPDATE posts SET title = ?, content = ? WHERE id = ?",
                (title, content, post_id)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("post_detail", post_id=post_id))
    
    # GET: Fetch post and pre-fill form
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    
    if post is None:
        conn.close()
        return "Post not found", 404
    
    conn.close()
    return render_template("edit_post.html", post=post)

@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
    if cursor.fetchone() is None:
        conn.close()
        return "Post not found", 404
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)