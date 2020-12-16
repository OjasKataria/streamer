function twitch(){
    var x = document.getElementById("twitch-form")
    x.style.display = "block";
}

function enabletwitch() {
    document.getElementById("twitch-channel").disabled = false;
}

window.onload = function (){
    document.getElementsByName("potty")[0].onclick = function () {
        document.getElementById("video-link").style.display = "block";
}};