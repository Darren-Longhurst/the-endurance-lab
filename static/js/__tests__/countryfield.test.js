// static/js/__tests__/countryfield.test.js

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const $ = require("jquery");

function runScriptInIsolatedContext(absPath, sandbox) {
  const code = fs.readFileSync(absPath, "utf8");
  const context = vm.createContext(sandbox);
  vm.runInContext(code, context, { filename: absPath });
}

describe("countryfield.js", () => {
  const COUNTRYFIELD_ABS = path.resolve(
    process.cwd(),
    "profiles/static/profiles/js/countryfield.js"
  );

  beforeEach(() => {
    // set up DOM + jQuery
    global.$ = $;

    document.body.innerHTML = `
      <select id="id_default_country">
        <option value="">---</option>
        <option value="GB">United Kingdom</option>
      </select>
    `;
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("on load with empty value, it sets placeholder grey", () => {
    runScriptInIsolatedContext(COUNTRYFIELD_ABS, {
      window,
      document,
      $,
      console,
    });

    expect($("#id_default_country").css("color")).toBe("rgb(170, 183, 196)");
  });

  test("on change to a country, it sets black", () => {
    runScriptInIsolatedContext(COUNTRYFIELD_ABS, {
      window,
      document,
      $,
      console,
    });

    $("#id_default_country").val("GB").trigger("change");
    expect($("#id_default_country").css("color")).toBe("rgb(0, 0, 0)");
  });

  test("on change back to empty, it sets placeholder grey", () => {
    runScriptInIsolatedContext(COUNTRYFIELD_ABS, {
      window,
      document,
      $,
      console,
    });

    $("#id_default_country").val("GB").trigger("change");
    $("#id_default_country").val("").trigger("change");
    expect($("#id_default_country").css("color")).toBe("rgb(170, 183, 196)");
  });
});
