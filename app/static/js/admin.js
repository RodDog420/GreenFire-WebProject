/**
 * admin.js
 *
 * Admin product form:
 *   - Slug auto-generation from name (new products only)
 *   - Show/hide type-specific field sections based on product_type
 */

document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------------
    // SLUG AUTO-GENERATION
    // Only active on new product forms (slug field is not readonly).
    // ------------------------------------------------------------------

    var nameInput = document.getElementById('name');
    var slugInput = document.getElementById('slug');

    if (nameInput && slugInput && !slugInput.readOnly) {
        var slugEdited = slugInput.value.length > 0;

        nameInput.addEventListener('input', function () {
            if (slugEdited) { return; }
            slugInput.value = nameInput.value
                .toLowerCase()
                .replace(/[^a-z0-9\s-]/g, '')
                .trim()
                .replace(/\s+/g, '-')
                .replace(/-+/g, '-');
        });

        slugInput.addEventListener('input', function () {
            slugEdited = slugInput.value.length > 0;
        });
    }


    // ------------------------------------------------------------------
    // FIELD SECTION VISIBILITY
    // Show only the sections relevant to the selected product type.
    // ------------------------------------------------------------------

    var typeSelect    = document.getElementById('product_type');
    var headyFields   = document.querySelector('.admin-fields-heady');
    var prodoFields   = document.querySelector('.admin-fields-prodo');
    var vapeFields    = document.querySelector('.admin-fields-vape');

    function updateFieldVisibility() {
        if (!typeSelect) { return; }
        var type = typeSelect.value;
        if (headyFields) {
            headyFields.style.display = type === 'heady' ? '' : 'none';
        }
        if (prodoFields) {
            prodoFields.style.display = type === 'prodo' ? '' : 'none';
        }
        if (vapeFields) {
            vapeFields.style.display = type === 'vape'  ? '' : 'none';
        }
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', updateFieldVisibility);
        updateFieldVisibility();
    }

});
