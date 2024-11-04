from flask import Flask

from app import App

flask = Flask(__name__)

app = App()

@flask.route('/board', methods=['GET'])
def get_steps():
  return app.get_steps()

@flask.route('/board/reset', methods=['POST'])
def reset():
  app.reset()

@flask.route('/board/solve', methods=['POST'])
def solve():
  app.solve()

if __name__ == '__main__':
  flask.run(debug=True)
