var pswinput = document.getElementById("btn__generatepswrd");


// pswinput.onclick = function () {
//     var length = (len) ? (len) : (10);
//     var string = "abcdefghijklmnopqrstuvwxyz"; //to upper 
//     var numeric = '0123456789';
//     var punctuation = '!@#$%^&*()_+~`|}{[]\:;?><,./-=';
//     var password = "";
//     var character = "";
//     var crunch = true;
//     while (password.length < length) {
//         entity1 = Math.ceil(string.length * Math.random() * Math.random());
//         entity2 = Math.ceil(numeric.length * Math.random() * Math.random());
//         entity3 = Math.ceil(punctuation.length * Math.random() * Math.random());
//         hold = string.charAt(entity1);
//         hold = (password.length % 2 == 0) ? (hold.toUpperCase()) : (hold);
//         character += hold;
//         character += numeric.charAt(entity2);
//         character += punctuation.charAt(entity3);
//         password = character;
//     }
//     password = password.split('').sort(function () { return 0.5 - Math.random() }).join('');
//     document.getElementById("password").value = password;
//     document.getElementById("rpassword").value = password;
//     return password.substr(0, len);
// }

pswinput.onclick = function () {
    var pLength = Math.random() * (14 - 6) + 6;
    var keyListAlpha = "abcdefghijklmnopqrstuvwxyz",
        keyListAlphaUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        keyListInt = "123456789",
        keyListSpec = "!@#_",
        password = '';
    var len = Math.ceil(pLength / 2);
    len = len - 1;
    var lenSpec = pLength - 2 * len;

    for (i = 0; i < len; i++) {
        password += keyListAlpha.charAt(Math.floor(Math.random() * keyListAlpha.length));
        password += (keyListAlpha.charAt(Math.floor(Math.random() * keyListAlpha.length))).toUpperCase();
        password += keyListInt.charAt(Math.floor(Math.random() * keyListInt.length));
    }

    for (i = 0; i < lenSpec; i++)
        password += keyListSpec.charAt(Math.floor(Math.random() * keyListSpec.length));
    password = password.split('').sort(function () { return 0.5 - Math.random() }).join('');
    navigator.clipboard.writeText(password);
    document.getElementById("password").value = password;
    document.getElementById("rpassword").value = password;

    var password = document.getElementById("password").value;
    var rpassword = document.getElementById("rpassword").value;
    if (password != rpassword) {
        document.getElementsByClassName("error-text")[0].textContent = 'Password and control password have to be same';
        document.getElementsByClassName("rpassword")[0].style = "border: 1px solid var(--red-color);";
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        document.getElementById("rpassword").setCustomValidity('Passwords do not match');
        // button.disabled = true;
    } else if (rpassword == password) {
        document.getElementsByClassName("error-text")[0].textContent = '';
        document.getElementsByClassName("rpassword")[0].style = "border: 1px solid var(--btn-color);";
        document.getElementsByClassName("error-panel")[0].style = "dipslay: none;";
        document.getElementById("rpassword").setCustomValidity('');
        // button.disabled = false;
    }

    /* Show password */
    // var passwordinput = document.getElementById("password");
    // var rpasswordinput = document.getElementById("rpassword");
    // if (passwordinput.type === "password" || rpasswordinput.type === "password") {
    //     passwordinput.type = "text";
    //     rpasswordinput.type = "text";
    // }
}