import os
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for

from characters import characters
from equipment import EquipmentData
from hero import Player, Hero, Enemy
from utils import load_equipment

app = Flask(__name__)
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EQUIPMENT: EquipmentData = load_equipment()
heroes: Dict[str, Hero] = dict()

def render_choose_character(**kwargs) -> str:
    return render_template(
        "hero_choosing.html",
        result={
            "classes": characters.keys(),
            "weapons": EQUIPMENT.weapon_names,
            "armors": EQUIPMENT.armor_names,
            **kwargs,
        })


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == "GET":
        return render_choose_character(header="Выберите героя", next_button="Выбрать врага")
    if request.method == "POST":
        heroes["player"] = Player(
            name=request.form["name"],
            class_=characters[request.form['unit_class']],
            weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
            armor=EQUIPMENT.get_armor(request.form["armor"]),
        )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == "GET":
        return render_choose_character(header="Выберите врага", next_button="Начать сражение")
    if request.method == "POST":
        heroes["enemy"] = Enemy(
            name=request.form["name"],
            class_=characters[request.form['unit_class']],
            weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
            armor=EQUIPMENT.get_armor(request.form["armor"]),
        )
    return redirect(url_for("start_fight"))


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    if "player" in heroes and "enemy" in heroes:
        return render_template("fight.html", heroes=heroes, result="Fight!")
    return redirect(url_for("menu_page"))


@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    pass


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    pass


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    pass


'''@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)'''

if __name__ == "__main__":
    app.run()
