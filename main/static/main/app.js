
function openLoginModal(button){
        var url = $(button).data("url");
        $("#login .modal-content").load(url);
        $("#login").modal("show");
    }

function openHelpModal(button){
        var url = $(button).data("url");
        $("#helpModal .modal-content").load(url);
        $("#helpModal").modal("show");
    }

$(function () {
        $('[data-toggle="info"]').tooltip()
    })

function snackbarFunction() {
    var tost = document.getElementById("snackbar");
    tost.className = "show";
        setTimeout(function () {
            tost.className = tost.className.replace("show", "");
        }, 10000);
}

function snackbarLogOutFunction() {
    var tost = document.getElementById("logOut");
    tost.className = "show";
        setTimeout(function () {
            tost.className = tost.className.replace("show", "");
        }, 10000);
}

document.addEventListener("DOMContentLoaded", function() {
    var message = document.getElementById("loginMessage");
    var disappearTime = 5000;

    function hideElement() {
       if(message){
      message.style.display = "none";
    }
}
 });
