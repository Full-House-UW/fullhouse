$(window).load(function() {
  var createHouseLink = $("#create_house_link")[0];

  $(createHouseLink).click(toggleCreateHouse);
});

function toggleCreateHouse() {
  var chdiv = $("#createhouse")[0];

  if (chdiv.style.display == "none") {
    chdiv.style.display = "";
  } else {
    chdiv.style.display = "none";
  }
}
