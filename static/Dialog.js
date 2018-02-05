/**
 * Impementation of a window. Can be minimized, closed, dragged and opened from
 * the navbar.
 * @param {String} html_id Id of the dialog element
 */
function Dialog (html_id) {

    /** The HTML element */
    this.dialogElement = document.getElementById(html_id);
    this.dragbarElement = this.dialogElement.children[0];
    this.closeButtonElement = this.dragbarElement.children[0];
    var vis = true;

    /** The bottom part  */
    this.content = function(){};

    /** Array of buttons from the dialog */
    this.buttons = [];

    /** The index of the button that is currently selected */
    this.selection = 0;

    /**
     * Initializes the dialong content
     * @param {Universe} world The entire universe
     * @param {RenderingContext2D} graphics The canvas graphics
     */
    this.init = function (world, graphics) {
        this.content(world, graphics);
    };

    this.dialogElement.shimmerDragClick = { x: 0, y: 0, dragging: false };

    /**
     * Sets the mouse events for the dialog
     */
    this.setMouseEvents = function () {

        var de = this.dialogElement;

        this.dragbarElement.onmousedown = function (event) {
            de.shimmerDragClick.x = event.offsetX;
            de.shimmerDragClick.y = event.offsetY;
            de.shimmerDragClick.dragging = true;
            de.style.zindex = 3;

            window.onmousemove = function (event) {
                if(de.shimmerDragClick.dragging){
                    de.style.left = event.clientX - de.shimmerDragClick.x + "px";
                    de.style.top = event.clientY - de.shimmerDragClick.y + "px";
                }
            };
        };

        this.dragbarElement.onmouseup = function (event) {
            de.shimmerDragClick.dragging = false;
            de.style.zindex = 1;
        };

        this.closeButtonElement.onclick = function (event) {
            de.style.display = "none";
        };

    };
    this.setMouseEvents();

    /** Minimize and maximize to be implemented */
    this.minimize = function () {};
    this.maximize = function () {};

    /**
     * Shows the dialog via style
     */
    this.show = function () {
        this.dialogElement.style.display = "block";
        vis = true;
    };

    /**
     * Hides the dialog via style
     */
    this.hide = function () {
        this.dialogElement.style.display = "none";
        vis = false;
    };

    this.visible = function () {
        return vis;
    };

    /**
     * Toggles to dialogs visability
     */
    this.toggle = function () {
      if (vis) {
        this.hide();
      } else {
        this.show();
      }
    };
}
