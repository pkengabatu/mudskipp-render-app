from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# temporary storage (no database yet)
provinces = ["Honiara", "Malaita", "Western", "Choiseul"]

# HOME
@app.route("/")
def home():
    return render_template_string("""
    <h1>Province CRUD System</h1>
    <ul>
        <li><a href="/provinces">View Provinces</a></li>
        <li><a href="/add">Add Province</a></li>
    </ul>
    """)

# READ (LIST)
@app.route("/provinces")
def list_provinces():
    html = "<h2>Provinces</h2><ul>"
    for i, p in enumerate(provinces):
        html += f"""
        <li>
            {p}
            <a href="/edit/{i}">Edit</a>
            <a href="/delete/{i}">Delete</a>
        </li>
        """
    html += "</ul><a href='/'>Back</a>"
    return html

# CREATE
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        provinces.append(name)
        return redirect("/provinces")

    return """
    <h2>Add Province</h2>
    <form method="post">
        <input name="name" placeholder="Province name">
        <button type="submit">Add</button>
    </form>
    <br><a href='/'>Back</a>
    """

# UPDATE
@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    if request.method == "POST":
        provinces[index] = request.form["name"]
        return redirect("/provinces")

    return f"""
    <h2>Edit Province</h2>
    <form method="post">
        <input name="name" value="{provinces[index]}">
        <button type="submit">Update</button>
    </form>
    <br><a href='/provinces'>Back</a>
    """

# DELETE
@app.route("/delete/<int:index>")
def delete(index):
    provinces.pop(index)
    return redirect("/provinces")

if __name__ == "__main__":
    app.run()
