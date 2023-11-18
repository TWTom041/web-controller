key_req_array = [];

function getKey(e) {
    var location = e.location;
    var selector;
    if (location === KeyboardEvent.DOM_KEY_LOCATION_RIGHT) {
        selector = ['[data-key="' + e.keyCode + '-R"]']
    } else {
        var code = e.keyCode || e.which;
        selector = [
            '[data-key="' + code + '"]',
            '[data-char*="' + encodeURIComponent(String.fromCharCode(code)) + '"]'
        ].join(',');
    }
    return document.querySelector(selector);
}

function pressKey(char) {
    var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
    if (!key) {
        return console.warn('No key for', char);
    }
    // console.log(key);
    key.setAttribute('data-pressed', 'on');
    setTimeout(function () {
        key.removeAttribute('data-pressed');
    }, 200);
}

function send_key_request() {
    if (key_req_array.length==0) {
        setTimeout(send_key_request, 20);
        return;
    }
    var to_be_sent = key_req_array.shift();
    $.ajax({
        url: '/api/keyboard',
        type: 'POST',
        data: JSON.stringify({
            "key": to_be_sent[0],
            "updown": to_be_sent[1],
        }),
        contentType: "application/json",
        dataType: 'json',
        success: function (data) {
            // console.log(data);
            return send_key_request();
        }
    });
}

function send_key(key, updown) {
    // console.log(key, updown);
    key_req_array.push([key, updown]);
}

function size() {
    var keyboard = document.querySelector('.keyboard');
    var size = keyboard.parentNode.clientWidth / 90;
    keyboard.style.fontSize = size + 'px';
    // console.log(size);
}

send_key_request()

window.addEventListener('load', function () {
    document.body.addEventListener('keydown', function (e) {
        var key = getKey(e);
        if (!key) {
            return console.warn('No key for', e.keyCode);
        }

        key.setAttribute('data-pressed', 'on');
    });

    document.body.addEventListener('keyup', function (e) {
        var key = getKey(e);
        key && key.removeAttribute('data-pressed');
    });



    window.addEventListener('resize', function (e) {
        size();
    });
    size();

    var key_elements = document.querySelectorAll('.key');
    key_elements.forEach(function (key) {
        key.addEventListener('mousedown', function (e) {
            var key_char = key.getAttribute('data-char');
            if (key_char === null) {
                key_num = key.getAttribute('data-key');
                key_char = key_num.charCodeAt(0);
            }
            send_key(key_char, "down");
        });
        key.addEventListener('mouseup', function (e) {
            var key_char = key.getAttribute('data-char');
            if (key_char === null) {
                key_num = key.getAttribute('data-key');
                key_char = key_num.charCodeAt(0);
            }
            send_key(key_char, "up");
        });
    });
})