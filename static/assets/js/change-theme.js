// var btn = document.getElementById("btn__theme");
// var link = document.getElementById("theme-link");
// let defaultTheme = "/assets/css/auth.css";
// var localTheme = localStorage.theme;

// (function() {
//     setTheme(localTheme)
//   })();

//   console.log(localStorage.theme);
  

// btn.addEventListener("click", function () { ChangeTheme(); });

// function ChangeTheme()
// {
//     let lightTheme = "/assets/css/light.css";
//     let darkTheme = "/assets/css/auth.css";

//     var currTheme = link.getAttribute("href");
//     var theme = "";

//     if(currTheme == lightTheme)
//     {
//    	 currTheme = darkTheme;
//    	 theme = "dark";
//     }
//     else
//     {    
//    	 currTheme = lightTheme;
//    	 theme = "light";
//     }

//     link.setAttribute("href", currTheme);
//     localStorage.theme = currTheme;
//     console.log(localStorage.theme);
    
// }

// function setTheme(theme) {
//     link.setAttribute("href", theme);
// }


var toggle = document.getElementById("theme-toggle");

var storedTheme = localStorage.getItem('theme') || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
if (storedTheme)
    document.documentElement.setAttribute('data-theme', storedTheme)


toggle.onclick = function() {
    var currentTheme = document.documentElement.getAttribute("data-theme");
    var targetTheme = "light";

    if (currentTheme === "light") {
        targetTheme = "dark";
    }

    document.documentElement.setAttribute('data-theme', targetTheme)
    localStorage.setItem('theme', targetTheme);
};

