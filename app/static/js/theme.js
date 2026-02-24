/**
 * JonesHQ theme switcher
 * Stores preference in localStorage and applies it via data-bs-theme on <html>.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'jhq-theme';

  function resolvedTheme(preference) {
    if (preference === 'auto') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return preference;
  }

  function applyTheme(preference) {
    document.documentElement.setAttribute(
      'data-bs-theme',
      resolvedTheme(preference)
    );
    updateActiveIndicator(preference);
  }

  function updateActiveIndicator(current) {
    // Mark the active dropdown item with a checkmark icon
    document.querySelectorAll('[onclick^="setTheme"]').forEach(function (el) {
      var match = el.getAttribute('onclick').match(/setTheme\('(\w+)'\)/);
      if (!match) return;
      var icon = el.querySelector('.bi');
      if (match[1] === current) {
        el.classList.add('active');
        if (icon) icon.classList.add('bi-check2');
      } else {
        el.classList.remove('active');
        if (icon) icon.classList.remove('bi-check2');
      }
    });
  }

  // Exposed globally so onclick handlers work
  window.setTheme = function (preference) {
    localStorage.setItem(STORAGE_KEY, preference);
    applyTheme(preference);
  };

  // Apply on load (theme was set pre-paint in base.html, just update indicators)
  document.addEventListener('DOMContentLoaded', function () {
    var saved = localStorage.getItem(STORAGE_KEY) || 'dark';
    updateActiveIndicator(saved);
  });

  // React to OS preference changes when set to 'auto'
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
    var saved = localStorage.getItem(STORAGE_KEY) || 'dark';
    if (saved === 'auto') applyTheme('auto');
  });
})();
