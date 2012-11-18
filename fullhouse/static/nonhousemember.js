window.onload = function() {
  var chdiv = $("#createhouse")[0];
  chdiv.style.display = "none";

  var createHouseLink = $("#create_house")[0];
  createHouseLink.addEventListener("click", toggleCreateHouse, false);
};

function toggleCreateHouse() {
  var chdiv = $("#createhouse")[0];

  if (chdiv.style.display == "none") {
    chdiv.style.display = "";
  } else {
    chdiv.style.display = "none";
  }
}
