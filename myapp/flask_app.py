import os
import config
from flask import Flask, request, make_response, render_template, jsonify
from utils.credentials_form import do_submit_credentials_form
from utils.subprocess_helpers import run_extra_env

# For simple next-request user feedback, one can use "Message Flashing" https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/

# Create app and set config 
def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None: 
        if app.config["ENV"] == "production":
            app.config.from_object("config.ProductionConfig")
        else:
            app.config.from_object("config.DebugConfig")
    else:
        app.config.from_object(test_config)
    
    @app.route("/")
    def hello():
        # if app.config["DEBUG"]:
        #     return "<h1 style='color:blue'>Hello There! (debug)</h1>"
        # else:
        #     return "<h1 style='color:blue'>Hello There! (production)</h1>"
        return make_response(render_template("hello.html.jinja", some_var="foo"))

    # Example of how to load a static html web page 
    # TODO: should use flask.send_file instead
    @app.route("/hello.html")
    def html_hello():
        with open("static/test.html", "r") as f:
            doc = f.read()
        return doc

    @app.route("/config-base.html")
    def html_base():
        return make_response(render_template("config-base.html.jinja"))

    @app.route("/single-input.html")
    def html_single_input():
        left_val = request.cookies.get("left-path-value") or "/left/default"
        right_val = request.cookies.get("right-path-value") or "/right/default"
        return make_response(render_template("single-pathinput.html.jinja", pathinput_initial_left_value=left_val, pathinput_initial_right_value=right_val))

    @app.route("/2-inputs.html")
    def html_2inputs():
        return make_response(render_template("page-with-2-pathinputs.html.jinja", A_initial_left_value="/the/initial/A/left/value", A_initial_right_value="/A/right/value", B_initial_left_value="/some/path", B_initial_right_value="/other"))

    # See https://hackersandslackers.com/flask-routes/ 
    @app.route("/api/<int:version>/test/", methods=['GET', 'POST', 'PUT'])
    def test_api_endpoint(version):
        response = make_response(
            '"content": "The version requested was \n{} \n\nRequest args: \n{} \n\nRequest data: \n{} \n\nRequest form: \n{} \n\nRequest headers: \n{}"'.format(version, request.args, request.data, request.form, request.headers),
            200
        )
        response.headers["Content-Type"] = "application/json"
        response.headers["Custom-response-header"] = "foo"
        return response

    @app.route("/api/submit_credentials", methods=['POST'])
    def submit_credentials_form():
        return do_submit_credentials_form()

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
