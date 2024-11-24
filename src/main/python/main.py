from flask import Flask
from flask_cors import cross_origin

from app import App

flask = Flask(__name__)
app = App()

@flask.errorhandler(ValueError)
def handle_bad_request(e: Exception):
  return str(e), 400

@flask.route('/board/<string:solver_name>/solve', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def get_steps(solver_name: str):
  print(solver_name)
  return app.get_steps(solver_name)

if __name__ == '__main__':
    flask.run()