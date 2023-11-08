/**
 * Generic functions to toggle fields/fieldsets in the admin panel on/off.
 */

/**
 * Generic script to toggle the visibility of fieldsets in admin inline fieldsets section on/off.
 * Toggles on select dropdown value change.
 * @param {Object} $ jQuery object
 * @param {String} parent_class_name A parent DOM element class name for admin fieldsets, e.g. `.field-legal_approval`
 * @param {String} data_attribute_name A model field to check against for whether to toggle on or off, e.g. `has-additional-permissions`
 * @param {String} fieldset_class_name A fieldset DOM element class name to toggle on/off, e.g. `.additional-information-docs`. Provided from the django admin side.
 */
function toggle_fieldset_on_select_change(
  $,
  parent_class_name,
  data_attribute_name,
  fieldset_class_name,
) {
  var toggle_fieldset_section = (ctx) => {
    // Toggles the `fieldset_class_name` fieldset section section on/off
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
      toggle_fieldset_section($(this));
    });
}

/**
 * Generic script to toggle the visibility of admin fieldset sections on/off.
 * Toggles on checkbox value change.
 * @param {*} $ jQuery object
 * @param {*} checked_field_identifier The identifier id of the checkbox field, follows the structure `id_model_field_name`
 * @param {*} fieldset_class_name A fieldset DOM element class name to toggle on/off, e.g. `.admin-contentious-burn`. Provided from the django admin side.
 */
function toggle_fieldset_on_checked_change(
  $,
  checked_field_identifier,
  fieldset_class_name,
) {
  var boolean_checked_field = $(checked_field_identifier);
  var toggle_fieldset_section = (show) => {
    // Toggles the `fieldset_class_name` fieldset section section on/off
    if (show) {
      $(fieldset_class_name).show();
    } else if (!show) {
      $(fieldset_class_name).hide();
    } else {
      console.error(
        `Error: can not get checked status of ${checked_field_identifier} check box`,
      );
    }
  };
  toggle_fieldset_section(boolean_checked_field.is(":checked"));
  boolean_checked_field.change(function () {
    console.log("change", $(this).is(":checked"));
    toggle_fieldset_section($(this).is(":checked"));
  });
}
