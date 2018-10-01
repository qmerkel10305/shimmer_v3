/**
 * Makes an API request
 * Note: callback is only called when there is no error.
 *
 * @param {String} type HTTP method (GET, POST, PUT, etc)
 * @param {String} path the URI of the request
 * @param {function} callback callback when the request is completed without an error
 * @param {String|undefined} body the body of the HTTP
 */
var apiRequest = function (type, path, callback, body) {
    var req = new XMLHttpRequest();
    req.open(type, path);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function (res) {
        var raw = JSON.parse(res.target.response);
        if (raw.status === "error") {
            alert(raw.error);
        }
        else {
            callback(raw.data);
        }
    }
    if (body) {
        req.send(body);
    } else {
        req.send();
    }
};