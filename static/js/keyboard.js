function getKey (e) {
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

function pressKey (char) {
    var key = document.querySelector('[data-char*="' + char.toUpperCase() + '"]');
    if (!key) {
        return console.warn('No key for', char);
    }
    console.log(key);
    key.setAttribute('data-pressed', 'on');
    setTimeout(function () {
        key.removeAttribute('data-pressed');
    }, 200);
}

function send_key(key, updown) {
    fetch('/api/keyboard', {
        method: 'POST',
        key: key,
        updown: updown
    }).then(function (res) {
        console.log(res);
    });
}

function size () {
    var keyboard = document.querySelector('.keyboard');
    var size = keyboard.parentNode.clientWidth / 90;
    keyboard.style.fontSize = size + 'px';
    console.log(size);
}

// var h1 = document.querySelector('h1');
// var originalQueue = h1.innerHTML;
// var queue = h1.innerHTML;

// function next () {
//     var c = queue[0];
//     queue = queue.slice(1);
//     h1.innerHTML = originalQueue.slice(0, originalQueue.length - queue.length);
//     pressKey(c);
//     if (queue.length) {
//         setTimeout(next, Math.random() * 200 + 50);
//     }
// }

// h1.innerHTML = "&nbsp;";
// setTimeout(next, 500);

window.addEventListener('load', function () {
    console.log("loaded")
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
            var key_char = e.target.getAttribute('data-char');
            console.log(key_char)
            if (key_char === null) {
                key_num = e.target.getAttribute('data-key');
                key_char = key_num.charCodeAt(0);
            }
            send_key(key_char, "down");
        });
        key.addEventListener('mouseup', function (e) {
            var key_char = e.target.getAttribute('data-char');
            if (key_char === null) {
                key_num = e.target.getAttribute('data-key');
                key_char = key_num.charCodeAt(0);
            }
            send_key(key_char, "up");
        });
    });
})