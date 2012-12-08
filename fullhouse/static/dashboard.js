$(window).load(resizePanes);
$(window).resize(resizePanes);

function resizePanes() {
  var winHeight = window.innerHeight ? window.innerHeight : document.documentElement.offsetHeight;
  var paneHeight = Math.max(winHeight * .55, 320);
  var innerPaneHeight = paneHeight - 80;
  

  $(".pane").each(function(index, element) {
    element.style.height = paneHeight + "px";
    $(element).find(".inner_pane")[0].style.height = innerPaneHeight + "px";
  });
}
