window.onload = function() {
  var createHouseLink = $("#create_house_link")[0];

  if (createHouseLink.addEventListener) {
    createHouseLink.addEventListener("click", toggleCreateHouse, false);
  } else {
    createHouseLink.attachEvent("onclick", toggleCreateHouse);
  }
};

function toggleCreateHouse() {
  var chdiv = $("#createhouse")[0];

  if (chdiv.style.display == "none") {
    chdiv.style.display = "";
  } else {
    chdiv.style.display = "none";
  }
}
