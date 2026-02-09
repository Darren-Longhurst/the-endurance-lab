/* global $, window */

function initBackToTop() {
  $(".btt-link").on("click", function (e) {
    e.preventDefault();
    window.scrollTo(0, 0);
  });
}

function initRemoveItem(reloadFn = () => window.location.reload()) {
  $(".remove-item").on("click", function () {
    // e.g. id="remove_19_20" -> "19_20"
    const itemId = $(this).attr("id").replace("remove_", "");
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    const url = `/cart/remove/${itemId}/`;

    $.post(url, { csrfmiddlewaretoken: csrfToken })
      .done(reloadFn)
      .fail(reloadFn);
  });
}

function initCartPage() {
  if (typeof $ === "undefined") return;
  initBackToTop();
  initRemoveItem();
}

if (typeof window !== "undefined") {
  initCartPage();
}

module.exports = {
  initCartPage,
  initBackToTop,
  initRemoveItem,
};
