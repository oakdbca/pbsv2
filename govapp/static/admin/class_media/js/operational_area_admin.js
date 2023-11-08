/**
 * This script is used to toggle the visibility of the contentious burn rationale fieldset section
 * in the Operational Area admin form.
 */
(function ($) {
  $(function () {
    // Run after document loaded
    toggle_fieldset_on_checked_change(
      $, // jQuery object
      "#id_contentious_burn", // The identifier id of the checkbox field is `id_model_field_name`
      ".admin-contentious-burn", // Class name of the fieldset to toggle on/off
    );
  });
})(django.jQuery);
