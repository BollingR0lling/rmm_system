var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];
var sendBtn = document.getElementById("sendBtn");
btn.onclick = function() {
  modal.style.display = "block";
}
sendBtn.onclick = function() {
    if (document.getElementById("iframeArea").value.startsWith("<iframe")) {
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