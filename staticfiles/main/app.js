// Uniwersalna funkcja do ładowania modali
function openModal(button, modalId) {
  const url = $(button).data("url");
  const $modal = $(modalId);

  if (url) {
    $modal.find(".modal-content").load(url, function () {
      $modal.modal("show");
    });
  }
}

// Skrócone funkcje wywołujące (zachowuję nazwy, by pasowały do Twojego HTML)
function openLoginModal(button) {
  openModal(button, "#login");
}
function openHelpModal(button) {
  openModal(button, "#helpModal");
}

// Inicjalizacja Tooltipów i innych elementów po załadowaniu DOM
$(function () {
  $('[data-toggle="info"], [data-bs-toggle="tooltip"]').tooltip();
});

// Uniwersalny Snackbar (obsługuje log-in, log-out i inne)
function showSnackbar(elementId, activeClass = "show", duration = 2000) {
  const snackbar = document.getElementById(elementId);

  if (snackbar) {
    snackbar.classList.add("show"); // Użycie classList jest bezpieczniejsze niż className

    setTimeout(function () {
      snackbar.classList.remove("show");
    }, duration);
  }
}

// Funkcje wywoływane przez Django Messages
function showLogInSnackbar() {
  showSnackbar("logIn");
}

function showLogOutSnackbar() {
  showSnackbar("logOut");
}

// Twoja ogólna funkcja snackbara
function snackbarFunction() {
  showSnackbar("snackbar", "show", 4000);
}
