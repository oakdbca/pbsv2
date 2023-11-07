/**
 * Generic functions to toggle fields/fieldsets in the admin panel on/off.
 */

/**
 * Generic script to toggle the visibility of fieldsets in admin inline fieldsets section on/off.
 * @param {Object} $ jQuery object
 * @param {String} parent_class_name A parent DOM element class name for admin fieldsets, e.g. `.field-legal_approval`
 * @param {String} data_attribute_name A model field to check against for whether to toggle on or off, e.g. `has-additional-permissions`
 * @param {String} fieldset_class_name A fieldset DOM element class name to toggle on/off, e.g. `.additional-information-docs` (default)
 */
function toggle_fieldset_on_select_change(
  $,
  parent_class_name,
  data_attribute_name,
  fieldset_class_name,
) {
  var toggle_additional_information = (ctx) => {
    // Toggles the the additional information fieldset section on/off
    const show =
      ctx.find("option:selected").data(data_attribute_name) === "True"
        ? true
        : false;
    // Get the next sibling fieldsets matched against `fieldset_class_name`
    const fieldsets_matched = $(ctx.parents("fieldset")).nextAll(
      `fieldset.${fieldset_class_name}`,
    );

    if (show) {
      fieldsets_matched.removeClass("hidden");
    } else if (!show) {
      fieldsets_matched.addClass("hidden");
    } else {
      console.error(
        `Error: can not get status of ${data_attribute_name} data attribute`,
      );
    }
  };

  $(parent_class_name)
    .find("select")
    .change(function () {
      toggle_additional_information($(this));
    });
}
