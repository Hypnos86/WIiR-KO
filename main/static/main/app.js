
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

document.addEventListener("DOMContentLoaded", function() {
    var message = document.getElementById("loginMessage");
    var disappearTime = 5000;

    function hideElement() {
       if(message){
      message.style.display = "none";
    }
}

   setTimeout(hideElement, disappearTime);
 });
 // Funkcja sprawdzająca aktualny czas i odpowiednio pokazująca/ukrywająca przycisk
function showHideButton() {
    var now = new Date();
    var currentHour = now.getHours();

     // Poniżej ustaw godziny, o których ma być pokazywany/ukrywany przycisk
     var showHour = 15; // Godzina, o której przycisk ma być pokazany
     var hideHour = 16; // Godzina, o której przycisk ma być ukryty

     var button = document.getElementById('dbDiv');

     if (currentHour === showHour) {
       button.style.display = 'block'; // Pokazuje przycisk
     } else if (currentHour === hideHour) {
       button.style.display = 'none'; // Ukrywa przycisk
     }
    }
// Funkcja wywoływana co minutę do sprawdzania czasu i pokazywania/ukrywania przycisku
setInterval(showHideButton, 300000); // Co 5 minut

function showSnackbar() {
      var snackbar = document.getElementById("snackbarDB");
      snackbar.classList.add("show");
      setTimeout(function(){
        snackbar.classList.remove("show");
        console.log('snackar');
      }, 3000); // Snackbar znika po 3 sekundach (3000 milisekund)
}

