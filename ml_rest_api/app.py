import os
import sys
import logging.config
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask, Blueprint
from ml_rest_api.settings import get_value
from ml_rest_api.ml_trained_model.wrapper import trained_model_wrapper
import ml_rest_api.api.health.liveness
import ml_rest_api.api.health.readiness
import ml_rest_api.api.model.predict
from ml_rest_api.api.restplus import api

app = Flask(__name__)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(flask_app):
    settings_to_apply = [
        #'FLASK_SERVER_NAME',
        'SWAGGER_UI_DOC_EXPANSION',
        'RESTPLUS_VALIDATE',
        'RESTPLUS_MASK_SWAGGER',
        'SWAGGER_UI_JSONEDITOR',
        'ERROR_404_HELP',
    ]
    for key in settings_to_apply:
        flask_app.config[key] = get_value(key)

def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)
    trained_model_wrapper.init()

def main():
    initialize_app(app)
    log.info('***** Starting development server at http://{}/api/ *****'.format(get_value('FLASK_SERVER_NAME')))
    app.run(debug=get_value('FLASK_DEBUG'), port=get_value('FLASK_PORT'), host=get_value('FLASK_HOST'))

if __name__ == "__main__":
    main()