// products/static/products/js/product_form.js

function initProductForm({ $ = window.$ } = {}) {
  $("#new-image")
    .off("change.productFormImage")
    .on("change.productFormImage", function () {
      const file = $("#new-image")[0]?.files?.[0];

      if (file && file.name) {
        $("#filename").text(`Image will be set to: ${file.name}`);
      } else {
        $("#filename").text("");
      }
    });
}

window.ProductForm = { initProductForm };

if (typeof module !== "undefined") {
  module.exports = { initProductForm };
}
