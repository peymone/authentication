var myInput = document.getElementById("password");
var myInput2 = document.getElementById("rpassword");
var myInput3 = document.getElementById("login");
var myInput4 = document.getElementById("email");
const button = document.getElementById('btn__signup');

myInput.onkeyup = function () {
    var password = document.getElementById("password").value;
    var rpassword = document.getElementById("rpassword").value;

    if (typeof password !== 'string') {
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        return [false, 'Error in validatePassword'];
    }

    if (password.length <= 7) {
        document.getElementsByClassName("error-text")[0].textContent = 'Password must have at least 8 characters';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        return [false, 'Password must have at least 8 characters'];
    }

    if (password.search(/[a-z]/) === -1) {
        document.getElementsByClassName("error-text")[0].textContent = 'Password must contain at least one lower case letter';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        return [false, 'Password must contain at least one lower case letter'];
    }

    if (password.search(/[A-Z]/) === -1) {
        document.getElementsByClassName("error-text")[0].textContent = 'Password must contain at least one upper case letter';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        return [false, 'Password must contain at least one upper case letter'];
    }

    if (password.search(/[0123456789]/) === -1) {
        document.getElementsByClassName("error-text")[0].textContent = 'Password must contain at least one digit';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
        return [false, 'Password must contain at least one digit'];
    }

    // if (password.search(/[!@#$%^&*()\-=_+[\]{}'"\\|,./<>?]/) === -1) {
    //     document.getElementsByClassName("help-text")[0].textContent = 'Password must contain at least one digit'
    //     return [false, 'Password must contain at least one upper case letter']
    //     alert('Password must contain at least one upper case letter');
    // }
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
    } else {
        document.getElementsByClassName("error-text")[0].textContent = "";
        document.getElementsByClassName("error-panel")[0].style = "dipslay: none;";
    }

    return [true];
}

myInput2.onkeyup = function () {
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
}

myInput3.onkeyup = function () {
    var login = document.getElementById("login").value;
    login = document.getElementById("login").value = login.toLowerCase();
    if (login.search(/[a-zA-z]/)) {
        document.getElementsByClassName("error-text")[0].textContent = 'Login must contain at least one letter';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
    } else if (login.length <= 4) {
        document.getElementsByClassName("error-text")[0].textContent = 'Login must contain at least 5 characters';
        document.getElementsByClassName("error-panel")[0].style = "display: block;";
    } else {
        document.getElementsByClassName("error-text")[0].textContent = '';
        document.getElementsByClassName("error-panel")[0].style = "display: none;";
    }
}

myInput4.onkeyup = function () {
    var email = document.getElementById("email").value;
    document.getElementById("email").value = email.toLowerCase();
}