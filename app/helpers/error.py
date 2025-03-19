from flask import render_template

def error(message, code=400):
    return render_template("error.html", code=code, message=message), code