$(window).load(function() {
  // Add an event for adding a form field.
  var add_form = $("#add_email")[0];

  $(add_form).click(addEmailField);
});

function addEmailField(e) {
  // Grab the number of fields already in here and increment.
  var numFieldsInput = $("#id_form-TOTAL_FORMS")[0];
  var newFieldIndex = parseInt(numFieldsInput.value);
  numFieldsInput.value = newFieldIndex + 1;

  var form = $($("#emptyform")[0].getElementsByTagName("p")[0]).clone()[0];
  var label = form.getElementsByTagName("label")[0];
  var input = form.getElementsByTagName("input")[0];
  var form_id = $(label).attr("for").replace("__prefix__", newFieldIndex);
  var form_name = $(input).attr("name").replace("__prefix__", newFieldIndex);
  $(label).attr("for", form_id);

  var form_input = $(input);
  form_input.attr("name", form_name);
  form_input.attr("id", form_id);

  $("#forms")[0].appendChild(form);
}
