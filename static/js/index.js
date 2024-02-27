var form = document.getElementById("inputForm");
var spinner = document.getElementById("spinnerDiv");
var overlay = document.getElementById("overlay");

document.getElementById("demoBtn").addEventListener("click", demo);

function demo() {
  document.getElementById("userID").value = "demo@rknec.edu";
  document.getElementById("password").value = "demo@rknec.edu";
}

form.addEventListener("submit", () => {
  spinner.classList.add("spinner-border");
  overlay.classList.add("overlay");
  console.log("ok");
});
