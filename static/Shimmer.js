/**
 * The root of the Shimmer app. Handles high level tasks
 *
 * @param {String} canvasId the id of the canvas
 */
function Shimmer (canvasId) {
  this.targets = new TargetsHandler();

  /** actual display canvas */
  var canvas = document.getElementById(canvasId);
  var context = canvas.getContext('2d');
  /** buffer display */
  var edit_canvas = document.createElement('canvas');
  var edit_context =  edit_canvas.getContext('2d');

  this.update = function () {
    var img = targets.img;
    var tar = targets.targets;

    edit_canvas.width = canvas.width = canvas.clientWidth;
    edit_canvas.height = canvas.height = canvas.clientHeight;
    ctx.drawImage(img, 0, 0, edit_canvas.width, edit_canvas.height);

    for (var i = 0; i < tar.length; i++) {
      var t = tar[i];
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.fillRect(t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height),
        t.width * (canvas.width / img.width), t.height * (canvas.height / img.height));
    }

    if (current != undefined ) {
      ctx.fillStyle = 'rgba(127, 255, 127, 0.3)';
      ctx.fillRect(current.a.x * (canvas.width / img.width), current.a.y * (canvas.height / img.height),
        current.width * (canvas.width / img.width), current.height * (canvas.height / img.height));
    }
  };

  this.submit = function () {
      apiRequest("POST", "/target", function() {});
  };

  this.createTarget = function (event) {
    if (Math.abs(current.width) > 10 && Math.abs(current.height) > 10)
      submission.targets.push(current);
    current = undefined;
    update();
  };

  /**
   * Submits an image and requests the next one with existing targets plotted
   */
  this.init = function() {
    var img = new Image();
    img.src = "img.jpg";

    img.onload = function() {
        tar = new TargetHandler(img);
        update();
    };
  };

  canvas.onmousedown = this.update;
  canvas.onmousemove = this.submit;
  canvas.onmouseup = this.createTarget;
  document.getElementById('submit').onmouseup = this.submit;
};
