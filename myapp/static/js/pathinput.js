function pathInputSubmit(left_id, middle_id, right_id, update_cookie, container_id, endpoint) {
    // TODO: use jQuery to get the input values from the elements with left_id, middle_id and right_id
    left_value = "";
    middle_value = "";
    right_value = "";
    // TODO: if update_cookie == true, then update the cookie values (for the current page) using js-cookie library https://github.com/js-cookie/js-cookie
    // Note that this cookie scheme assumes there is a single path input component on the page, and this is adequate. Pages with multiple path input components will not need to persist the values. 
    if (update_cookie) {
        Cookies.set('left-path-value', left_value, { expires: 365, path: '' });
        Cookies.set('right-path-value', right_value, { expires: 365, path: '' });
        // TODO: refresh the current page
        return;
    }

    if (container_id != "") {
        // TODO: replace a <div> in the current page with id=container_id with the result of an AJAX call to the endpoint provided passing the left, middle and right values as arguments
        // TODO: handle any errors
        return;
    }
}