/**
 * The root of the Shimmer app. Handles high level tasks
 *
 * @param {String} canvasId the id of the canvas
 */
function Shimmer (canvasId) {
  var current = {};
  var targets = {};

  /** actual display canvas */
  var canvas = document.getElementById(canvasId);
  var ctx = canvas.getContext('2d');
  /** buffer display */
  var edit_canvas = document.createElement('canvas');
  var edit_ctx =  edit_canvas.getContext('2d');

  this.update = function (event) {
    if (event != undefined ) {
      targets.setMouse(event, canvas);
    }

    var img = targets.getImage();
    var tar = targets.getTargets();

    edit_canvas.width = canvas.width = canvas.clientWidth;
    edit_canvas.height = canvas.height = canvas.clientHeight;
    ctx.drawImage(img, 0, 0, edit_canvas.width, edit_canvas.height);

    for (var i = 0; i < tar.length; i++) {
      var t = tar[i];

      // draw target bounding box
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.fillRect(t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height),
        t.width * (canvas.width / img.width), t.height * (canvas.height / img.height));

      // draw delete bubble
      ctx.fillStyle = 'rgba(255, 0, 0, 1.0)';
      ctx.beginPath();
      ctx.arc( t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height), 5, 0, 2 * Math.PI);
      ctx.fill();
    }

    var current = targets.getCurrent();
    if (current != undefined) {
      ctx.fillStyle = 'rgba(127, 255, 127, 0.3)';
      ctx.fillRect(current.a.x * (canvas.width / img.width), current.a.y * (canvas.height / img.height),
        current.width * (canvas.width / img.width), current.height * (canvas.height / img.height));
    }
  };

  this.submit = function () {
    console.log(targets.getImage());
      apiRequest("POST", "/target/" + targets.getId(), function(err, res) {
      }, JSON.stringify(
        { id: targets.getId(),
          targets: targets.getTargets(),
          image: targets.getImage().src
        }
      ));
    // request new image
  };

  /**
   * Submits an image and requests the next one with existing targets plotted
   */
  this.init = function() {
    var self = this;
    apiRequest("GET", "/next", function(res) {
      var raw = JSON.parse(res.target.response);

      var img = new Image();
      img.src = raw.image;

      img.onload = function() {
          targets = new TargetsHandler(raw.id, raw.targets, img);
          self.update();
      };
    });

  };

  canvas.onmousedown = this.update;
  canvas.onmousemove = this.update;
  canvas.onmouseup = this.update;
  window.addEventListener("resize", this.update);
  document.getElementById('submit-button').onmouseup = this.submit;
};