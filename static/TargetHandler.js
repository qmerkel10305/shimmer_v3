/**
 * A single image from a flight
 *
 * @param {Object} response the server response for getting an image
 */
var TargetsHandler  = function (id, targets, response) {
  var self = this;

  // no backend for this yet rofl
  var id = id;
  var img = response;
  var targets = targets;
  var editTargetBuffer;

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
   * Functions for target creation / editing
   */
  this.editTarget = function (target, graphics) {
    shapeSelector.show();
    shapeSelector.ctx.drawImage(graphics.img,
      target.a.x, target.a.y, target.width, target.height,
      0, 0, shapeSelector.canvas.width, shapeSelector.canvas.height/2);

    editTargetBuffer = target;
    // check if target is new
    if (target.shape == null) {
      targets.push(editTargetBuffer);
    }
    shapeSelector.form.children[ 5].value = editTargetBuffer.shape || 'square';
    shapeSelector.form.children[ 7].value = editTargetBuffer.orientation || 'N';
    shapeSelector.form.children[ 9].value = editTargetBuffer.shape_color || 'black';
    shapeSelector.form.children[11].value = editTargetBuffer.alphanumeric || 'A';
    shapeSelector.form.children[13].value = editTargetBuffer.alphanumeric_color || 'white';
    self.drawPreview()
  }

  this.drawPreview = function (event) {
    editTargetBuffer.shape =              shapeSelector.form.children[ 5].value;
    editTargetBuffer.orientation =        shapeSelector.form.children[ 7].value;
    editTargetBuffer.shape_color =        shapeSelector.form.children[ 9].value;
    editTargetBuffer.alphanumeric =       shapeSelector.form.children[11].value;
    editTargetBuffer.alphanumeric_color = shapeSelector.form.children[13].value;

    var canvas = shapeSelector.canvas;
    shapeSelector.ctx.save();
    shapeSelector.ctx.clearRect(0, canvas.height/2, canvas.width, canvas.height/2);
    shapeSelector.ctx.fillStyle = editTargetBuffer.shape_color || "#000000";
    var charOffset = { x: 0, y: 0 };
    switch (editTargetBuffer.shape) {
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
    shapeSelector.ctx.fillStyle = editTargetBuffer.alphanumeric_color || "#000000";
    shapeSelector.ctx.font="60px monospace";
    shapeSelector.ctx.fillText(editTargetBuffer.alphanumeric,
      80 + charOffset.x, 320 + charOffset.y);
    shapeSelector.ctx.restore();
  }
  var attrButtons = document.getElementsByClassName('attr-button');
  for (var i = 0; i < attrButtons.length; i++) {
    attrButtons[i].onchange = this.drawPreview;
  }

  /**
   * When the user "Update" button
   */
  this.updateTarget = function (event) {
    editTargetBuffer.shape =              shapeSelector.form.children[ 5].value;
    editTargetBuffer.orientation =        shapeSelector.form.children[ 7].value;
    editTargetBuffer.shape_color =        shapeSelector.form.children[ 9].value;
    editTargetBuffer.alphanumeric =       shapeSelector.form.children[11].value;
    editTargetBuffer.alphanumeric_color = shapeSelector.form.children[13].value;
    self.closeEditor();
  }
  document.getElementById('update-target-button').onmouseup = this.updateTarget;

  /**
   * Removes the current target from the list
   */
  this.removeTarget = function (event) {
    if (editTargetBuffer.target_id != undefined) {
      apiRequest("DELETE", "/target/" + editTargetBuffer.target_id, function(err, res) {
        console.log("Database remove target... success");
      });
    }
    targets.splice(targets.indexOf(editTargetBuffer), 1);
    self.closeEditor();
  }
  document.getElementById('discard-target-button').onmouseup = this.removeTarget;

  this.closeEditor = function (event) {
    shapeSelector.hide();
    editTargetBuffer = undefined;
  };

  /**
   *  Target util functions
   */
  this.clearAll = function () {
    targets = [];
    editTargetBuffer = undefined;
  };

  this.isReady = function () {
    return editTargetBuffer == undefined;
  }
};
