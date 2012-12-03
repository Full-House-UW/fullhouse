window.onload = function() {
  // Add an event for adding a form field.
  var add_form = $("#add_email")[0];

  if (add_form.addEventListener) {
    add_form.addEventListener("click", addEmailField);
  else {
    add_form.attachEvent("onclick", addEmailField);
  }
}

function addEmailField(e) {
  // Grab the number of fields already in here and increment.
  var numFieldsInput = $("#id_form-TOTAL_FORMS")[0];
  var newFieldIndex = numFieldsInput.value;
  numFieldsInput.value = newFieldIndex + 1;

  var form = $($("#emptyform")[0].childNodes[1]).clone()[0];
  var form_id = $(form.childNodes[0]).attr("for").replace("__prefix__", newFieldIndex);
  var form_name = $(form.childNodes[2]).attr("name").replace("__prefix__", newFieldIndex);
  $(form.childNodes[0]).attr("for", form_id);

  var form_input = $(form.childNodes[2]);
  form_input.attr("name", form_name);
  form_input.attr("id", form_id);

  $("#forms")[0].appendChild(form);
}
