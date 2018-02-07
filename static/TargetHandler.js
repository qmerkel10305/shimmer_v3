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

  this.finishTarget = function (event) {
    // TODO set character
    newTargetBuffer.shape = event.target.innerText;
    shapeSelector.hide();
    newTargetBuffer = undefined;
    current = undefined;
  }

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

};
