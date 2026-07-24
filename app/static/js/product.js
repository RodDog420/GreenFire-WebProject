/**
 * product.js
 *
 * Handles product detail page interactions:
 *   - Thumbnail gallery: clicking a thumb swaps the primary image
 *   - Image zoom: lens box on image, zoomed panel beside it (desktop only)
 *   - Lightbox: full-screen image viewer, opens on main image click
 *       Keyboard: Escape closes, ArrowLeft/ArrowRight navigates
 *       Touch: swipe left/right navigates
 *   - Share button: copies page URL to clipboard
 *
 * No inline scripts anywhere on this page. All server data passed via
 * data- attributes. CSP-safe: no eval, no innerHTML, no dynamic script
 * creation. element.style property manipulation is not governed by
 * CSP style-src and is permitted without unsafe-inline.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------------
    // THUMBNAIL GALLERY
    // Clicking a thumbnail updates the primary image src and alt.
    // The first thumbnail (primary image) is marked active on load.
    // ------------------------------------------------------------------

    var mainImg = document.getElementById('product-main-img');
    var thumbs  = document.querySelectorAll('.product-thumb');

    if (mainImg && thumbs.length) {
        thumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                var src = thumb.getAttribute('data-src');
                var alt = thumb.getAttribute('data-alt');
                if (src) { mainImg.src = src; }
                if (alt) { mainImg.alt = alt; }
                thumbs.forEach(function (t) {
                    t.classList.remove('product-thumb--active');
                    t.setAttribute('aria-pressed', 'false');
                });
                thumb.classList.add('product-thumb--active');
                thumb.setAttribute('aria-pressed', 'true');
            });
        });
    }


    // ------------------------------------------------------------------
    // IMAGE ZOOM — desktop only (min-width: 64rem)
    //
    // Lens box tracks the cursor over the primary image.
    // Zoom panel shows the magnified region to the right of the image.
    // On mobile/tablet the lens and panel are hidden via CSS display:none
    // and the JS bails out early via matchMedia check.
    // ------------------------------------------------------------------

    var imgWrap   = document.getElementById('product-img-wrap');
    var zoomPanel = document.getElementById('product-zoom-panel');
    var zoomLens  = document.getElementById('product-zoom-lens');

    if (imgWrap && zoomPanel && zoomLens && mainImg) {

        var desktopMq = window.matchMedia('(min-width: 64rem)');

        function moveZoom(e) {
            if (!desktopMq.matches) { return; }

            var rect   = imgWrap.getBoundingClientRect();
            var lensW  = zoomLens.offsetWidth;
            var lensH  = zoomLens.offsetHeight;
            var panelW = zoomPanel.offsetWidth;
            var panelH = zoomPanel.offsetHeight;

            var x = e.clientX - rect.left  - (lensW / 2);
            var y = e.clientY - rect.top   - (lensH / 2);

            x = Math.max(0, Math.min(x, rect.width  - lensW));
            y = Math.max(0, Math.min(y, rect.height - lensH));

            zoomLens.style.left = x + 'px';
            zoomLens.style.top  = y + 'px';

            // Single ratio keeps both axes uniform — prevents distortion.
            // Panel width / lens width drives the zoom level.
            var ratio = panelW / lensW;

            zoomPanel.style.backgroundImage =
                'url("' + mainImg.src + '")';
            zoomPanel.style.backgroundSize =
                (rect.width  * ratio) + 'px ' +
                (rect.height * ratio) + 'px';
            zoomPanel.style.backgroundPosition =
                '-' + (x * ratio) + 'px ' +
                '-' + (y * ratio) + 'px';

            zoomLens.style.display  = 'block';
            zoomPanel.style.display = 'block';
        }

        function hideZoom() {
            zoomLens.style.display  = 'none';
            zoomPanel.style.display = 'none';
        }

        imgWrap.addEventListener('mousemove',  moveZoom);
        imgWrap.addEventListener('mouseleave', hideZoom);
    }


    // ------------------------------------------------------------------
    // LIGHTBOX
    // Opens on click of the main image wrapper.
    // Image array built from thumbnail data attributes — falls back to
    // main image alone when no additional images exist.
    // ------------------------------------------------------------------

    var lightbox       = document.getElementById('product-lightbox');
    var lbImg          = document.getElementById('lightbox-img');
    var lbImgWrap      = document.getElementById('lightbox-img-wrap');
    var lbClose        = document.getElementById('lightbox-close');
    var lbPrev         = document.getElementById('lightbox-prev');
    var lbNext         = document.getElementById('lightbox-next');
    var lbCounter      = document.getElementById('lightbox-counter');
    var lbCurrentIndex = 0;

    if (lightbox && lbImg && imgWrap &&
        mainImg && mainImg.tagName === 'IMG') {

        // Build image array from thumbs if they exist, else main image only.
        var lbImages = [];
        if (thumbs.length > 0) {
            thumbs.forEach(function (thumb) {
                var src = thumb.getAttribute('data-src');
                var alt = thumb.getAttribute('data-alt') || '';
                if (src) { lbImages.push({ src: src, alt: alt }); }
            });
        } else {
            lbImages.push({ src: mainImg.src, alt: mainImg.alt });
        }

        function showLbImage(index) {
            lbImg.src = lbImages[index].src;
            lbImg.alt = lbImages[index].alt;
            if (lbCounter) {
                if (lbImages.length > 1) {
                    lbCounter.textContent = (index + 1) + ' / ' + lbImages.length;
                    lbCounter.removeAttribute('hidden');
                } else {
                    lbCounter.setAttribute('hidden', '');
                }
            }
            if (lbPrev) {
                lbPrev.style.display = index > 0 ? 'flex' : 'none';
            }
            if (lbNext) {
                lbNext.style.display =
                    index < lbImages.length - 1 ? 'flex' : 'none';
            }
        }

        function openLightbox(index) {
            lbCurrentIndex = Math.max(0, Math.min(index, lbImages.length - 1));
            showLbImage(lbCurrentIndex);
            lightbox.removeAttribute('hidden');
            document.body.style.overflow = 'hidden';
            if (lbClose) { lbClose.focus(); }
        }

        var ZOOM_MULTIPLIER = 2;

        // Sets the zoomed image to an explicit pixel size, not a CSS
        // transform: scale(). transform's visual overflow is only
        // reliably scrollable in the end (bottom/right) direction in
        // practice — the start (top/left) direction gets silently
        // truncated, cutting off part of the image no matter how it's
        // scrolled. An explicit width/height doesn't have this problem,
        // since it's real layout size, not a paint-only visual effect.
        //
        // Clearing the inline size before measuring is what keeps this
        // resize-safe: it forces the image back to its natural
        // (object-fit: contain) rendered size for that measurement, so
        // the doubled target is always derived fresh from the current
        // viewport rather than from a stale prior zoom size.
        function applyZoom() {
            lbImg.style.width = '';
            lbImg.style.height = '';
            var rect = lbImg.getBoundingClientRect();
            lbImg.style.width = (rect.width * ZOOM_MULTIPLIER) + 'px';
            lbImg.style.height = (rect.height * ZOOM_MULTIPLIER) + 'px';
        }

        function centerZoomScroll() {
            lightbox.scrollLeft =
                (lightbox.scrollWidth - lightbox.clientWidth) / 2;
            lightbox.scrollTop =
                (lightbox.scrollHeight - lightbox.clientHeight) / 2;
        }

        function resetZoom() {
            lightbox.classList.remove('lightbox--zoomed');
            lbImg.style.width = '';
            lbImg.style.height = '';
            lightbox.scrollTop = 0;
            lightbox.scrollLeft = 0;
        }

        function closeLightbox() {
            lightbox.setAttribute('hidden', '');
            resetZoom();
            document.body.style.overflow = '';
            imgWrap.focus();
        }

        function lbGoTo(index) {
            if (index < 0 || index >= lbImages.length) { return; }
            resetZoom();
            lbCurrentIndex = index;
            showLbImage(lbCurrentIndex);
        }

        // Open at whichever image is currently active in the gallery.
        imgWrap.setAttribute('tabindex', '0');
        imgWrap.setAttribute('role', 'button');
        imgWrap.setAttribute('aria-label', 'Open full-screen image viewer');

        function getActiveIndex() {
            var active = 0;
            thumbs.forEach(function (thumb, i) {
                if (thumb.classList.contains('product-thumb--active')) {
                    active = i;
                }
            });
            return active;
        }

        imgWrap.addEventListener('click', function () {
            openLightbox(getActiveIndex());
        });

        imgWrap.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openLightbox(getActiveIndex());
            }
        });

        // Click image to zoom in. Once zoomed, a click no longer zooms
        // back out — the close button already covers that, and leaving
        // click free avoids it firing after a drag-to-pan (below) ends.
        if (lbImg) {
            lbImg.addEventListener('click', function (e) {
                e.stopPropagation();
                if (!lightbox.classList.contains('lightbox--zoomed')) {
                    lightbox.classList.add('lightbox--zoomed');
                    applyZoom();
                    centerZoomScroll();
                }
            });
        }

        // Drag-to-pan while zoomed. At this zoom level the image is
        // larger than the viewport in both directions — scrollbars alone
        // are not a discoverable way to bring the rest of the piece into
        // view, so support the conventional grab-and-drag pan gesture.
        var isPanning = false;
        var panStartX = 0, panStartY = 0;
        var panScrollStartX = 0, panScrollStartY = 0;

        if (lbImg) {
            lbImg.addEventListener('mousedown', function (e) {
                if (!lightbox.classList.contains('lightbox--zoomed')) {
                    return;
                }
                isPanning = true;
                panStartX = e.clientX;
                panStartY = e.clientY;
                panScrollStartX = lightbox.scrollLeft;
                panScrollStartY = lightbox.scrollTop;
                lbImg.classList.add('lightbox__img--panning');
                e.preventDefault();
            });
        }

        document.addEventListener('mousemove', function (e) {
            if (!isPanning) { return; }
            lightbox.scrollLeft = panScrollStartX - (e.clientX - panStartX);
            lightbox.scrollTop = panScrollStartY - (e.clientY - panStartY);
        });

        document.addEventListener('mouseup', function () {
            if (!isPanning) { return; }
            isPanning = false;
            lbImg.classList.remove('lightbox__img--panning');
        });

        // Controls
        if (lbClose) { lbClose.addEventListener('click', closeLightbox); }
        if (lbPrev) {
            lbPrev.addEventListener('click', function () {
                lbGoTo(lbCurrentIndex - 1);
            });
        }
        if (lbNext) {
            lbNext.addEventListener('click', function () {
                lbGoTo(lbCurrentIndex + 1);
            });
        }

        // Close on backdrop click. lbImgWrap is included because it's
        // sized to fill the whole lightbox — without it, e.target is
        // always the wrap (or a fixed-position button above it), never
        // the lightbox element itself, so backdrop clicks would never fire.
        lightbox.addEventListener('click', function (e) {
            if (e.target === lightbox || e.target === lbImgWrap) {
                closeLightbox();
            }
        });

        // Keyboard navigation (only when lightbox is open)
        document.addEventListener('keydown', function (e) {
            if (lightbox.hasAttribute('hidden')) { return; }
            if (e.key === 'Escape')      { closeLightbox(); }
            if (e.key === 'ArrowLeft')   { lbGoTo(lbCurrentIndex - 1); }
            if (e.key === 'ArrowRight')  { lbGoTo(lbCurrentIndex + 1); }
        });

        // A resize while zoomed leaves both the pixel size and the scroll
        // centering stale relative to the new viewport — recompute both
        // fresh rather than dropping out of zoom entirely.
        window.addEventListener('resize', function () {
            if (lightbox.classList.contains('lightbox--zoomed')) {
                applyZoom();
                centerZoomScroll();
            }
        });

        // Touch swipe — 50px threshold
        var touchStartX = 0;
        lightbox.addEventListener('touchstart', function (e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        lightbox.addEventListener('touchend', function (e) {
            var delta = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(delta) > 50) {
                lbGoTo(delta > 0 ? lbCurrentIndex + 1 : lbCurrentIndex - 1);
            }
        }, { passive: true });
    }


    // ------------------------------------------------------------------
    // SHARE BUTTON
    // Copies the current page URL to the clipboard.
    // Falls back gracefully if Clipboard API is unavailable.
    // ------------------------------------------------------------------

    var shareBtn = document.getElementById('product-share-btn');

    if (shareBtn) {
        var originalLabel = shareBtn.textContent;

        shareBtn.addEventListener('click', function () {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(window.location.href)
                    .then(function () {
                        shareBtn.textContent = 'Link copied!';
                        setTimeout(function () {
                            shareBtn.textContent = originalLabel;
                        }, 2000);
                    })
                    .catch(function () {
                        shareBtn.textContent = 'Copy URL from address bar';
                        setTimeout(function () {
                            shareBtn.textContent = originalLabel;
                        }, 3000);
                    });
            } else {
                shareBtn.textContent = 'Copy URL from address bar';
                setTimeout(function () {
                    shareBtn.textContent = originalLabel;
                }, 3000);
            }
        });
    }

});
