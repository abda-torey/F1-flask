"use strict";
window.addEventListener("load", function () {
  var ui = new firebaseui.auth.AuthUI(firebase.auth());
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
        document.getElementById("logout").onclick = function () {

          firebase.auth().signOut();

          // clear the token cookie
          document.cookie = "token=";

          // redirect the user on logout
          window.location.replace("/");
          
          };
      } else {
       
        document.cookie = "token=";
        document.getElementById("login").onclick =  function () {
            ui.start("#firebase-auth-container", uiConfig);
          };
      }
    },
    function (error) {
      console.log(error);
      alert("Unable to log in: " + error);
    }
  );
});
