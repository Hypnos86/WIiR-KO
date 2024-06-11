function openLoginModal(button) {
  const url = $(button).data("url");
  $("#login .modal-content").load(url);
  $("#login").modal("show");
}

function openHelpModal(button) {
  const url = $(button).data("url");
  $("#helpModal .modal-content").load(url);
  $("#helpModal").modal("show");
}

$(function () {
  $('[data-toggle="info"]').tooltip();
});

function snackbarFunction() {
  const tost = document.getElementById("snackbar");
  tost.className = "show";
  setTimeout(function () {
    tost.className = tost.className.replace("show", "");
  }, 4000);
}

function showLogInSnackbar() {
  try {
    const snackbar = document.getElementById("logIn");
    snackbar.className = "log-in show";
    setTimeout(function () {
      snackbar.className = snackbar.className.replace("log-in show", "log-in");
    }, 2000);
  } catch (error) {
    console.error(error);
  }
}
function showLogOutSnackbar() {
  try {
    const snackbar = document.getElementById("logOut");
    snackbar.className = "log-out show";
    setTimeout(function () {
      snackbar.className = snackbar.className.replace(
        "log-out show",
        "log-out"
      );
    }, 2000);
  } catch (error) {
    console.error(error);
  }
}
