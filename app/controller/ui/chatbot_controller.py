from flask import Blueprint, request, redirect, render_template, flash
from app.database.connection import Connection


def chatbot_blueprint(db: Connection) -> Blueprint:
    bp_chatbot = Blueprint("chatbot", __name__)

    @bp_chatbot.route("/chatbot")
    def chatbot():

        return render_template('chatbot.html')

    return bp_chatbot