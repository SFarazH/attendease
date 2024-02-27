var form = document.getElementById("inputForm");
var spinner = document.getElementById("spinnerDiv");
var overlay = document.getElementById("overlay");

form.addEventListener("submit", () => {
  spinner.classList.add("spinner-border");
  overlay.classList.add("overlay");
  console.log("ok");
});
