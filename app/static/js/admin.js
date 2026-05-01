/**
 * admin.js
 *
 * Admin product form:
 *   - Slug auto-generation from name (new products only)
 *   - Show/hide type-specific field sections based on product_type
 *   - Display-order reference panel keyed by subcategory
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

    var typeSelect  = document.getElementById('product_type');
    var headyFields = document.querySelector('.admin-fields-heady');
    var prodoFields = document.querySelector('.admin-fields-prodo');
    var vapeFields  = document.querySelector('.admin-fields-vape');

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
            vapeFields.style.display = (type === 'vape' || type === 'tool') ? '' : 'none';
        }
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', updateFieldVisibility);
        updateFieldVisibility();
    }


    // ------------------------------------------------------------------
    // DISPLAY ORDER REFERENCE PANEL
    // Heady products have no subcategory — their panel key is 'heady'.
    // All other types: show the panel matching the selected subcategory.
    // If no subcategory is selected, hide all panels.
    // ------------------------------------------------------------------

    var subcatSelect = document.getElementById('subcategory');

    function updateRefPanel() {
        if (!typeSelect) { return; }
        var type   = typeSelect.value;
        var subcat = subcatSelect ? subcatSelect.value : '';
        var key    = (type === 'heady') ? 'heady' : subcat;

        document.querySelectorAll('.admin-order-reference').forEach(function (panel) {
            var panelKey = panel.getAttribute('data-ref-subcat');
            panel.hidden = !key || (panelKey !== key);
        });
    }

    if (typeSelect) {
        typeSelect.addEventListener('change', updateRefPanel);
    }
    if (subcatSelect) {
        subcatSelect.addEventListener('change', updateRefPanel);
    }
    updateRefPanel();


    // ------------------------------------------------------------------
    // FEATURED ARTIST ORDER — gray out when Featured Artist is unchecked
    // ------------------------------------------------------------------

    var featuredCheckbox   = document.querySelector('input[name="is_featured"]');
    var featuredOrderInput = document.getElementById('featured_order');

    if (featuredCheckbox && featuredOrderInput) {
        var featuredOrderWrap = featuredOrderInput.closest('.admin-featured-order');

        function syncFeaturedOrder() {
            var enabled = featuredCheckbox.checked;
            featuredOrderInput.disabled = !enabled;
            if (featuredOrderWrap) {
                featuredOrderWrap.classList.toggle('admin-featured-order--disabled', !enabled);
            }
        }

        syncFeaturedOrder();
        featuredCheckbox.addEventListener('change', syncFeaturedOrder);
    }

});
