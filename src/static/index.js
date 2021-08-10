function show() {
  var x = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }

}
function change() {
  var x = document.getElementById("ButtonShowHide");
  if (x.textContent === "Show solved sudoku board") {
    x.textContent = "Hide solved sudoku board";
  } else {
    x.textContent = "Show solved sudoku board";
  }
}