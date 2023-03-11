"use strict";
window.addEventListener("load", function () {
  var logoutButton = document.getElementById("logout");
  var loginButton = document.getElementById("login");
  if (logoutButton) {
    logoutButton.onclick = function () {
      // ask firebase to sign out the user
      firebase.auth().signOut();
    };
  }
   if (loginButton) {
    loginButton.onclick = function () {
      var ui = new firebaseui.auth.AuthUI(firebase.auth());
      ui.start("#firebase-auth-container", uiConfig);
      document.cookie = "token=";
    };
  }

  var uiConfig = {
    signInSuccessUrl: "/",
    signInOptions: [firebase.auth.EmailAuthProvider.PROVIDER_ID],
  };

  firebase.auth().onAuthStateChanged(
    function (user) {
      if (user) {
        console.log("Signed in as ", user.displayName, user.email);
        user.getIdToken().then(function (token) {
          document.cookie = "token=" + token;
        });
      } else {
        var ui = new firebaseui.auth.AuthUI(firebase.auth());
        ui.start("#firebase-auth-container", uiConfig);
        document.cookie = "token=";
      }
    },
    function (error) {
      console.log(error);
      alert("Unable to log in: " + error);
    }
  );
});
