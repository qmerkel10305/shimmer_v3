/**
 * A single image from a flight
 *
 * @param {Object} response the server response for getting an image
 */
function EditTargetTool() {

  this.render = function (tar, graphics) {
    // draw
    var canvas = graphics.canvas;
    var ctx = graphics.ctx;
    var img = graphics.img;

    if (current != undefined) {
      ctx.fillStyle = 'rgba(127, 255, 127, 0.3)';
      ctx.fillRect(current.a.x * (canvas.width / img.width), current.a.y * (canvas.height / img.height),
      current.width * (canvas.width / img.width), current.height * (canvas.height / img.height));
    }
  }

  this.getCurrent = function () {
    return current;
  };

  this.onmouseup = function(event, tar, graphics) {
    // TODO open
  }

  this.onmousedown = function(event, tar, graphics) {
    // TODO if over a target
  }

  this.onmousemove = function(event, tar, graphics) {
    // TODO determine if mouse is over a target

    var canvas = graphics.canvas;
    var img = graphics.img;
    if (current == undefined || !tar.isReady()) {
      return;
    }
    current.b.x = event.x * img.width / canvas.width;
    current.b.y = event.y * img.height / canvas.height;
    current.width = current.b.x - current.a.x;
    current.height = current.b.y - current.a.y;
  }
}
