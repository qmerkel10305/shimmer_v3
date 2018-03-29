/**
 * Makes an API request
 *
 * @param {String} type HTTP method (GET, POST, PUT, etc)
 * @param {String} path the URI of the request
 * @param {function} callback callback when the request is completed
 * @param {String|undefined} body the body of the HTTP
 */
var apiRequest = function (type, path, callback, body) {
    var req = new XMLHttpRequest();
    req.open(type, path);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = callback
    if (body) {
        req.send(body);
    } else {
        req.send();
    }
};