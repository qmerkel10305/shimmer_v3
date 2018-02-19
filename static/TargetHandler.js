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
  shapeSelector.ctx = shapeSelector.canvas.getContext('2d');
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
      0, 0, shapeSelector.canvas.width, shapeSelector.canvas.height/2);

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

    var canvas = shapeSelector.canvas;
    shapeSelector.ctx.save();
    shapeSelector.ctx.clearRect(0, canvas.height/2, canvas.width, canvas.height/2);
    shapeSelector.ctx.fillStyle = newTargetBuffer.shape_color || "#000000";
    var charOffset = { x: 0, y: 0 };
    switch (newTargetBuffer.shape) {
      case "circle":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.arc(100, 300, 65, 0, 2 * Math.PI);
        shapeSelector.ctx.fill();
        break;
      case "semicircle":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.arc(100, 260, 80, 0, Math.PI);
        shapeSelector.ctx.fill();
        break;
      case "quarter_circle":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.arc(40, 240, 120, 0, Math.PI / 2);
        shapeSelector.ctx.lineTo(40, 240);
        shapeSelector.ctx.fill();
        charOffset = { x: -10, y: -10 };
        break;
      case "square":
        shapeSelector.ctx.fillRect(50, 250, 100, 100);
        break;
      case "rectangle":
        shapeSelector.ctx.fillRect(30, 260, 140, 80);
        break;
      case "trapezoid":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo( 60, 260);
        shapeSelector.ctx.lineTo( 20, 340);
        shapeSelector.ctx.lineTo(180, 340);
        shapeSelector.ctx.lineTo(140, 260);
        shapeSelector.ctx.fill();
        break;
      case "triangle":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo(100, 240);
        shapeSelector.ctx.lineTo(170, 360);
        shapeSelector.ctx.lineTo( 30, 360);
        shapeSelector.ctx.fill();
        charOffset = { x: 0, y: 10 };
        break;
      case "pentagon":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo(100, 230);
        shapeSelector.ctx.lineTo( 32, 287);
        shapeSelector.ctx.lineTo( 60, 360);
        shapeSelector.ctx.lineTo(140, 360);
        shapeSelector.ctx.lineTo(168, 287);
        shapeSelector.ctx.fill();
        break;
      case "hexagon":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo( 60, 230);
        shapeSelector.ctx.lineTo(140, 230);
        shapeSelector.ctx.lineTo(175, 300);
        shapeSelector.ctx.lineTo(140, 370);
        shapeSelector.ctx.lineTo( 60, 370);
        shapeSelector.ctx.lineTo( 25, 300);
        shapeSelector.ctx.fill();
        break;
      case "octagon":
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo( 70, 225);
        shapeSelector.ctx.lineTo(130, 225);
        shapeSelector.ctx.lineTo(175, 275);
        shapeSelector.ctx.lineTo(175, 325);
        shapeSelector.ctx.lineTo(125, 375);
        shapeSelector.ctx.lineTo( 75, 375);
        shapeSelector.ctx.lineTo( 25, 325);
        shapeSelector.ctx.lineTo( 25, 275);
        shapeSelector.ctx.fill();
        break;
      case "star":
        /* TODO: make me pretty :( */
        shapeSelector.ctx.beginPath();
        shapeSelector.ctx.moveTo(100, 225);
        shapeSelector.ctx.lineTo(125, 260);
        shapeSelector.ctx.lineTo(175, 260);
        shapeSelector.ctx.lineTo(150, 300);
        shapeSelector.ctx.lineTo(165, 350);
        shapeSelector.ctx.lineTo(100, 330);
        shapeSelector.ctx.lineTo( 35, 350);
        shapeSelector.ctx.lineTo( 50, 300);
        shapeSelector.ctx.lineTo( 25, 260);
        shapeSelector.ctx.lineTo( 75, 260);
        shapeSelector.ctx.fill();
        break;
      case "cross":
        shapeSelector.ctx.fillRect(80, 240, 40, 120);
        shapeSelector.ctx.fillRect(40, 280, 120, 40);
        break;
    }
    shapeSelector.ctx.fillStyle = newTargetBuffer.alphanumeric_color || "#000000";
    shapeSelector.ctx.font="60px monospace";
    shapeSelector.ctx.fillText(newTargetBuffer.alphanumeric,
      80 + charOffset.x, 320 + charOffset.y);
    shapeSelector.ctx.restore();
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
