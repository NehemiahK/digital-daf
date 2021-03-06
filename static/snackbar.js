var moveSnackbarOffscreen = () => $("#snackbar").css("bottom", -400);
var hideSnackbar = () => $("#snackbar").animate({"bottom": -400});

var updateSnackbar = function(labelHtml, buttons) {
  $("#snackbar-text").html(labelHtml);
  var buttonsDiv = $("#snackbar-buttons").html("");
  if (!buttons) {
    buttons = [];
  } else if (!buttons.length) {
    buttons = [buttons];
  }
  for (var i in buttons) {
    var button = buttons[i]
    buttonsDiv.append(
      `<button class="mdl-button mdl-js-button mdl-button--colored">${button.text}</button>`);
  }

  var buttonElements = $("#snackbar-buttons button");
  for (var i = 0; i < buttonElements.length; i++) {
    $(buttonElements[i]).click(buttons[i].onClick);
  }
}

var displaySnackbar = function(labelHtml, buttons) {
  updateSnackbar(labelHtml, buttons);

  moveSnackbarOffscreen();
  $("#snackbar").animate({"bottom": 0});
}

var hasSeenLatestPreferences = function() {
  if (localStorage.lastViewedVersionOfPreferencesPage) {
    return parseInt(localStorage.lastViewedVersionOfPreferencesPage) === 1;
  }
  return false;
}

var hasSeenPreferencesSnackbarEnough = function() {
  return parseInt(localStorage.preferencePageCounter) < 3;
}

PREFERENCES_PAGE_SNACKBAR_COUNT_MAX = 3;

$(document).ready(function() {
  moveSnackbarOffscreen();

  var preferencePageSnackbarShownCount = localStorage.preferencePageSnackbarShownCount || 0;
  preferencePageSnackbarShownCount++;

  if (window.location.pathname !== "/preferences"
      && !hasSeenLatestPreferences()
      && preferencePageSnackbarShownCount <= PREFERENCES_PAGE_SNACKBAR_COUNT_MAX) {
    localStorage.preferencePageSnackbarShownCount = preferencePageSnackbarShownCount;
    displaySnackbar("Check out the available options available!", [
      {
        text: "Preferences",
        onClick: function() {
          gtag("event", "snackbar.preferences_page.clicked");
          window.location.pathname = "/preferences"
        },
      },
      {
        text: "Dismiss",
        onClick: function() {
          gtag("event", "snackbar.preferences_page.dismissed");
          localStorage.preferencePageSnackbarShownCount = PREFERENCES_PAGE_SNACKBAR_COUNT_MAX;
          hideSnackbar();
        },
      },
    ]);
  }
});
