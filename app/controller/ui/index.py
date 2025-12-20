from flask import Blueprint, request, redirect, render_template, flash

@app.route('/index')
def index(app):
    return "<h1>Index</h1>"