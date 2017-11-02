/**
 * A single image from a flight
 *
 * @param {Object} reponse the server response for getting an image
 */
var TargetsHandler  = function (reponse) {
  // no backend for this yet rofl
  var img = reponse;
  var targets = [];

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

  this.makeTarget = function () {
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

  this.setMouse = function(event) {
    if ( current != undefined ) {
      current.b.x = event.x * img.width / canvas.width;
      current.b.y = event.y * img.height / canvas.height;
      current.width = current.b.x - current.a.x;
      current.height = current.b.y - current.a.y;
    } else {
    }
    update();
  };

  this.createTarget = function (event) {
    if (Math.abs(current.width) > 10 && Math.abs(current.height) > 10)
      submission.targets.push(current);
    current = undefined;
    update();
  };

  this.submit = function (event) {
    var tarpost = new XMLHttpRequest();   // new HttpRequest instance
    tarpost.open("POST", "/target");
    tarpost.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    tarpost.onload = function (req, res) {
      console.log(req);
      console.log(res);
    };

    tarpost.send(JSON.stringify(submission));
  };
};
