
now_speed = { x: 0, y: 0 };
mouse_flag = true;

function init() {
    // easal stuff goes hur
    var xCenter = 150;
    var yCenter = 150;
    var stage = new createjs.Stage('joystick');

    var psp = new createjs.Shape();
    psp.graphics.beginFill('#333333').drawCircle(xCenter, yCenter, 50);

    psp.alpha = 0.25;

    var vertical = new createjs.Shape();
    var horizontal = new createjs.Shape();
    vertical.graphics.beginFill('#ff4d4d').drawRect(150, 0, 2, 300);
    horizontal.graphics.beginFill('#ff4d4d').drawRect(0, 150, 300, 2);

    stage.addChild(psp);
    stage.addChild(vertical);
    stage.addChild(horizontal);
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener('tick', stage);
    stage.update();

    var myElement = $('#joystick')[0];
    cont_size = window.innerWidth * 0.6;

    function size() {
        var w = window.innerWidth;
        cont_size = w * 0.6;
        $('#joystick').css({
            width: cont_size + 'px',
            height: cont_size + 'px'
        });
        $('.joystick-containers').css({
            width: cont_size - 12 + 'px',
        });
    }

    // create a simple instance
    // by default, it only adds horizontal recognizers
    var mc = new Hammer(myElement);

    mc.on("panstart", function (ev) {
        var pos = $('#joystick').position();
        xCenter = psp.x;
        yCenter = psp.y;
        psp.alpha = 0.5;

        stage.update();
    });

    // listen to events...
    mc.on("panmove", function (ev) {
        var pos = $('#joystick').position();

        var x = (ev.center.x - pos.left - window.cont_size / 2);
        var y = (ev.center.y - pos.top - window.cont_size / 2);
        // $('#xVal').text('X: ' + x);
        // $('#yVal').text('Y: ' + (-1 * y));

        var coords = calculateCoords(ev.angle, ev.distance);

        psp.x = coords.x;
        psp.y = coords.y;

        psp.alpha = 0.5;

        stage.update();
    });

    mc.on("panend", function (ev) {
        calculateCoords(0, 0);
        xCenter = 0;
        yCenter = 0;

        psp.alpha = 0.25;
        createjs.Tween.get(psp).to({ x: xCenter, y: yCenter }, 750, createjs.Ease.elasticOut);
    });

    window.addEventListener('resize', size);
    size();
}

function send_mouse(stick_pos) {
    // console.log(stick_pos);
    if (now_speed.x != 0 || now_speed.y != 0 && mouse_flag) {
        mouse_flag = false;
        $.ajax({
            url: '/api/mouse',
            type: 'POST',
            data: JSON.stringify(stick_pos),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            },
            always: function () {
                mouse_flag = true;
            }
        });
    }
    setTimeout(function () {
        send_mouse(now_speed);
    }, 30);
}


function calculateCoords(angle, distance) {
    var coords = {};
    distance = Math.min(distance, 100);
    var rads = (angle * Math.PI) / 180.0;

    coords.x = distance * Math.cos(rads);
    coords.y = distance * Math.sin(rads);
    // console.log(coords)
    now_speed = coords;

    return coords;
}

window.addEventListener('load', init);
window.addEventListener('load', () => {
    document.querySelector("#mouseleftbtn").addEventListener("mousedown", function () {
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "down", button: "left" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouseleftbtn").addEventListener("mouseup", function () {
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "up", button: "left" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouserightbtn").addEventListener("mousedown", function () {
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "down", button: "right" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouserightbtn").addEventListener("mouseup", function () {
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "up", button: "right" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouserightbtn").addEventListener("touchstart", function (ev) {
        ev.preventDefault();
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "down", button: "right" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouserightbtn").addEventListener("touchend", function (ev) {
        ev.preventDefault();
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "up", button: "right" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouseleftbtn").addEventListener("touchstart", function (ev) {
        ev.preventDefault();
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "down", button: "left" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })

    document.querySelector("#mouseleftbtn").addEventListener("touchend", function (ev) {
        ev.preventDefault();
        $.ajax({
            url: '/api/click',
            type: 'POST',
            data: JSON.stringify({ updown: "up", button: "left" }),
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                // console.log(data);
            }
        });
    })
});

send_mouse()
