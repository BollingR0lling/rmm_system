var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var sendBtn = document.getElementById("sendBtn");
btn.onclick = function() {
  modal.style.display = "block";
}
sendBtn.onclick = function() {
    cur_req = new XMLHttpRequest()
    const csrftoken = getCookie('csrftoken');
    if (document.getElementById("iframeArea").value.startsWith("http://")) {
        cur_req.open('POST', window.location.href, true)
        cur_req.setRequestHeader('Content-type', 'application/json; charset=utf-8');
        cur_req.setRequestHeader('X-CSRFToken', csrftoken)
        cur_req.send(JSON.stringify({"link": document.getElementById("iframeArea").value}))
        alert("Success");
    } else {
        alert("You must insert iframe link")
    }
}
span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}