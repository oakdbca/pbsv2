/**
 * This script is used to toggle the visibility of the additional information fieldset section
 * (class .additional-information to be defined in the admin Media subclass) of admin inline
 * pages of/off.
 */

(function ($) {
  // Run after document loaded
  $(function () {
    toggle_fieldset_on_select_change(
      $, // jQuery
      ".field-legal_approval", // Fieldsets parent div element class name
      "has-additional-permissions", // Custom choice field, see: OperationalAreaApprovalChoiceField
      "additional-information-docs", // Class name of the fieldset to toggle on/off
    );
    toggle_fieldset_on_select_change(
      $, // jQuery
      ".field-legal_approval", // Fieldsets parent div element class name
      "is-shire-approval", // Custom choice field, see: OperationalAreaApprovalChoiceField
      "additional-information-lga", // Class name of the fieldset to toggle on/off
    );
  });
})(django.jQuery);
