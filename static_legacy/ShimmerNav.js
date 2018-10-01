/**
 * The navigation display
 */
function ShimmerNav (canvasId) {

    /** Array of dialog windows */
    var dialogs = [];

    /** Reference to the Shimmer object */
    var shimmer = new Shimmer(canvasId);

    /** Buttons that are a part of the navbar */
    var buttons = [
        function () { console.log("Not implemented"); },
        function () { shimmer.submitAndLoad("/next"); },
        function () { console.log("Not implemented"); },
        function () { console.log("Not implemented"); },
        function () { shimmer.getTargets().clearAll(); shimmer.update(); },
        function () { console.log("Not implemented"); },
        function () { console.log("Not implemented"); },
        function () { console.log("Not implemented"); },
        function () { console.log("Not implemented"); },
        function () { console.log("Not implemented"); },
        function () { if (dialogs.length > 0) dialogs[0].toggle(); },
        function () { if (dialogs.length > 1) dialogs[1].toggle(); },
        function () { if (dialogs.length > 2) dialogs[2].toggle(); },
        function () {
          for (var i = 0; i < dialogs.length; i++) {
            dialogs[i].hide();
          }
        }
    ];

    this.blockBrush = function () {
        return dialogs[0].selection;
    };

    this.init = function () {

        shimmer.init();

        dialogs[0] = new Dialog('help_dialog');
        dialogs[0].content = function(){};

        dialogs[1] = new Dialog('control_palette');
        dialogs[1].content = function(){};

        dialogs[2] = new Dialog('tool_palette');
        dialogs[2].content = function(){};


        if (document.body.clientHeight < 600 ||
                document.body.clientWidth < 800) {
            dialogs[3] = new Dialog('size_alert');
        }

        this.initAllDialogs();

        var menuItem;
        var i = 0;
        while ((menuItem = document.getElementById("button_" + i)) !== null) {
            if (i < buttons.length) menuItem.onclick = buttons[i];
            i++;
        }
    };

    this.initAllDialogs = function () {
        for (var i = 0; i < dialogs.length; i++) {
            dialogs[i].init();
            dialogs[i].show();
        }
    };
}
