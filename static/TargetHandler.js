/**
 * A single image from a flight
 *
 * @param {Object} response the server response for getting an image
 */
var TargetsHandler  = function (id, response) {
  // no backend for this yet rofl
  var id = id;
  var img = response;
  var targets = [];
  var current = undefined;

  this.getId = function () { return id; };
  this.getImage = function () { return img; };
  this.getTargets = function () { return targets; };
  this.getCurrent = function () { return current; };

  /**
   * State of the frontend. Just .
   */
  this.getSubmission = function () {
    return {
      img: img.src,
      width: img.width,
      height: img.height,
      targets: targets
    };
  };

  this.makeTarget = function (event, canvas) {
    return {
      a: {
        x: event.x * img.width / canvas.width,
        y: event.y * img.height / canvas.height
      },
      b: {
        x: event.x * img.width / canvas.width,
        y: event.y * img.height / canvas.height
      },
      width: 0,
      height: 0
    };
  };

  this.setMouse = function(event, canvas) {
    if (event.type == "mousemove") {
      if (current == undefined) {
        return;
      }
      current.b.x = event.x * img.width / canvas.width;
      current.b.y = event.y * img.height / canvas.height;
      current.width = current.b.x - current.a.x;
      current.height = current.b.y - current.a.y;
    } else if (event.type == "mousedown") {
      current = this.makeTarget(event, canvas);
    } else if (event.type == "mouseup") {
      if (Math.abs(current.width) > 10 && Math.abs(current.height) > 10)
        targets.push(current);
      current = undefined;
    }
  };
};
