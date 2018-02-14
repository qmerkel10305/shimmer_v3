/**
 * A single image from a flight
 *
 * @param {Object} response the server response for getting an image
 */
var TargetsHandler  = function (id, targets, response) {

  // no backend for this yet rofl
  var id = id;
  var img = response;
  var targets = targets;

  this.getId = function () { return id; };
  this.getImage = function () { return img; };
  this.getTargets = function () { return targets; };
  var shapeSelector = new Dialog('classify_target');
  shapeSelector.hide();
  shapeSelector.canvas = document.getElementById('classify-canvas');
  shapeSelector.preview = document.getElementById('preview-canvas');
  shapeSelector.ctx = shapeSelector.canvas.getContext('2d');
  shapeSelector.pctx = shapeSelector.preview.getContext('2d');
  shapeSelector.form = document.getElementById('class_form');

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

  /**
   *
   * Functions for target creation / editing
   *
   */
  var newTargetBuffer;
  this.addTarget = function (target, graphics) {
    shapeSelector.show();
    shapeSelector.ctx.drawImage(graphics.img,
      target.a.x, target.a.y, target.width, target.height,
      0, 0, shapeSelector.canvas.width, shapeSelector.canvas.height);

    newTargetBuffer = target;
    targets.push(newTargetBuffer);
  }

  this.cancelTarget = function (event) {
    shapeSelector.hide();
    newTargetBuffer = undefined;
  };

  this.drawPreview = function (event) {
    newTargetBuffer.shape =              shapeSelector.form.children[1].value;
    newTargetBuffer.orientation =        shapeSelector.form.children[3].value;
    newTargetBuffer.shape_color =        shapeSelector.form.children[5].value;
    newTargetBuffer.alphanumeric =       shapeSelector.form.children[7].value;
    newTargetBuffer.alphanumeric_color = shapeSelector.form.children[9].value;

    var canvas = shapeSelector.preview;
    shapeSelector.pctx.clearRect(0, 0, canvas.width, canvas.height);
    shapeSelector.pctx.fillStyle = "#556B2F";
    shapeSelector.pctx.fillRect(0, 0, canvas.width, canvas.height);
    shapeSelector.pctx.fillStyle = newTargetBuffer.shape_color || "#000000";
    // circle, semicircle, quarter_ circle, triangle, square,
    // rectangle, trapezoid, pentagon, hexagon, octagon, star, cross
    switch (newTargetBuffer.shape) {
      case "circle":
        break;
      case "semicircle":
        break;
      case "quarter_circle":
        break;
      case "square":
        shapeSelector.pctx.fillRect(80, 40, 150, 75);
        break;
      case "rectangle":
        shapeSelector.pctx.fillRect(20, 20, 150, 100);
        break;
      case "trapezoid":
        break;
      case "pentagon":
        break;
      case "hexagon":
        break;
      case "octagon":
        break;
      case "star":
        break;
      case "cross":
        console.log();
        shapeSelector.pctx.fillRect(110, 20, 80, 120);
        shapeSelector.pctx.fillRect(40, 57, 220, 40);
        break;
    }
    shapeSelector.pctx.fillStyle = newTargetBuffer.alphanumeric_color || "#000000";
    shapeSelector.pctx.font="60px monospace";
    shapeSelector.pctx.fillText(newTargetBuffer.alphanumeric, 130, 95);
  }

  this.finishTarget = function (event) {
    newTargetBuffer.shape =              shapeSelector.form.children[1].value;
    newTargetBuffer.shape_color =        shapeSelector.form.children[3].value;
    newTargetBuffer.alphanumeric =       shapeSelector.form.children[5].value;
    newTargetBuffer.alphanumeric_color = shapeSelector.form.children[7].value;
    newTargetBuffer.orientation =        shapeSelector.form.children[9].value;
    // TODO reset ^^^^
    shapeSelector.hide();
    newTargetBuffer = undefined;
    current = undefined;
  }

  /**
   *
   *  Target util functions
   *
   */
  this.clearAll = function () {
    targets = [];
    current = undefined;
  };

  this.isReady = function () {
    return newTargetBuffer == undefined;
  }

  document.getElementById('cancel-target-button').onmouseup = this.cancelTarget;
  var shapeButtons = document.getElementsByClassName('shape-button');
  for (var i = 0; i < shapeButtons.length; i++) {
      shapeButtons[i].onmouseup = this.finishTarget;
  }

  var attrButtons = document.getElementsByClassName('attr-button');
  for (var i = 0; i < attrButtons.length; i++) {
      attrButtons[i].onchange = this.drawPreview;
  }

};
