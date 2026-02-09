// products/static/products/js/product.js

function initProductPage({
  $ = window.$,
  scrollToFn = (x, y) => window.scrollTo(x, y),
  replaceLocationFn = (url) => window.location.replace(url),
} = {}) {
  // Back to top
  $(".btt-link")
    .off("click.productsBtt")
    .on("click.productsBtt", function (e) {
      e.preventDefault?.();
      scrollToFn(0, 0);
    });

  // Sort selector
  $("#sort-selector")
    .off("change.productsSort")
    .on("change.productsSort", function () {
      const selector = $(this);
      const currentUrl = new URL(window.location.href);
      const selectedVal = selector.val();

      if (selectedVal !== "reset") {
        const [sort, direction] = selectedVal.split("_");
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
      } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
      }

      replaceLocationFn(currentUrl.toString());
    });
}

window.ProductPage = { initProductPage };

if (typeof module !== "undefined") {
  module.exports = { initProductPage };
}
