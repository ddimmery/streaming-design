from flask import request, jsonify, render_template_string
from datetime import datetime as dt
from flask import current_app as app
from flask_cors import cross_origin
import uuid
import json
import requests
import traceback

from config import Config
from . import redis
from .data_models import db, Respondent, State
from .design import design_factory
from .processor_config import process_cfg_factory
from .redis import update_redis, get_state_data


@app.route('/', methods=['POST'])
@cross_origin()
def add_record_api():
    app.logger.info(request.values)
    print(request.values)
    return add_record(request.values)


def add_record(req_args):
    now = dt.now()
    cfg = Config()
    processor = process_cfg_factory(cfg.PROCESSOR_NAME)()
    design = design_factory(cfg.DESIGN_NAME)(processor.covariate_length())

    uid = req_args.get('userid')
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
        app.logger.info(req_args)
        covariates = processor.process(req_args)

        assignment, new_state = design.assign(current_state, covariates)
        status = "SUCCESS"
    except (ValueError, KeyError, TypeError):
        app.logger.error(
            "Reverting to backup design."
        )
        status = "FAILED"
        app.logger.error(traceback.print_exc())
        assignment = design.backup_assign(current_state)
        covariates = req_args
        new_state = current_state
    app.logger.warn(req_args)
    app.logger.warn(json.dumps(req_args))
    resp = Respondent(
        userid=uid if uid is not None else str(uuid.uuid4()),
        assignment=assignment,
        data=json.dumps(req_args),
        status=status,
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
    app.logger.info({'status': status, 'assignment': assignment})
    return jsonify({'assignment': assignment})


@app.route('/', methods=["GET"])
def dashboard():
    return render_template_string("""
<!doctype html>
<html>
<body>
    <p><a href="{{ url_for('reset') }}">Reset the app!</a></p>
    <p><a href="{{ url_for('test_post') }}">Send a test POST request.</a></p>
</body>
</html>
    """)


@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    db.session.commit()
    r_keys = redis.keys('*')
    if len(r_keys) > 0:
        redis.delete(*r_keys)
    return render_template_string("""
<!doctype html>
<html>
<body>
    <p>Reset Successful.</p>
    <p><a href="{{ url_for('dashboard') }}">Return to dashboard.</a></p>
</body>
</html>
    """)


@app.route('/test')
def test_post():
    # construct dict to send
    cfg = Config()
    processor = process_cfg_factory(cfg.PROCESSOR_NAME)()
    cov = processor.mock_config()
    uid = request.values.get('userid')
    if uid is None:
        cov['userid'] = str(uuid.uuid4())
    return add_record(cov)