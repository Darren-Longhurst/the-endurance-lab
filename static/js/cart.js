/* global $, window */

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split("; ") : [];
  for (let i = 0; i < cookies.length; i++) {
    const [key, ...rest] = cookies[i].split("=");
    if (key === name) return decodeURIComponent(rest.join("="));
  }
  return null;
}

function initBackToTop() {
  $(".btt-link").on("click", function (e) {
    e.preventDefault();
    window.scrollTo(0, 0);
  });
}

function initRemoveItem(reloadFn = () => window.location.reload()) {
  $(".remove-item").on("click", function () {
    const itemId = $(this).data("item-id");
    const url = `/cart/remove/${itemId}/`;
    const csrfToken = getCookie("csrftoken");

    $.ajax({
      url,
      type: "POST",
      headers: { "X-CSRFToken": csrfToken },
    })
      .done(() => reloadFn())
      .fail(() => reloadFn());
  });
}

function initCartPage() {
  if (typeof $ === "undefined") return;
  initBackToTop();
  initRemoveItem();
}

if (typeof window !== "undefined") initCartPage();

module.exports = { initCartPage, initBackToTop, initRemoveItem };
