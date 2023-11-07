/**
 * This script is used to toggle the visibility of the additional information fieldset section
 * in the Operational Area Legal/Approval admin form.
 */
(function ($) {
  $(function () {
    // Run after document loaded
    var has_additional_permissions = $("#id_has_additional_permissions");
    var toggle_additional_information = (show) => {
      // Toggles the the additional information fieldset section on/off
      if (show) {
        $(".additional-information").show();
      } else if (!show) {
        $(".additional-information").hide();
      } else {
        console.error(
          "Error: can not get checked status of has_additional_permissions field",
        );
      }
    };
    toggle_additional_information(has_additional_permissions.is(":checked"));
    has_additional_permissions.change(function () {
      console.log("change", $(this).is(":checked"));
      toggle_additional_information($(this).is(":checked"));
    });
  });
})(django.jQuery);
