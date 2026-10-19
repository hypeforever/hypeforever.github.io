// Photo gallery lightbox (PhotoSwipe 5) for the album pages.
// Each thumbnail link (.photo-thumb) points to the full image and carries its
// size in data-pswp-width/-height. Without JavaScript the link opens the image.
// The CSS is included in _layouts/album.html (same version).
import PhotoSwipeLightbox from 'https://cdnjs.cloudflare.com/ajax/libs/photoswipe/5.4.4/photoswipe-lightbox.esm.min.js';

const lightbox = new PhotoSwipeLightbox({
  gallery: '.photo-grid',
  children: '.photo-thumb',
  pswpModule: () => import('https://cdnjs.cloudflare.com/ajax/libs/photoswipe/5.4.4/photoswipe.esm.min.js'),
  bgOpacity: 0.9,
  // Allow zooming in far enough to read the magazine scans
  secondaryZoomLevel: 2,
  maxZoomLevel: 4,
});

// Caption at the bottom: title and description from below the thumbnail
lightbox.on('uiRegister', () => {
  lightbox.pswp.ui.registerElement({
    name: 'caption',
    order: 9,
    isButton: false,
    appendTo: 'root',
    onInit: (el, pswp) => {
      pswp.on('change', () => {
        const caption = pswp.currSlide.data.element
          ?.closest('.photo-card')
          ?.querySelector('.photo-caption');
        el.innerHTML = caption ? caption.innerHTML : '';
        el.hidden = !caption;
      });
    },
  });
});

lightbox.init();
