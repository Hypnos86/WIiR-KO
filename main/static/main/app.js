
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

function showLogInSnackbar() {
    try{
        var snackbar = document.getElementById("logIn");
        snackbar.className = "log-in show";
        setTimeout(function(){
            snackbar.className = snackbar.className.replace("log-in show", "log-in");
        }, 3000);
    }
    catch(error){
        console.error(error)
    }
};
function showLogOutSnackbar() {
    try{
        var snackbar = document.getElementById("logOut");
        snackbar.className = "log-out show";
        setTimeout(function(){ snackbar.className = snackbar.className.replace("log-out show", "log-out"); }, 3000);
    }
    catch(error){
        console.error(error)
    }
};