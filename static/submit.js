// This file handles submitting formulas to the server

$(document).ready(function() {
  $("#formula-form").submit(function(event) {
    // Disable the default submit action
    event.preventDefault();

    // Get the formula and colapse all whitespace
    var formula = $("#formula").val().replace(/\s/g, ' ');

    // Evaluate the formula
    try {
      var result = math.evaluate(formula);
    } catch(err) {
      $("#submission-alert").text(
        "Invalid mathematical formula: " + err
      ).show();
      return;
    }

    // Submit the evaluated formula to the server
    $.post("/calculations", formula + " = " + result)
      .done(function () {
        // Submission was successful, hide the alert (if it's showing) and clear
        // the text area
        $("#submission-alert").hide();
        $("#formula").val('');
      }).fail(function (jqXHR, textStatus) {
        // Display an alert indicating the request failed
        $("#submission-alert").text(
          "Failed to save calculation, please try again or contact the \
           administrator"
        ).show();
      });
  });
})
