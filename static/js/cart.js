/* global $, window */

function initBackToTop() {
  $(".btt-link").on("click", function (e) {
    e.preventDefault();
    window.scrollTo(0, 0);
  });
}

function initRemoveItem(reloadFn = () => window.location.reload()) {
  $(".remove-item").on("click", function () {
    const itemId = $(this).data("item-id"); // "19_20"
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    const url = `/cart/remove/${itemId}/`;

    $.post(url, { csrfmiddlewaretoken: csrfToken })
      .done(function () {
        reloadFn();
      })
      .fail(function () {
        reloadFn();
      });
  });
}

function initCartPage() {
  if (typeof $ === "undefined") return; // safety if jquery isn't loaded
  initBackToTop();
  initRemoveItem();
}

// Auto-init when loaded in browser
if (typeof window !== "undefined") {
  initCartPage();
}

// Export for Jest tests
if (typeof module !== "undefined") {
  module.exports = {
    initCartPage,
    initBackToTop,
    initRemoveItem,
  };
}
