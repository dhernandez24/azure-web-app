from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from flask import Flask, abort, render_template

from azure_web_app import auth, db
from azure_web_app._constants import SECRET_ENV_FILE

FAVORITES = [
    {"id": 1, "title": "Chocolate", "why": "Chocolate makes me happy."},
    {"id": 2, "title": "Arcade", "why": "I love playing arcade games."},
    {"id": 3, "title": "Hunter x Hunter", "why": "My favorite anime is Hunter x Hunter."},
]

MOVIES = [
    {"id": 1, "title": "Spirited Away", "Thoughts": "I am a sucker for great amimation and this movie is a masterpiece."},
    {"id": 2, "title": "The Prince of Egypt", "Thoughts": "Underrated movie, breathtaking animation and even bettersoundtrack."},
    {"id": 3, "title": "Interstellar", "Thoughts": "Extremely interesting, amazing sound track and great acting."},
]


def create_app():
    load_dotenv(find_dotenv(SECRET_ENV_FILE))
    app = Flask(__name__)
    db.setup_for_app(app)
    auth.setup_auth(app)
    setup_routes(app)
    return app


def index():
    return render_template(
        "index.html",
        name= "Dalila",

        hobby="Painting",
        fun_fact="I went to Tokyo this winter",
        hours_per_week=4, 
        hour=datetime.now().hour,
        show_counter=False,
        favorites=FAVORITES,
        movies=MOVIES
    )


def movies(movie_id: int):
    for movie in MOVIES:
        if movie["id"] == movie_id:
            return render_template("movies.html", movie=movie)

    abort(404)
    

def movies_list():
    return render_template("movies_list.html", movies=MOVIES)

    
def favorite_detail(favorite_id: int):
    for favorite in FAVORITES:
        if favorite["id"] == favorite_id:
            return render_template("favorite.html", favorite=favorite)
    abort(404)


def setup_routes(app):
    app.route("/")(index)
    app.route("/favorites/<int:favorite_id>")(favorite_detail)
    app.route("/movies/<int:movie_id>")(movies)
    app.route("/movies")(movies_list)


def run_app(debug: bool = True) -> None:
    app = create_app()
    app.run(debug=debug)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
