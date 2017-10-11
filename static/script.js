
var canvas = document.getElementById('classify-canvas');
var ctx = canvas.getContext('2d');

var edit_canvas = document.createElement('canvas');
var edit_ctx = canvas.getContext('2d');

var submission;
var img = new Image();
img.src = "img.jpg";

img.onload = function() {
    submission = {
      img: img.src,
      width: img.width,
      height: img.height,
      targets: []
    };
    edit_canvas.width = canvas.width = window.innerWidth;
    edit_canvas.height = canvas.height = window.innerHeight;
    ctx.drawImage(img, 0, 0, edit_canvas.width, edit_canvas.height);
}

var main = function() {
  update();
      aniFrame = window.requestAnimationFrame  ||
          window.mozRequestAnimationFrame    ||
          window.webkitRequestAnimationFrame ||
          window.msRequestAnimationFrame     ||
          window.oRequestAnimationFrame;
          aniFrame(main, canvas);
};

var ix, iy;
var cur;
canvas.onmousedown = function (event) {
  cur = document.createElement("div");
  cur.classList.add("box");
  ix = event.x;
  iy = event.y;
  cur.style.left =  ix + "px";
  cur.style.top = iy + "px";
  document.body.appendChild(cur);
};

canvas.onmousemove = function (event) {
  if ( cur != undefined ) {
    cur.style.width = event.x - ix + "px";
    cur.style.height = event.y - iy + "px";
  }
};

canvas.onmouseup = function (event) {
  cur = undefined;

  var target = {
    topLeft: {
      x: ix * img.width / window.innerWidth,
      y: iy * img.width / window.innerHeight
    },
    bottomRight: {
      x: event.x * img.width / window.innerWidth,
      y: event.y * img.width / window.innerHeight
    },
    width: (event.x - ix) * (img.width / window.innerWidth),
    height: (event.y - iy) * (img.width / window.innerHeight)
  };

  if (Math.abs(target.width) > 10 && Math.abs(target.height) > 10)
    submission.targets.push(target);
};

document.getElementById('submit').onmouseup = function (event) {
  var tarpost = new XMLHttpRequest();   // new HttpRequest instance
  tarpost.open("POST", "/target");
  tarpost.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  tarpost.send(JSON.stringify(submission));
};
