count = document.querySelectorAll(".count");
var num, den;

for (var i = 0; i < count.length; i++) {
  num = parseInt(count[i].textContent.split("/")[0]);
  den = parseInt(count[i].textContent.split("/")[1]);

  function atclass(num, den) {
    num = num + 1;
    den = den + 1;
    return parseFloat((num / den) * 100).toFixed(1);
  }

  function missclass(num, den) {
    num = num;
    den = den + 1;
    return parseFloat((num / den) * 100).toFixed(1);
  }

  document.querySelectorAll(".attend")[i].textContent =
    " " + atclass(num, den) + "%";
  document.querySelectorAll(".miss")[i].textContent =
    " " + missclass(num, den) + "%";
}

var [numF, denF] = document
  .getElementById("countFinal")
  .textContent.split("/")
  .map(Number);
console.log(numF, denF);

document.getElementById("attendFinal").textContent =
  " " + atclass(numF, denF) + "%";
document.getElementById("missFinal").textContent =
  " " + missclass(numF, denF) + "%";

percentage = document.querySelectorAll(".percentage");
bar = document.querySelectorAll(".progress-bar");

for (var i = 0; i < percentage.length; i++) {
  percent = parseFloat(percentage[i].textContent);

  if (percent < 60) {
    bar[i].classList.add("bg-danger");
    percentage[i].classList.add("danger");
  } else if ((percent >= 60) & (percent < 75)) {
    bar[i].classList.add("bg-warning");
    percentage[i].classList.add("warning");
  } else {
    bar[i].classList.add("bg-success");
    percentage[i].classList.add("success1");
  }
}

finalPercent = parseInt(document.querySelector(".pFinal").textContent);
if (finalPercent < 60) {
  txt = "Consider attending some classes!";
} else if ((finalPercent >= 60) & (finalPercent <= 75)) {
  txt = "Keep those medical certificates ready!";
} else if ((finalPercent > 75) & (finalPercent <= 85)) {
  txt = "Don't worry, you're safe!";
} else if (finalPercent > 85) {
  txt = "Why dont you take a few days off!";
}

document.querySelector(".textFinal").innerText = txt;
