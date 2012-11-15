window.onload(function() {
  var chdiv = $("#createhouse");
  chdiv.style.visibility = "hidden";

  chdiv.addEventListener("click", toggleCreateHouse, false);
});

function toggleCreateHouse() {
  var chdiv = $("#createhouse");

  if (chdiv.style.visibility == "hidden") {
    chdiv.style.visibility = "visible";
  } else {
    chdiv.style.visibility = "hidden";
  }
}
