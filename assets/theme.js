/* LILA (ليلى) — Theme JavaScript
   Premium Shopify store for Moroccan women
   ========================================= */

document.addEventListener('DOMContentLoaded', function() {
  initHeaderScroll();
  initMobileMenu();
  initFaqAccordion();
  initStickyAddToCart();
  initProductGallery();
  initQuantitySelector();
  initSmoothScroll();
  initLazyLoading();
  initCountdownTimer();
});

/* === HEADER SCROLL EFFECT === */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

/* === MOBILE MENU === */
function initMobileMenu() {
  const openBtn = document.querySelector('.mobile-menu-btn');
  const closeBtn = document.querySelector('.mobile-menu-close');
  const menu = document.querySelector('.mobile-menu');
  const overlay = document.querySelector('.mobile-menu-overlay');

  if (!openBtn || !menu) return;

  function openMenu() {
    menu.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (overlay) overlay.classList.add('visible');
  }

  function closeMenu() {
    menu.classList.remove('open');
    document.body.style.overflow = '';
    if (overlay) overlay.classList.remove('visible');
  }

  openBtn.addEventListener('click', openMenu);

  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay) overlay.addEventListener('click', closeMenu);

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeMenu();
  });
}

/* === FAQ ACCORDION === */
function initFaqAccordion() {
  const questions = document.querySelectorAll('.faq-question');
  questions.forEach(function(question) {
    question.addEventListener('click', function() {
      const item = this.closest('.faq-item');
      if (!item) return;
      const isActive = item.classList.contains('active');

      /* Close all */
      document.querySelectorAll('.faq-item.active').forEach(function(i) {
        i.classList.remove('active');
      });

      /* Toggle current */
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });
}

/* === STICKY ADD TO CART === */
function initStickyAddToCart() {
  const sticky = document.querySelector('.sticky-atc');
  const addBtn = document.querySelector('.product-form .btn-primary');
  if (!sticky || !addBtn) return;

  const productSection = document.querySelector('.product-showcase');
  if (!productSection) return;

  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) {
        sticky.classList.add('visible');
      } else {
        sticky.classList.remove('visible');
      }
    });
  }, { threshold: 0 });

  observer.observe(productSection);
}

/* === PRODUCT GALLERY === */
function initProductGallery() {
  const thumbs = document.querySelectorAll('.product-thumb');
  const mainImage = document.querySelector('.product-main-image img');
  if (!thumbs.length || !mainImage) return;

  thumbs.forEach(function(thumb) {
    thumb.addEventListener('click', function() {
      const src = this.getAttribute('data-image');
      if (!src) return;

      thumbs.forEach(function(t) { t.classList.remove('active'); });
      this.classList.add('active');
      mainImage.src = src;
    });
  });
}

/* === QUANTITY SELECTOR === */
function initQuantitySelector() {
  const selectors = document.querySelectorAll('.qty-selector');
  selectors.forEach(function(selector) {
    const input = selector.querySelector('.qty-input');
    const minus = selector.querySelector('.qty-btn.minus');
    const plus = selector.querySelector('.qty-btn.plus');
    if (!input) return;

    if (minus) {
      minus.addEventListener('click', function() {
        let val = parseInt(input.value) || 1;
        if (val > 1) {
          input.value = val - 1;
          triggerEvent(input, 'change');
        }
      });
    }

    if (plus) {
      plus.addEventListener('click', function() {
        let val = parseInt(input.value) || 1;
        const max = parseInt(input.getAttribute('max')) || 99;
        if (val < max) {
          input.value = val + 1;
          triggerEvent(input, 'change');
        }
      });
    }

    input.addEventListener('change', function() {
      let val = parseInt(this.value) || 1;
      const max = parseInt(this.getAttribute('max')) || 99;
      const min = parseInt(this.getAttribute('min')) || 1;
      if (val < min) this.value = min;
      if (val > max) this.value = max;
    });
  });
}

/* === SMOOTH SCROLL === */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      const headerOffset = 80;
      const elementPosition = target.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    });
  });
}

/* === LAZY LOADING === */
function initLazyLoading() {
  if ('loading' in HTMLImageElement.prototype) {
    document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {
      img.src = img.getAttribute('data-src') || img.src;
    });
  } else {
    /* Fallback */
    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.getAttribute('data-src') || img.src;
          observer.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(function(img) {
      observer.observe(img);
    });
  }
}

/* === COUNTDOWN TIMER === */
function initCountdownTimer() {
  const timers = document.querySelectorAll('[data-countdown]');
  timers.forEach(function(timer) {
    const endTime = new Date(timer.getAttribute('data-countdown')).getTime();
    if (isNaN(endTime)) return;

    function update() {
      const now = new Date().getTime();
      const diff = endTime - now;

      if (diff <= 0) {
        timer.innerHTML = '<span class="countdown-ended">Offer ended</span>';
        return;
      }

      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      timer.querySelector('.countdown-hours').textContent = String(hours).padStart(2, '0');
      timer.querySelector('.countdown-minutes').textContent = String(minutes).padStart(2, '0');
      timer.querySelector('.countdown-seconds').textContent = String(seconds).padStart(2, '0');
    }

    update();
    setInterval(update, 1000);
  });
}

/* === UTILITY: Trigger Events === */
function triggerEvent(el, type) {
  if ('createEvent' in document) {
    var e = document.createEvent('HTMLEvents');
    e.initEvent(type, false, true);
    el.dispatchEvent(e);
  } else {
    el.fireEvent('on' + type);
  }
}

/* === AJAX ADD TO CART === */
function ajaxAddToCart(variantId, quantity, callback) {
  const formData = {
    items: [{
      id: variantId,
      quantity: quantity || 1
    }]
  };

  fetch(window.lila.cartAddUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.status === 422) {
      showToast(data.description || 'Something went wrong', 'error');
      if (callback) callback(false, data);
    } else {
      updateCartCount(data.item_count || 0);
      showToast('Added to cart!', 'success');
      if (callback) callback(true, data);
    }
  })
  .catch(function(err) {
    console.error('Cart error:', err);
    showToast('Something went wrong', 'error');
    if (callback) callback(false, err);
  });
}

/* === UPDATE CART COUNT === */
function updateCartCount(count) {
  const badge = document.querySelector('.cart-count');
  if (badge) {
    badge.textContent = count || '';
  }
}

/* === TOAST === */
function showToast(message, type) {
  var toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }

  var icon = type === 'success'
    ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';

  toast.className = 'toast toast-' + type;
  toast.innerHTML = icon + '<span>' + message + '</span>';
  toast.classList.add('show');

  clearTimeout(toast._hideTimer);
  toast._hideTimer = setTimeout(function() {
    toast.classList.remove('show');
  }, 3000);
}
