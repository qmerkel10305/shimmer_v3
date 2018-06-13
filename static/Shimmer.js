/**
 * The root of the Shimmer app. Handles high level tasks
 *
 * @param {String} canvasId the id of the canvas
 */
function Shimmer (canvasId) {
  var current = {};
  var targets = {};

  /** send captured mouse data to */
  var tool = new MouseHandler();

  /** actual display canvas */
  var canvas = document.getElementById(canvasId);
  var ctx = canvas.getContext('2d');
  /** buffer display */
  var edit_canvas = document.createElement('canvas');
  var edit_ctx =  edit_canvas.getContext('2d');

  this.update = function (event) {
    var img = targets.getImage();
    var tar = targets.getTargets();
    var graphics = {
      canvas: canvas,
      ctx: ctx,
      img: img
    };

    if (event != undefined && event) {
      tool['on' + event.type](event, targets, graphics);
    }

    edit_canvas.width = canvas.width = canvas.clientWidth;
    edit_canvas.height = canvas.height = canvas.clientHeight;
    ctx.drawImage(img, 0, 0, edit_canvas.width, edit_canvas.height);

    for (var i = 0; i < tar.length; i++) {
      var t = tar[i];
      if (t.a === undefined )
        break;
      // draw target bounding box
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.fillRect(t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height),
        t.width * (canvas.width / img.width), t.height * (canvas.height / img.height));
    }

    tool.render(targets, graphics);
  };

  this.submitAndLoad = function (str) {
    var data = {
      id: targets.getId(),
      targets: targets.getTargets(),
      image: targets.getImage().src
    };
    console.log(data);
    var self = this;
    apiRequest("POST", "/target/" + targets.getId(), function(raw) {
      // Only load the next image if the submission is successful
      self.loadImage(str);
    }, JSON.stringify(data));
  };

  /**
   * Requests a image one with existing targets plotted
   */
  this.loadImage = function(str) {
    var self = this;
    apiRequest("GET", str, function(raw) {
      var img = new Image();
      img.src = raw.image;

      document.getElementById("img_info").innerHTML = "Flight " + raw.flight + " | Image " + raw.id;

      img.onload = function() {
          targets = new TargetsHandler(raw.id, raw.targets, img);
          self.update();
      };
    });

  };

  /**
   * Loads a target and an image into Shimmer
   */
  this.init = function () {
    this.loadImage("/next");
  }

  this.getTargets = function () {
    return targets;
  }

  var self = this;
  canvas.onmousedown = this.update;
  canvas.onmousemove = this.update;
  canvas.onmouseup = this.update;
  window.addEventListener("resize", this.update);
  window.addEventListener("keydown", function (e) {
    if (e.keyCode == 13) {
      self.submitAndLoad("/next");
    } else if (e.keyCode == 37) {
      var x = targets.getId() - 1;
      if(x < 0) {
        return;
      }
      self.submitAndLoad("/image/" + x);
    } else if (e.keyCode == 39) {
      var x = targets.getId() + 1;
      if(x < 0) {
        return;
      }
      self.submitAndLoad("/image/" + x);
    } else if (e.keyCode == 38) {
      var img_id = parseInt(prompt("Image id number?", "0"));
      self.submitAndLoad("/image/" + img_id);
    }
  });
};
