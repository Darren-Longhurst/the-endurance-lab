// static/js/__tests__/product.test.js

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const $ = require("jquery");

function runScriptInIsolatedContext(absPath, sandbox) {
  const code = fs.readFileSync(absPath, "utf8");
  const context = vm.createContext(sandbox);
  vm.runInContext(code, context, { filename: absPath });
  return context;
}

describe("products page JS", () => {
  const PRODUCT_JS_ABS = path.resolve(
    process.cwd(),
    "products/static/products/js/products.js"
  );

  beforeEach(() => {
    global.$ = $;

    document.body.innerHTML = `
      <a class="btt-link"></a>
      <select id="sort-selector">
        <option value="reset">reset</option>
        <option value="price_asc">price_asc</option>
      </select>
    `;

    // Ensure a predictable URL
    window.history.pushState({}, "", "http://localhost/products/");
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("clicking .btt-link scrolls to top", () => {
    const scrollToMock = jest.fn();

    const ctx = runScriptInIsolatedContext(PRODUCT_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    // script attaches to window
    window.ProductPage.initProductPage({ $, scrollToFn: scrollToMock });

    $(".btt-link").trigger("click");
    expect(scrollToMock).toHaveBeenCalledWith(0, 0);
  });

  test("changing sort updates URL via replace", () => {
    const replaceMock = jest.fn();

    runScriptInIsolatedContext(PRODUCT_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    window.ProductPage.initProductPage({ $, replaceLocationFn: replaceMock });

    $("#sort-selector").val("price_asc").trigger("change");

    expect(replaceMock).toHaveBeenCalledTimes(1);
    const calledWith = replaceMock.mock.calls[0][0];
    expect(calledWith).toContain("sort=price");
    expect(calledWith).toContain("direction=asc");
  });

  test("reset removes sort params via replace", () => {
    const replaceMock = jest.fn();

    window.history.pushState(
      {},
      "",
      "http://localhost/products/?sort=name&direction=desc"
    );

    runScriptInIsolatedContext(PRODUCT_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    window.ProductPage.initProductPage({ $, replaceLocationFn: replaceMock });

    $("#sort-selector").val("reset").trigger("change");

    const calledWith = replaceMock.mock.calls[0][0];
    expect(calledWith).not.toContain("sort=");
    expect(calledWith).not.toContain("direction=");
  });
});
