
var canvas = document.getElementById('classify-canvas');
var ctx = canvas.getContext('2d');

var edit_canvas = document.createElement('canvas');
var edit_ctx = canvas.getContext('2d');

var submission;
var current;
var img = new Image();
img.src = "img.jpg";

function update () {
  edit_canvas.width = canvas.width = canvas.clientWidth;
  edit_canvas.height = canvas.height = canvas.clientHeight;
  ctx.drawImage(img, 0, 0, edit_canvas.width, edit_canvas.height);

  for (var i = 0; i < submission.targets.length; i++) {
    var t = submission.targets[i];
    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.fillRect(t.a.x * (canvas.width / img.width), t.a.y * (canvas.height / img.height),
      t.width * (canvas.width / img.width), t.height * (canvas.height / img.height));
  }

  if (current != undefined ) {
    ctx.fillStyle = 'rgba(127, 255, 127, 0.3)';
    ctx.fillRect(current.a.x * (canvas.width / img.width), current.a.y * (canvas.height / img.height),
      current.width * (canvas.width / img.width), current.height * (canvas.height / img.height));
  }
}

img.onload = function() {
    submission = {
      img: img.src,
      width: img.width,
      height: img.height,
      targets: []
    };
    update();
}

var main = function() {

      aniFrame = window.requestAnimationFrame  ||
          window.mozRequestAnimationFrame    ||
          window.webkitRequestAnimationFrame ||
          window.msRequestAnimationFrame     ||
          window.oRequestAnimationFrame;
          aniFrame(main, canvas);
};

canvas.onmousedown = function (event) {
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
    height: 0
  };
};

canvas.onmousemove = function (event) {
  if ( current != undefined ) {
    current.b.x = event.x * img.width / canvas.width;
    current.b.y = event.y * img.height / canvas.height;
    current.width = current.b.x - current.a.x;
    current.height = current.b.y - current.a.y;
  }
  update();
};

canvas.onmouseup = function (event) {
  if (Math.abs(current.width) > 10 && Math.abs(current.height) > 10)
    submission.targets.push(current);
  current = undefined;
  update();
};

document.getElementById('submit').onmouseup = function (event) {
  var tarpost = new XMLHttpRequest();   // new HttpRequest instance
  tarpost.open("POST", "/target");
  tarpost.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  tarpost.send(JSON.stringify(submission));
};
