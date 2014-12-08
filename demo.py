from flask import Flask, request, jsonify, abort
import random

app = Flask(__name__)

def validate_int(num):
    """
    cast the num to int and return the value, return False if error occurs
    """
    try:
        return int(num)
    except ValueError:
        return False
    

class Game(object):
    total = 0
    now = 0
    selected = []
    result = None

    @classmethod
    def is_avaliable(cls):
        return cls.now != len(cls.selected)

    @classmethod
    def is_started(cls):
        return cls.total

    @classmethod
    def create_game(cls, total):
        assert total <= 15
        cls.total = total

    @classmethod
    def quit_game(cls):
        cls.total = 0
        cls.now = 0
        cls.selected = []
        cls.result = None

    @classmethod
    def select_num(cls, num):
        cls.selected.append(num)
        if len(cls.selected) == cls.total:
            cls.result = random.choice(cls.selected)

    @classmethod
    def is_selected(cls, num):
        return num in cls.selected

    @classmethod
    def is_full(cls):
        return cls.total == cls.now

    @classmethod
    def is_end(cls):
        return cls.total == len(cls.selected)


@app.route('/demo/init_game', methods=['POST'])
def init_game():
    if request.form is None or 'total' not in request.form:
        abort(404)
    total = validate_int(request.form['total'])
    if not total or total > 15:
        abort(400)
    if Game.is_started():
        return jsonify(status=False)
    Game.create_game(total)
    Game.now += 1
    return jsonify(status=True, total=Game.total, selected=Game.selected)

@app.route('/demo/start', methods=['POST'])
def start():
    if Game.total == 0:
        return jsonify(status=False)
    else:
        if Game.is_full():
            return jsonify(status=True, is_full=True)
        else:
            Game.now += 1
            print 'after add', Game.now
            return jsonify(status=True, is_full=False, total=Game.total, selected=Game.selected)

@app.route('/demo/get_selected', methods=['POST'])
def get_selected():
    print 'now', Game.now
    if Game.is_started():
        if not Game.is_end():
            return jsonify(status=True, total=Game.total, selected=Game.selected)
        return jsonify(status=True, total=Game.total, selected=Game.selected, result=Game.result)
    else:
        return jsonify(status=False)

@app.route('/demo/select', methods=['POST'])
def select():
    if 'num' not in request.form:
        abort(404)
    num = validate_int(request.form['num'])
    if Game.is_end() or num not in range(Game.total) or not Game.is_avaliable():
        abort(400)
    if num not in Game.selected:
        Game.select_num(num)
        if Game.is_end():
            return jsonify(status=True, total=Game.total, selected=Game.selected, result=Game.result)
        return jsonify(status=True, total=Game.total, selected=Game.selected)
    else:
        return jsonify(status=False, total=Game.total, selected=Game.selected)

@app.route('/demo/quit', methods=['POST'])
def quit():
    if Game.is_end():
        Game.quit_game()
        return jsonify(status=True)
    else:
        return jsonify(status=False)

if __name__ == '__main__':
    print app.url_map
    app.run(debug=True)
