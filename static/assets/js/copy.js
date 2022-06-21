var email1 = document.getElementById("credits__email");
var email2 = document.getElementById("credits__email2");

email1.onclick = function () {
    emailclip = document.getElementById("credits__email").textContent;
    navigator.clipboard.writeText(emailclip.trim());
}

email2.onclick = function () {
    emailclip2 = document.getElementById("credits__email2").textContent;
    navigator.clipboard.writeText(emailclip2.trim());
}