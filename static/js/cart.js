/* global $, window */

function initBackToTop() {
  $(".btt-link").on("click", function (e) {
    e.preventDefault();
    window.scrollTo(0, 0);
  });
}

function initRemoveItem(reloadFn = () => window.location.reload()) {
  $(".remove-item").on("click", function (e) {
    e.preventDefault();

    const itemId = $(this).data("item-id");
    const url = `/cart/remove/${itemId}/`;
    const csrfToken = window.CSRF_TOKEN;

    $.post(url, { csrfmiddlewaretoken: csrfToken }).done(function () {
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
module.exports = {
  initCartPage,
  initBackToTop,
  initRemoveItem,
};
