from flask import request, jsonify
from datetime import datetime as dt
from flask import current_app as app
from flask_cors import cross_origin
from .data_models import db, Respondent, State
import uuid
import json

from .design_logic import BasicBWD as design_logic_cls


@app.route('/', methods=['POST'])
@cross_origin()
def add_record():
    """Create a user via query string parameters."""
    now = dt.now()
    design_logic = design_logic_cls()

    n_state = State.query.count()
    print(n_state)
    if n_state == 0:
        current_state = design_logic.initial_state()
    else:
        state_data = State.query.get(n_state)
        current_state = json.loads(state_data.state)

    covariates = design_logic.process(request.values)

    assignment, new_state = design_logic.assign(current_state, covariates)
    resp = Respondent(
        anonid=str(uuid.uuid4()),
        assignment=assignment,
        data=json.dumps(covariates),
        created=now,
    )
    db.session.add(resp)
    st = State(
        update_time=now,
        state=json.dumps(new_state)
    )
    db.session.add(st)
    db.session.commit()
    return jsonify({'assignment': assignment})


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return "Reset successful."


@app.route('/test')
def test_post():
    return """
    <form action="/", method="POST">
    <div>
        <label for="gender">What gender do you identify as?</label>
        <select id="gender" name="gender">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Non-binary">Non-binary</option>
            <option value="Other">Other</option>
        </select>
    </div>
    <div>
        <label for="ideology">What is your ideology?</label>
        <select id="ideology" name="ideology">
            <option value="-2">Very Liberal</option>
            <option value="-1">Liberal</option>
            <option value="0">Moderate</option>
            <option value="1">Conservative</option>
            <option value="2">Very Conservative</option>
        </select>
    </div>
    <div>
        <button>Send POST</button>
    </div>
    </form>
    """
