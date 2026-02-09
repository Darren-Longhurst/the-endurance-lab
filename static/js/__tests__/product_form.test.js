// static/js/__tests__/product_form.test.js

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const $ = require("jquery");

function runScriptInIsolatedContext(absPath, sandbox) {
  const code = fs.readFileSync(absPath, "utf8");
  const context = vm.createContext(sandbox);
  vm.runInContext(code, context, { filename: absPath });
}

describe("product form JS (add/edit)", () => {
  const FORM_JS_ABS = path.resolve(
    process.cwd(),
    "products/static/products/js/product_form.js"
  );

  beforeEach(() => {
    global.$ = $;

    document.body.innerHTML = `
      <input id="new-image" type="file" />
      <p id="filename"></p>
    `;
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("shows filename when a file is selected", () => {
    runScriptInIsolatedContext(FORM_JS_ABS, {
      window,
      document,
      $,
      console,
      module: undefined,
    });

    window.ProductForm.initProductForm({ $ });

    const input = $("#new-image")[0];
    Object.defineProperty(input, "files", {
      configurable: true,
      value: [{ name: "edit-image.png" }],
    });

    $("#new-image").trigger("change");

    expect($("#filename").text()).toBe("Image will be set to: edit-image.png");
  });

  test("clears filename if no file is present", () => {
    runScriptInIsolatedContext(FORM_JS_ABS, {
      window,
      document,
      $,
      console,
      module: undefined,
    });

    window.ProductForm.initProductForm({ $ });

    const input = $("#new-image")[0];
    Object.defineProperty(input, "files", {
      configurable: true,
      value: [],
    });

    $("#new-image").trigger("change");

    expect($("#filename").text()).toBe("");
  });
});
