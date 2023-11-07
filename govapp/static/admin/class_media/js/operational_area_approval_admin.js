/**
 * This script is used to toggle the visibility of the additional information fieldset section
 * (class .additional-information to be defined in the admin Media subclass) of admin inline
 * pages of/off.
 */

(function ($) {
  $(function () {
    // Run after document loaded
    toggle_additional_information_on_select_change(
      $, // jQuery
      ".field-legal_approval", // Fieldsets parent div element class name
      "has-additional-permissions", // Custom choice field, see: OperationalAreaApprovalChoiceField
      "additional-information", // Class name of the fieldset to toggle on/off
    );
  });
})(django.jQuery);
