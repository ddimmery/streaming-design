from flask import request, jsonify
from datetime import datetime as dt
from flask import current_app as app
from flask_cors import cross_origin
from .data_models import db, Respondent, State
from . import redis
import uuid
import json
import traceback

from config import Config
from .design import design_factory
from .processor_config import process_cfg_factory
from .redis import update_redis, get_state_data


@app.route('/', methods=['POST'])
@cross_origin()
def add_record():
    """Create a user via query string parameters."""
    now = dt.now()
    cfg = Config()
    processor = process_cfg_factory(cfg.PROCESSOR_NAME)()
    design = design_factory(cfg.DESIGN_NAME)(processor.covariate_length())

    uid = request.values.get('userid')
    if uid is None:
        app.logger.warning("userid not provided.")
    else:
        uid_result = Respondent.query.get(uid)
        if uid_result is not None:
            return jsonify({'assignment': uid_result.assignment})

    sample_size = redis.get("sample_size")
    try:
        sample_size = int(sample_size)
    except TypeError:
        sample_size = 0

    if sample_size == 0:
        current_state = design.initial_state()
        redis.set('sample_size', 1)
    else:
        current_state = get_state_data(redis, design.state_keys())
        redis.set('sample_size', sample_size + 1)

    try:
        covariates = processor.process(request.values)

        assignment, new_state = design.assign(current_state, covariates)
    except (ValueError, KeyError, TypeError):
        app.logger.error(
            "Reverting to backup design."
        )
        app.logger.error(traceback.print_exc())
        assignment = design.backup_assign(current_state)
        covariates = request.values
        new_state = current_state

    resp = Respondent(
        userid=uid if uid is not None else str(uuid.uuid4()),
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
    update_redis(redis, new_state)
    return jsonify({'assignment': assignment})


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    db.session.commit()
    r_keys = redis.keys('*')
    redis.delete(*r_keys)
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
        <label for="twitteruse">What is your twitter use?</label>
        <select id="twitteruse" name="twitteruse">
            <option value="-2">-2</option>
            <option value="-1">-1</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
    </div>
    <div>
        <label for="politicaluse">What is your politicaluse?</label>
        <select id="politicaluse" name="politicaluse">
            <option value="-2">-2</option>
            <option value="-1">-1</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
    </div>
    <div>
        <label for="seepoltweets">What is your seepoltweets?</label>
        <select id="seepoltweets" name="seepoltweets">
            <option value="-2">-2</option>
            <option value="-1">-1</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
    </div>
    <div>
        <label for="poltweetsvideo">What is your poltweetsvideo?</label>
        <select id="poltweetsvideo" name="poltweetsvideo">
            <option value="-2">-2</option>
            <option value="-1">-1</option>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
        </select>
    </div>
    <div>
        <button>Send POST</button>
    </div>
    </form>
    """
