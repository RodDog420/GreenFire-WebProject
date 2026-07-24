/**
 * artist.js
 *
 * Handles Featured Artist page portrait gallery interactions:
 *   - Thumbnail gallery: clicking a thumb swaps the primary image
 *   - Lightbox: full-screen image viewer, opens on main image click
 *       Keyboard: Escape closes, ArrowLeft/ArrowRight navigates
 *       Touch: swipe left/right navigates
 *
 * No inline scripts anywhere on this page. CSP-safe: no eval, no
 * innerHTML, no dynamic script creation.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ------------------------------------------------------------------
    // THUMBNAIL GALLERY
    // Clicking a thumbnail updates the primary image src and alt.
    // The first thumbnail (primary image) is marked active on load.
    // ------------------------------------------------------------------

    var mainImg = document.getElementById('artist-portrait-main');
    var thumbs  = document.querySelectorAll('.artist-bio__portrait-thumb-btn');

    if (mainImg && thumbs.length) {
        thumbs.forEach(function (thumb) {
            thumb.addEventListener('click', function () {
                var src = thumb.getAttribute('data-src');
                var alt = thumb.getAttribute('data-alt');
                if (src) { mainImg.src = src; }
                if (alt) { mainImg.alt = alt; }
                thumbs.forEach(function (t) {
                    t.classList.remove('artist-bio__portrait-thumb-btn--active');
                    t.setAttribute('aria-pressed', 'false');
                });
                thumb.classList.add('artist-bio__portrait-thumb-btn--active');
                thumb.setAttribute('aria-pressed', 'true');
            });
        });
    }


    // ------------------------------------------------------------------
    // LIGHTBOX
    // Opens on click of the main image wrapper.
    // Image array built from thumbnail data attributes.
    // ------------------------------------------------------------------

    var imgWrap        = document.getElementById('artist-portrait-wrap');
    var lightbox        = document.getElementById('artist-lightbox');
    var lbImgWrap       = document.getElementById('artist-lightbox-img-wrap');
    var lbImg           = document.getElementById('artist-lightbox-img');
    var lbClose         = document.getElementById('artist-lightbox-close');
    var lbPrev          = document.getElementById('artist-lightbox-prev');
    var lbNext          = document.getElementById('artist-lightbox-next');
    var lbCounter       = document.getElementById('artist-lightbox-counter');
    var lbCurrentIndex  = 0;

    if (lightbox && lbImg && lbImgWrap && imgWrap && mainImg) {

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
            lightbox.classList.remove('artist-lightbox--zoomed');
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

        function getActiveIndex() {
            var active = 0;
            thumbs.forEach(function (thumb, i) {
                if (thumb.classList.contains(
                        'artist-bio__portrait-thumb-btn--active')) {
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
                if (!lightbox.classList.contains('artist-lightbox--zoomed')) {
                    lightbox.classList.add('artist-lightbox--zoomed');
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
                if (!lightbox.classList.contains('artist-lightbox--zoomed')) {
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

        // Close on backdrop click
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
            if (lightbox.classList.contains('artist-lightbox--zoomed')) {
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

});
