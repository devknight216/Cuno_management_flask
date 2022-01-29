import os
import config
from flask import Flask, request, make_response, render_template, jsonify
from utils.credentials_form import do_submit_credentials_form
from utils.subprocess_helpers import run_extra_env

# Render methods
def render_tabbed_content(provider, file):        
    return render_template("tabbed-content.html.jinja", provider=provider, file=file)

# @param creds is required to at least contain { "S3": [], "AZ": [], "GS": []}
def render_tabbed_page(provider, filename, creds):
    doc = render_template("tabbed-page.html.jinja", credentials=creds)
    if creds and provider and filename: 
        content = render_tabbed_content(provider, filename)
    else:
        content = "<h1>You will need to import some credentials to get started.</h1>"
    doc = doc.replace("<!--###initialtabcontent###-->", content)
    return doc

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
    
    @app.route("/tabbed-page")
    def tabbed_page():
        creds = {
            "S3": [],
            "AZ": ["file_name_4", "file_name_5", "file_name_6"],
            "GS": ["file_name_6", "file_name_7", "file_name_8"]
        }
        try: 
            provider = request.args["provider"]
        except:
            provider = None
        try:
            filename = request.args["filename"]
        except:
            filename = None
        
        if not provider or not filename or not filename in creds[provider]: 
            for p in creds: 
                if creds[p]:
                    provider = p
                    filename = creds[p][0]
                    break
        doc = render_tabbed_page(provider, filename, creds)
        return make_response(doc)

    @app.route("/api/generate-tabbed-content")
    def tabbed_content():
        return make_response(render_tabbed_content(provider=request.args["provider"], file=request.args["file"]))
<<<<<<< HEAD
    
    @app.route("/credentials-form")
    def credentials_form():
        settings = {
            "filepath": "/absolute/path",
            "filename": "foo",
            "access-key-id": "XXX-XXXX-XXXX-XXXX-XXX",
            "access-key": "XXX-XXXX-XXXX-XXXX-XXX",
            "endpoint": "",
            "pathstyle": True,
            "skipssl": False,
            "nossl": False
        }

        return make_response(render_template("credentials-form.html.jinja", settings=settings))
=======
>>>>>>> f768c84d6466a847ef02fe191112707ac4fa9b4e

    return app

    

if __name__ == "__main__":
    create_app().run(host='0.0.0.0')
