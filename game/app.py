import os
from functools import wraps
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from characters import characters_
from controller import Game
from equipment import EquipmentData
from hero import Player, Hero, Enemy
from utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EQUIPMENT: EquipmentData = load_equipment()
heroes: Dict[str, Hero] = dict()
game = Game()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if game.game_processing:
            return func(*args, **kwargs)
        if game.game_results:
            return render_template("fight.html", heroes=heroes, battle_result=game.game_results)
        return redirect(url_for("menu_page"))
    return wrapper

def render_choose_character(**kwargs) -> str:
    return render_template(
        "hero_choosing.html",
        result={
            "classes": characters_.keys(),
            "weapons": EQUIPMENT.weapon_names,
            "armors": EQUIPMENT.armor_names,
            **kwargs,
        })


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/test")
def test_page():
    return "<h2>test text</h2>"


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        return render_choose_character(header="Выберите героя", next_button="Выбрать врага")
    if request.method == "POST":
        heroes["player"] = Player(
            name=request.form["name"],
            class_=characters_[request.form['unit_class']],
            weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
            armor=EQUIPMENT.get_armor(request.form["armor"]),
        )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        return render_choose_character(header="Выберите врага", next_button="Начать сражение")
    if request.method == "POST":
        heroes["enemy"] = Enemy(
            name=request.form["name"],
            class_=characters_[request.form['unit_class']],
            weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
            armor=EQUIPMENT.get_armor(request.form["armor"]),
        )
    return redirect(url_for("start_fight"))


@app.route("/fight/")
def start_fight():
    if "player" in heroes and "enemy" in heroes:
        game.run(**heroes)
        return render_template("fight.html", heroes=heroes, result="Fight!")
    return redirect(url_for("menu_page"))


@app.route("/fight/hit")
@game_processing
def hit():
    return render_template("fight.html", heroes=heroes, result=game.player_hit())


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    return render_template("fight.html", heroes=heroes, result=game.player_use_skill())


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    return render_template("fight.html", heroes=heroes, result=game.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
