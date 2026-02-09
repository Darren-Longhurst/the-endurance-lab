// static/js/__tests__/cart.test.js

const $ = require("jquery");
const cart = require("../cart");

describe("cart.js", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <a class="btt-link"></a>
      <a class="remove-item" data-item-id="123"></a>
    `;

    global.$ = $;
    window.CSRF_TOKEN = "abc123";

    $.post = jest.fn(() => ({
      done: (cb) => cb(),
    }));
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("clicking .btt-link scrolls to top", () => {
    window.scrollTo = jest.fn();

    cart.initBackToTop();
    $(".btt-link").trigger("click");

    expect(window.scrollTo).toHaveBeenCalledWith(0, 0);
  });

  test("clicking .remove-item posts to correct URL and reloads page", () => {
    const reloadMock = jest.fn();

    cart.initRemoveItem(reloadMock);
    $(".remove-item").trigger("click");

    expect($.post).toHaveBeenCalledWith("/cart/remove/123/", {
      csrfmiddlewaretoken: "abc123",
    });

    expect(reloadMock).toHaveBeenCalled();
  });
});
