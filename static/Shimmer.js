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
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.fillRect(t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height),
        t.width * (canvas.width / img.width), t.height * (canvas.height / img.height));
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
      apiRequest("POST", "/target/" + targets.img, function(err, res) {
      }, JSON.stringify(targets.getTargets()));
      
    // request new image
  };

  /**
   * Submits an image and requests the next one with existing targets plotted
   */
  this.init = function() {
    var img = new Image();
    img.src = "img.jpg";

    var self = this;
    img.onload = function() {
        targets = new TargetsHandler(0, img);
        self.update();
    };
  };

  canvas.onmousedown = this.update;
  canvas.onmousemove = this.update;
  canvas.onmouseup = this.update;
  document.getElementById('submit').onmouseup = this.submit;
};
