var token = ""
var cursor_x_pos = 0
var min_x_pos = 0
var console_blocked = false
var cur_req = null
var cur_cmd = ""
var cur_timer = null
var pool_cnt = 0
var autocomplete_words = []
var cmd_history = []
var cmd_history_pos = -1
var cmd_history_unfinished = ""

function console_print(text) {
    var lines = text.split("\n")
    var cursor_el = document.getElementById("cursor")

    for (var i = 0; i < lines.length - 1; i += 1) {
        var el = document.createElement('span')
        el.innerText = lines[i] + "\n"

        cursor_el.insertAdjacentElement("beforebegin", el)
        cursor_x_pos = 0
    }

    var last_line = lines[lines.length-1]
    for (var i = 0; i < last_line.length; i += 1) {
        var el = document.createElement('span')
        el.innerText = last_line[i]
        cursor_el.insertAdjacentElement("beforebegin", el)
        cursor_x_pos += 1
    }
//    window.scrollTo(0,document.body.scrollHeight);
}

function cursor_left() {
    if (cursor_x_pos <= min_x_pos) {
        return false
    }
    var cursor_el = document.getElementById("cursor")
    prev_el = cursor_el.previousSibling

    if (!prev_el || prev_el.tagName != "SPAN" || prev_el.innerText == "\n") {
        return false
    }

    cursor_el.removeAttribute("id")
    prev_el.setAttribute("id", "cursor")

    cursor_x_pos -= 1
    return true
}

function cursor_right() {
    var cursor_el = document.getElementById("cursor")
    next_el = cursor_el.nextSibling

    if (!next_el || next_el.tagName != "SPAN") {
        return false
    }
    cursor_el.removeAttribute("id")
    next_el.setAttribute("id", "cursor")

    cursor_x_pos += 1
    return true
}

function backspace() {
    if (cursor_x_pos <= min_x_pos) {
        return false
    }

    var cursor_el = document.getElementById("cursor")
    prev_el = cursor_el.previousSibling

    if (!prev_el || prev_el.tagName != "SPAN" || prev_el.innerText == "\n") {
        return false
    }
    prev_el.parentNode.removeChild(prev_el)
    cursor_x_pos -= 1
    return true
}

function del() {
    if (!cursor_right()) {
        return false
    }
    backspace()
    return true
}

function home() {
    while(cursor_left()) {}
}

function end() {
    while(cursor_right()) {}
}

function prompt() {
    if (!token) {
        console_print("login: root\n")
        console_print("token: ")
        min_x_pos = 7
    } else {
        console_print("# ")
        min_x_pos = 2
    }
}

function sanitize_input(startCharsNum) {
    while(cursor_left()) {}

    for (var i = 0; i < startCharsNum; i += 1) {
        cursor_right()
    }
    while(del()) {}
    console_print("<hidden>")
}

function autocomplete(s) {
    var candidates = []

    autocomplete_words.forEach(function(item, num, arr) {
        if(item.startsWith(s)) {
            candidates.push(item)
        }
    })
    if (candidates.length == 0) {
        return ""
    } else if (candidates.length == 1) {
        return candidates[0].substring(s.length) + " "
    } else {
        console.log(candidates)
        candidates.sort()
        var first = candidates[0]
        var last = candidates[candidates.length - 1]

        for (var i = s.length; i < Math.min(first.length, last.length); i += 1) {
            if (first[i] != last[i]) {
                return first.substring(s.length, i)
            }
        }
        return first.substring(s.length)
    }
    return ""
}


function get_console_input() {
    var old_min_x_pos = min_x_pos
    min_x_pos = 0
    var cmd = ""
    while(cursor_left()) {}
    do {
        cmd += document.getElementById("cursor").textContent
    } while(cursor_right())
    min_x_pos = old_min_x_pos
    return cmd.slice(0, -1)
}


function history_prev() {
    if(cmd_history_pos == -1) {
        cmd_history_unfinished = get_console_input()
    }

    if(cmd_history_pos + 1 < cmd_history.length) {
        cmd_history_pos += 1
    } else {
        return
    }
    var cmd = cmd_history[cmd_history_pos]

    var old_min_x_pos = min_x_pos
    min_x_pos = 0
    while(cursor_right()) {}
    while(backspace()) {}
    min_x_pos = old_min_x_pos

    console_print(cmd)
}

function history_next() {
    if (cmd_history_pos < 0) {
        return
    }
    cmd_history_pos -= 1

    var cmd
    if (cmd_history_pos == -1) {
        cmd = cmd_history_unfinished
    } else {
        if(cmd_history_pos >= cmd_history.length) {
            return
        }

        cmd = cmd_history[cmd_history_pos]
    }

    var old_min_x_pos = min_x_pos
    min_x_pos = 0

    while(cursor_right()) {}
    while(backspace()) {}

    min_x_pos = old_min_x_pos

    console_print(cmd)
}

function get_request(t, cmd, args) {
    cur_req = new XMLHttpRequest()
    cur_req.open('GET', '/hello', true)
    cur_req.setRequestHeader("X-Authorization", "Bearier")
    cur_req.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    cur_req.onreadystatechange  = function() {
        if (cur_req.readyState == 4) {
            if (cur_req.status == 200) {
                token = t
            }
            var jsonResponse = JSON.parse(cur_req.responseText);
               console_print(jsonResponse["message"] + "\n")
               prompt()
               console_blocked = false
        }
                };
                cur_req.send('');
}

function call_api(t, cmd, args) {

    cur_req = new XMLHttpRequest()
    cur_req.open('POST', '/api', true)
    cur_req.setRequestHeader("X-Authorization", "Bearier " + t)
    cur_req.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    cur_req.onreadystatechange = function() {
        if (cur_req.readyState == 4) {
            if (cur_req.status == 200) {
                token = t
            }
                get_request(t, cmd, args)
                console_blocked = false
            }
        }
    cur_req.send(JSON.stringify({"cmd": cmd, "args": args}))
}

function sys_info() {
    cur_req = new XMLHttpRequest()
    cur_req.open('GET', '/sys_info', true)
    cur_req.setRequestHeader("X-Authorization", "Bearier")
    cur_req.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    cur_req.onreadystatechange  = function() {
        if (cur_req.readyState == 4) {
            var jsonResponse = JSON.parse(cur_req.responseText);
               console_print(jsonResponse["sys"] + "," + jsonResponse["architecture"] + " " + jsonResponse["machine"] + "\n" + jsonResponse["node"] + "\n")
               prompt()
        }
                };
    cur_req.send('');

}


function handle_command(cmd) {
    cmd = cmd.replace(/^\s+|\s+$/g, '')  // Trim
    console_blocked = true
    if (cmd.startsWith("token: ")) {
        t = cmd.substring(7)
        console.log("token", t)
        call_api(t, "login", [window.localStorage["session"]])
    } else if (cmd.startsWith("# ")) {
        cmd_history.unshift(cmd)
        cmd_history_pos = -1
        cmd_history_unfinished = ""

        words = cmd.substring(2).split(/\s+/)
        command_name = words[0]
        command_args = words.splice(1)
        console.log("name", command_name, "args", command_args)

        call_api(token, command_name, command_args)
    } else {
        prompt()
        console_blocked = false
    }
}

document.onkeydown = function(e) {
    e = e || window.event;

    if ( (e.key == "c" || e.key == "z" || e.key == "\\") && (e.ctrlKey || e.metaKey)) {
        if(e.key == "c" && window.getSelection().toString() != "") {
            return true
        }
        console_print("^" + e.key.toUpperCase() + "\n")
        console_blocked = false
        // console.log("unlocked")
        if (cur_req) {
            cur_req.onreadystatechange = function() {}
            cur_req.abort()
        }
        if (cur_timer) {
            clearTimeout(cur_timer)
            cur_timer = null
        }
        prompt()
        return false
    }

    if(console_blocked) {
        return true
    }
    if (e.key == "ArrowLeft") {
        cursor_left()
    } else if (e.key == "ArrowRight") {
        cursor_right()
    } else if (e.key == "Backspace") {
        backspace()
    } else if (e.key == "Delete") {
        del()
    } else if (e.key == "Home") {
        home()
    } else if (e.key == "End") {
        end()
    } else if (e.key == "ArrowUp") {
        history_prev()
    } else if (e.key == "ArrowDown") {
        history_next()
    } else if (e.key == "Enter") {
        min_x_pos = 0

        cmd = get_console_input()
        if (cmd.startsWith("token: ")) {
            sanitize_input(7)
        }

        console_print("\n")
        handle_command(cmd)
    } else if (e.key == "Tab") {
        var old_min_x_pos = min_x_pos
        min_x_pos = 0

        var cmd_len = 0
        while(cursor_left()) {
            cmd_len += 1
        }

        cmd = ""
        for (var i = 0; i < cmd_len; i += 1) {
            cmd += document.getElementById("cursor").textContent
            cursor_right()
        }

        min_x_pos = old_min_x_pos

        if (!cmd.startsWith("# ")) {
             return false
        }

        cmd = cmd.slice(2)
        if (cmd.length == 0) {
            return false
        }

        console_print(autocomplete(cmd))
    } else if (e.key.length == 1 && (!e.ctrlKey && !e.metaKey)) {
        console_print(e.key)
    } else {
        return true
    }
    return false
};

if (!window.localStorage["session"]) {
    var r = new Uint32Array(2);
    window.crypto.getRandomValues(r);
    window.localStorage["session"] = r[0].toString(16) + r[1].toString(16)
}


var console_el = document.getElementById("console")
console_el.setAttribute("contenteditable", true)
console_el.focus()
console_el.setAttribute("contenteditable", false)
console_el.addEventListener("paste", function(e) {
    e.preventDefault();
    var text = e.clipboardData.getData("text/plain");
    console_print(text.split("\n")[0])
});

sys_info()