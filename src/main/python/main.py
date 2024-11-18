from flask import Flask

from app import App

flask = Flask(__name__)
app = App()

@flask.route('/board/<string:solver_name>/solve', methods=['GET'])
def get_steps(solver_name: str):
  print(solver_name)
  return app.get_steps(solver_name)

if __name__ == '__main__':
  flask.run()