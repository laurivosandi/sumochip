modes = {
    BLOCKLY:0,
    CODEMIRROR:1,
    MANUAL:2
};
direction = {
    FORWARD : 1,
    BACK : 2,
    RIGHT : 3,
    LEFT : 4,
    STOP : 0
};
position = {
    FRONT : 'front',
    LEFT : 'left',
    RIGHT : 'right'
}

init();

function init() {
    switchToBlockly();
    document.getElementById("content").style.display = "initial";
    document.getElementById("loading").style.display = "none";

    injectBlockly(); // Silveri kood mostly
    injectCodemirror();
    wsConnect();
    setOnClickFunctions();
};

function wsConnect() {
    var socketStatus = document.getElementById("socketStatus");
    socket = new WebSocket('ws:'+window.location.host);
    socket.onopen = function (event) {
	    console.log("connected");
        socketStatus.innerHTML = 'ühendatud';
	    console.log(event);
        socketStatus.className = 'connected';
        // start andurite näitude saatmist:
        socket.send('sensors');
    };
    socket.onerror = function (error) {
        console.log('WebSocket Error: ');
	    console.log(error);
        socketStatus.innerHTML = "ühendus robotiga puudub";
        socketStatus.className = 'disconnected';
    };
    socket.onclose = function (event) {
	    console.log(event);
        socketStatus.innerHTML = "ühendus puudub";
        socketStatus.className = 'disconnected';
    };  

    socket.onmessage = function(event){
        var msg = JSON.parse(event.data);
        console.log(msg);
        if (msg.savedCode) {   
            switchToCodemirror();
            codemirror.setValue(msg.savedCode);
            return;
        }
        // enemy sensors
        if (msg.enemy_right && msg.enemy_left) {
            document.getElementById('enemyFrontview').style.backgroundImage = "url('/static/img/redx.png')";
            document.getElementById('enemyRightview').style.backgroundImage = "none";
            document.getElementById('enemyLeftview').style.backgroundImage = "none";
        }
        else {
            document.getElementById('enemyFrontview').style.backgroundImage ="none";
            if (msg.enemy_right) {
                document.getElementById('enemyRightview').style.backgroundImage = "url('/static/img/redx.png')";
            }
            else {
                document.getElementById('enemyRightview').style.backgroundImage = "none";
            }
            if (msg.enemy_left) {
                document.getElementById('enemyLeftview').style.backgroundImage = "url('/static/img/redx.png')";
            }
            else {
                document.getElementById('enemyLeftview').style.backgroundImage = "none";
            }
        }
       
        // line sensors
        if (msg.line_left) {
                document.getElementById('lineSensor').style.borderLeft = '20px solid #eee';
        }
        else {
                document.getElementById('lineSensor').style.borderLeft = '20px solid #555';
        }
        if (msg.line_right) {
                document.getElementById('lineSensor').style.borderRight = '20px solid #eee';
        }
        else {
                document.getElementById('lineSensor').style.borderRight = '20px solid #555';
        }
        if (msg.line_front) {
                document.getElementById('lineSensor').style.borderTop = '20px solid #eee';
        }
        else {
                document.getElementById('lineSensor').style.borderTop = '20px solid #555';
        }        
        //battery info
        document.getElementById('charge').style.width = msg.capacity +'%';

    };   
};
//keylistenerid
window.onkeydown = function(e) {
    if (mode == modes.MANUAL) {
        var key = e.keyCode;
        if (key == 40)
            move(direction.BACK);
        else if (key == 38)
            move(direction.FORWARD);
        else if (key == 37)
            move(direction.LEFT);
        else if (key == 39)
            move(direction.RIGHT);   
    }   
};
window.onkeyup = function(e) {
    if (mode == modes.MANUAL)
        stop();
};
//prevent scrolling with keys
window.addEventListener("keydown", function(e) {
    // space and arrow keys
    if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
    }
}, false);

function isMobile() {
    if (navigator.userAgent.match(/Android/i)
            || navigator.userAgent.match(/iPhone/i)
            || navigator.userAgent.match(/iPad/i)
            || navigator.userAgent.match(/iPod/i)
            || navigator.userAgent.match(/BlackBerry/i)
            || navigator.userAgent.match(/Windows Phone/i)
            || navigator.userAgent.match(/Opera Mini/i)
            || navigator.userAgent.match(/IEMobile/i)
            ) {
        return true;
    }
}
var nothing = function() {};

// set onclickid ja ontouchid
function setOnClickFunctions() {
    if (!isMobile()) {
        var buttons = document.querySelectorAll ("controlButton");
        for (var i=0; i < buttons.length; i++) {
          buttons[i].ontouchend = nothing;
          buttons[i].ontouchstart = nothing;
        }
    }
    else {
        var buttons = document.querySelectorAll ("controlButton");
        for (var i=0; i < buttons.length; i++) {
          buttons[i].onmousedown = nothing;
          buttons[i].onmouseup = nothing;
        }
    }
};


// nuppude korral websocket message serverile
function move(command) {
    socket.send(command);
};
function stop(){
    move(direction.STOP);
};
function isLine(value){
    socket.send('isLine'+value);
};
function isEnemy(value){
    socket.send('isEnemy' + value)
};
function uploadCode() {
    if (mode == modes.BLOCKLY) {
            socket.send(Blockly.Python.workspaceToCode(workspace));    
    }
    if (mode == modes.CODEMIRROR) {
        socket.send(codemirror.getValue());
    }
};
function getSavedCode() {
    socket.send('getSavedCode');
};
function runCode() {
    document.getElementById('robotimg').src = '/static/img/robot-evil.png';
    socket.send('executeCode');
}
function stopCode() {
    document.getElementById('robotimg').src = '/static/img/robot.png';
    socket.send('stopCode');
}


function switchToBlockly() {
    document.getElementById("blockly").style.display = "initial";
    document.getElementById("codemirror").style.display = "none";
    document.getElementById("manual").style.display = "none";
    document.getElementById("program").style.display = "initial";
    mode = modes.BLOCKLY;

}
function switchToCodemirror() {
    document.getElementById("blockly").style.display = "none";
    document.getElementById("codemirror").style.display = "initial";
    document.getElementById("manual").style.display = "none";
    document.getElementById("program").style.display = "initial";

    var code = Blockly.Python.workspaceToCode(workspace);
    codemirror.setValue(code);
    codemirror.refresh();
    mode = modes.CODEMIRROR;

}

function toggleProgrammingStyle() {
    if (mode == modes.BLOCKLY) {
        switchToCodemirror();
    }
    else if (mode == modes.CODEMIRROR) {
        switchToBlockly();
    }
}

function switchToManual() {
    document.getElementById("program").style.display = "none";
    document.getElementById("blockly").style.display = "none";
    document.getElementById("codemirror").style.display = "none";
    document.getElementById("manual").style.display = "initial";
    mode = modes.MANUAL;
    stopCode();
}

function injectBlockly() {
    Blockly.HSV_SATURATION = 0.8;
    Blockly.HSV_VALUE = 0.80;

    /* MOVE */
    Blockly.Blocks.sumorobot_move = {
        init: function () {
            this.setColour(230);
            this.appendDummyInput()
				.appendField(new Blockly.FieldDropdown(this.VALUES), 'MOVE');
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setTooltip('move to chosen direction');

        }
    };
    Blockly.Blocks.sumorobot_move.VALUES =
		[[Blockly.Msg.CONTROLS_SUMOROBOT_FORWARD + ' \u2191', 'forward'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_BACKWARD + ' \u2193', 'back'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_RIGHT + ' \u21BB', 'right'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_LEFT + ' \u21BA', 'left'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_STOP, 'stop']];
    Blockly.JavaScript.sumorobot_move = function () {
        var value = this.getFieldValue('MOVE');
        return 'sumorobot.' + value + '();\n';
    };
    Blockly.Python.sumorobot_move = function () {
        var value = this.getFieldValue('MOVE');
        return 'sumorobot.' + value + '()\n';
    };


    /* DELAY */
    Blockly.Blocks.sumorobot_delay = {
        init: function () {
            this.setColour(58);
            this.appendDummyInput().appendField(Blockly.Msg.CONTROLS_SUMOROBOT_DELAY)
				.appendField(new Blockly.FieldTextInput('1', Blockly.FieldTextInput.numberValidator), 'DELAY');
            this.setPreviousStatement(true);
            this.setNextStatement(true);
            this.setTooltip('continue moving to chosen direction');
        }
    };
    Blockly.JavaScript.sumorobot_delay = function () {
        var value = this.getFieldValue('DELAY');
        return 'sumorobot.delay(' + value + ');\n';
    };
    Blockly.Python.sumorobot_delay = function () {
        var value = this.getFieldValue('DELAY');
        return 'sleep(' + value + ')\n';
    };

    /* ENEMY */
    Blockly.Blocks.sumorobot_enemy = {
        init: function () {
            this.setColour(0);
            this.appendDummyInput()
				.appendField(new Blockly.FieldDropdown(this.VALUES), 'ENEMY');
            this.setOutput(true, 'Boolean');
            this.setTooltip('detect enemy');
        }
    };
    Blockly.Blocks.sumorobot_enemy.VALUES =
		[[Blockly.Msg.CONTROLS_SUMOROBOT_ENEMY_LEFT, 'LEFT'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_ENEMY_RIGHT, 'RIGHT'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_ENEMY_FRONT, 'FRONT']];
    Blockly.JavaScript.sumorobot_enemy = function () {
        var value = this.getFieldValue('ENEMY');
        return ['sumorobot.isEnemy(' + value + ')', Blockly.JavaScript.ORDER_ATOMIC];
    };
    Blockly.Python.sumorobot_enemy = function () {
        var value = this.getFieldValue('ENEMY');
        return ['isEnemy("' + value + '")', Blockly.Python.ORDER_ATOMIC];
    };

    /* LINE */
    Blockly.Blocks.sumorobot_line = {
        init: function () {
            this.appendDummyInput()
				.appendField(new Blockly.FieldDropdown(this.VALUES), 'LINE');
            this.setOutput(true, 'Boolean');
            this.setTooltip('detect line');
        }
    };
    Blockly.Blocks.sumorobot_line.VALUES =
		[[Blockly.Msg.CONTROLS_SUMOROBOT_LINE_LEFT, 'LEFT'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_LINE_RIGHT, 'RIGHT'],
		[Blockly.Msg.CONTROLS_SUMOROBOT_LINE_FRONT, 'FRONT']];
    Blockly.JavaScript.sumorobot_line = function () {
        var value = this.getFieldValue('LINE');
        return ['sumorobot.isLine(' + value + ')', Blockly.JavaScript.ORDER_ATOMIC];
    };
    Blockly.Python.sumorobot_line = function () {
        var value = this.getFieldValue('LINE');
        return ['isLine("' + value + '")', Blockly.Python.ORDER_ATOMIC];
    };

    /* inject Blobkly */
    workspace = Blockly.inject(document.getElementById('blocklyArea'), {
        path: "/static/blockly/",
        trashcan: true,
        scrollbars: true,
        toolbox: '<xml id="toolbox" style="display: none;">' +
			'<block type="controls_if"></block>' +
			'<block type="sumorobot_move"><title name="MOVE">forward</title></block>' +
			'<block type="sumorobot_enemy"><title name="ENEMY">FRONT</title></block>' +
			'<block type="sumorobot_line"><title name="LINE">FRONT</title></block>' +
			'<block type="sumorobot_delay"></block></xml>'
    });
    
}

function injectCodemirror() {
    var codemirrrorDiv = document.getElementById("codemirrorDiv");
    codemirror = CodeMirror(codemirrrorDiv, {
        mode: "python",
        lineNumbers: true
    });
};
