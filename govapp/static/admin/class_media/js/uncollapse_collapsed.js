/**
 * Script to start collapsible inlines in uncollapsed (hidden) form with the option
 * to hide them, rather than the default of starting them collapsed with the option
 * to show them.
 *
 * Usage:
 *     class Media:
            js = (
                "admin/js/jquery.init.js",
                "admin/class_media/js/uncollapse_collapsed.js",
            )
        fieldsets = (
            (
                None,
                {
                    "fields": (
                        ...
                    ),
                    "classes": (
                        "collapse",
                        "uncollapse-collapsed",
                    ),
                },
            ),
        )

 */
(function ($) {
    // Run after document loaded
    $(function () {
        const fieldsets = document.querySelectorAll('fieldset.uncollapse-collapsed');
        for (const [i, elem] of fieldsets.entries()) {
            elem.classList.remove('collapsed');
            elem.classList.add('collapse', 'in');
            $(elem).find('h2 a').text(function () { return "Hide" })
        }
    });
})(django.jQuery);
