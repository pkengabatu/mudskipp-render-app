import os
import psycopg2
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')

# CREATE TABLE automatically (runs once on startup)
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS provinces (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# HOME
@app.route("/")
def home():
    return """
    <h1>Province System (Database Version)</h1>
    <a href="/provinces">View Provinces</a> |
    <a href="/add">Add Province</a>
    """

# READ
@app.route("/provinces")
def list_provinces():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM provinces")
    rows = cur.fetchall()
    conn.close()

    html = "<h2>Provinces</h2><ul>"
    for r in rows:
        html += f"""
        <li>
            {r[1]}
            <a href="/delete/{r[0]}">Delete</a>
        </li>
        """
    html += "</ul><a href='/'>Back</a>"
    return html

# CREATE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO provinces (name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()

        return redirect("/provinces")

    return """
    <h2>Add Province</h2>
    <form method="post">
        <input name="name" placeholder="Province name">
        <button type="submit">Add</button>
    </form>
    """

# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM provinces WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect("/provinces")

if __name__ == "__main__":
    app.run()
