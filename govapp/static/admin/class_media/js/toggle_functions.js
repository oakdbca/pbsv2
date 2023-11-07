/**
 * Generic functions to toggle fields/fieldsets in the admin panel on/off.
 */

/**
 * Generic script to toggle the visibility of fieldsets in admin inline fieldsets section on/off.
 * @param {Object} $ jQuery object
 * @param {String} parent_class_name A parent DOM element class name for admin fieldsets, e.g. `.field-legal_approval`
 * @param {String} data_attribute_name A model field to check against for whether to toggle on or off, e.g. `has-additional-permissions`
 * @param {String} fieldset_class_name A fieldset DOM element class name to toggle on/off, e.g. `.additional-information` (default)
 */
function toggle_additional_information_on_select_change(
  $,
  parent_class_name,
  data_attribute_name,
  fieldset_class_name = "additional-information",
) {
  var toggle_additional_information = (ctx) => {
    // Toggles the the additional information fieldset section on/off
    const show =
      ctx.find("option:selected").data(data_attribute_name) === "True"
        ? true
        : false;
    const fieldset_additional_information = $(ctx.parents("fieldset")[0]).next(
      `fieldset.${fieldset_class_name}`,
    );

    if (show) {
      fieldset_additional_information.removeClass("hidden");
    } else if (!show) {
      fieldset_additional_information.addClass("hidden");
    } else {
      console.error(
        `Error: can not get status of ${data_attribute_name} givdata attribute`,
      );
    }
  };

  $(parent_class_name)
    .find("select")
    .change(function () {
      toggle_additional_information($(this));
    });
}
