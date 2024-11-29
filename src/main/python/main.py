import logging

from flask import Flask, jsonify, request
from flask_cors import cross_origin

from app import App
from solver.hill_climbing import HillClimbing

logging.getLogger().setLevel(logging.DEBUG)

flask = Flask(__name__)
app = App()

@flask.errorhandler(ValueError)
def handle_bad_request(e: Exception):
  return str(e), 400

#TODO: update api to return final queen positions
@flask.route('/board/<string:solver_name>/solve', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def get_steps(solver_name: str):
    steps = app.get_steps(solver_name)
    duration = app.get_solve_duration()
    nodes_expanded = app.get_nodes_expanded()

    return {
        "steps": steps,
        "solveDuration": duration,
        "nodesExpanded": nodes_expanded
    }

@flask.route('/board/solvers/setup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def setup():
    print(request.args)
    limit = request.args.get('limit', type=int)
    side_moves = request.args.get('side_moves', type=int)
    if limit is None or side_moves is None:
        raise ValueError('Limit and side moves required')

    app.set_limit(limit)
    app.set_side_moves(side_moves)
    return 'ok'

@flask.route('/board/queens', methods=['GET'])
@cross_origin()
def get_queens():
    return app.get_queens()

if __name__ == '__main__':
    flask.run()
    # n = 8
    # bc = Backtracking(n)
    # bc.solve()
    # print('forward checking')
    # fc = ForwardChecking(n)
    # fc.solve()


def hill_climbing():
    hc = HillClimbing(8)
    solved_count = 0
    for i in range(100):
        hc.reset()
        hc.solve()
        # print(f"Score is {hc.solution_score} and steps are {hc.updates_count}")
        if hc.solution_score == 0:
            solved_count += 1
        # hc.print_board()
    print(f"{solved_count} and {(solved_count / 100) * 100}%")
