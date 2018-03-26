/**
 * A single image from a flight
 *
 * @param {Object} response the server response for getting an image
 */
function MouseHandler() {
  /** box being drag selected by the mouse */
  var current = undefined;
  /** target the mouse is over */
  var over = undefined;

  /**
   * Renders the green box to select
   */
  this.render = function (tar, graphics) {
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

  /**
   * on Mouse up
   */
  this.onmouseup = function(event, tar, graphics) {
    var canvas = graphics.canvas;
    var img = graphics.img;
    if (Math.abs(current.width) < 10 && Math.abs(current.height) < 10) {
      if (over != undefined) {
          tar.editTarget(over, graphics);
          current = over = undefined;
      }
      current = over = undefined;
      return; // too small
    }

    // normalize points
    if (current.a.x > current.b.x) {
      var temp = current.a.x;
      current.a.x = current.b.x;
      current.b.x = temp;
    }

    if (current.a.y > current.b.y) {
      var temp = current.a.y;
      current.a.y = current.b.y;
      current.b.y = temp;
    }

    current.width = Math.abs(current.b.x - current.a.x);
    current.height =  Math.abs(current.b.y - current.a.y);

    tar.editTarget(current, graphics);
    current = over = undefined;
  }

  /**
   * On mouse down on the canvas
   */
  this.onmousedown = function(event, tar, graphics) {
    var canvas = graphics.canvas;
    var img = graphics.img;
    current = {
      a: {
        x: event.x * img.width / canvas.width,
        y: event.y * img.height / canvas.height
      },
      b: {
        x: event.x * img.width / canvas.width,
        y: event.y * img.height / canvas.height
      },
      width: 0,
      height: 0,
      shape: null,
      orientation: null,
      shape_color: null,
      alphanumeric: null,
      alphanumeric_color: null
    };
  }

  /**
   * Mouse move on campus
   */
  this.onmousemove = function(event, tar, graphics) {
    var canvas = graphics.canvas;
    var img = graphics.img;

    // scaled x and y
    var s = { x: event.x * img.width  / canvas.width,
              y: event.y * img.height / canvas.height };

    // check if we over a target
    over = undefined;
    var n = tar.getTargets();
    for (var i = 0; i < n.length; i++) {
      if (n[i].a.x <= s.x && n[i].a.y <= s.y &&
          n[i].b.x >= s.x && n[i].b.y >= s.y) {
            over = n[i];
      }
    }

    if (current == undefined || !tar.isReady()) {
      return;
    }
    current.b = s;
    current.width = current.b.x - current.a.x;
    current.height = current.b.y - current.a.y;

  }
}
