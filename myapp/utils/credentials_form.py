from flask import make_response, jsonify

class form_issue:
    def __init__(self, input_name, error_title, error_message):
        self.input_name = input_name
        self.error_title = error_title
        self.error_message = error_message

def credentials_form_error_response(num_issues, issues, full_log="", full_errorlog=""):
    response = make_response(jsonify({"input-issues": num_issues, "issues": issues, "full_log": full_log, "full_errorlog": full_errorlog}), 400)
    # TODO: fill headers as necessary
    response.headers["Content-Type"] = "application/json"
    # response.headers["Custom-response-header"] = "foo"
    return response

def do_submit_credentials_form():
    # TODO: fill these variables from the request args and JSON body accessible via request.args, request.data
    filepath = None
    new_filename = None
    # access-key-id, access-key, etc. 

    # TODO: validate and sanitise inputs, collecting issues/errors into an issue_list (list of objects of type form_issue)
    #       In particular, if an endpoint is provided we should be checking that it is accessible (ping using Python urllib)
    # TODO: if issue_list is non-empty, return credentials_form_error_response

    # TODO: check that the file specified at filepath exists

    # TODO: parse the file using a custom parser into a Credentials object 

    # TODO: add/remove/edit credentials object as necessary depending on the arguments/request data
    
    # TODO: overwrite the existing file with the edits
    # Note: file owner/mode/permissions must not change when this is done so it is not sufficient to delete the old and write a new file.

    # If the filename has changed (filename/filepath no longer agree) then:
    #  TODO: rename the file
    #  TODO: list all files in ../bucketstore; and replace any references to the old filename with the new file name. 
    # Note: file owner/mode/permissions must not change when this is done so it is not sufficient to delete the old and write a new file.

    # TODO: if everything is ok return 200 OK
    response = make_response(
        jsonify({'OK' : 'in json'}),
        200
    )
    # TODO: fill headers as necessary
    response.headers["Content-Type"] = "application/json"
    # response.headers["Custom-response-header"] = "foo"
    return response
