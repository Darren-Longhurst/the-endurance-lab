// static/js/__tests__/stripe_elements.test.js

const fs = require("fs");
const path = require("path");
const vm = require("vm");
const $ = require("jquery");

function runScriptInIsolatedContext(absPath, sandbox) {
  const code = fs.readFileSync(absPath, "utf8");
  const context = vm.createContext(sandbox);
  vm.runInContext(code, context, { filename: absPath });
}

async function flushPromises() {
  await Promise.resolve();
  await Promise.resolve();
  await Promise.resolve();
}

function wireFormFields(form) {
  // jsdom doesn't reliably map form controls to form.<name>
  form.full_name = document.getElementById("full_name");
  form.phone_number = document.getElementById("phone_number");
  form.email = document.getElementById("email");
  form.street_address1 = document.getElementById("street_address1");
  form.street_address2 = document.getElementById("street_address2");
  form.town_or_city = document.getElementById("town_or_city");
  form.country = document.getElementById("country");
  form.county = document.getElementById("county");
  form.postcode = document.getElementById("postcode");
}

describe("stripe_elements.js", () => {
  const STRIPE_JS_ABS = path.resolve(
    process.cwd(),
    "checkout/static/checkout/js/stripe_elements.js"
  );

  beforeEach(() => {
    global.$ = $;

    // Polyfill $.trim for test environment (some jQuery builds don't expose it)
    if (typeof $.trim !== "function") {
      $.trim = (s) => String(s ?? "").trim();
    }

    document.body.innerHTML = `
      <div id="id_stripe_public_key">"pk_test_123"</div>
      <div id="id_client_secret">"cs_test_456"</div>

      <div id="card-element"></div>
      <div id="card-errors"></div>

      <div id="loading-overlay" style="display:none"></div>

      <form id="payment-form">
        <input name="csrfmiddlewaretoken" value="abc123" />
        <input id="id-save-info" checked="checked" />

        <input id="full_name" name="full_name" value="Test User" />
        <input id="phone_number" name="phone_number" value="0123456789" />
        <input id="email" name="email" value="test@example.com" />

        <input id="street_address1" name="street_address1" value="1 Test Street" />
        <input id="street_address2" name="street_address2" value="" />
        <input id="town_or_city" name="town_or_city" value="London" />
        <input id="country" name="country" value="GB" />
        <input id="county" name="county" value="Greater London" />
        <input id="postcode" name="postcode" value="SW1A 1AA" />

        <button id="submit-button" type="submit">Pay</button>
      </form>
    `;

    // jQuery fx used in script; stub to avoid animation issues
    $.fn.fadeToggle = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("mounts Stripe card element and wires change handler", () => {
    const cardMock = {
      mount: jest.fn(),
      addEventListener: jest.fn(),
      update: jest.fn(),
    };

    const elementsMock = { create: jest.fn(() => cardMock) };

    const stripeObjMock = {
      elements: () => elementsMock,
      confirmCardPayment: jest.fn(() =>
        Promise.resolve({ paymentIntent: { status: "succeeded" } })
      ),
    };

    const StripeCtorMock = jest.fn(() => stripeObjMock);

    runScriptInIsolatedContext(STRIPE_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    window.StripeElementsPage.initStripeElements({
      $,
      StripeCtor: StripeCtorMock,
      locationRef: { reload: jest.fn() },
    });

    expect(StripeCtorMock).toHaveBeenCalledWith("pk_test_123");
    expect(elementsMock.create).toHaveBeenCalledWith("card", expect.any(Object));
    expect(cardMock.mount).toHaveBeenCalledWith("#card-element");
    expect(cardMock.addEventListener).toHaveBeenCalledWith("change", expect.any(Function));
  });

  test("on submit: posts cache data and calls confirmCardPayment, then submits form", async () => {
    // Mock $.post success
    $.post = jest.fn(() => ({
      done: (cb) => {
        cb();
        return { fail: () => {} };
      },
      fail: () => {},
    }));

    const cardMock = {
      mount: jest.fn(),
      addEventListener: jest.fn(),
      update: jest.fn(),
    };

    const elementsMock = { create: jest.fn(() => cardMock) };

    const confirmCardPaymentMock = jest.fn(() =>
      Promise.resolve({ paymentIntent: { status: "succeeded" } })
    );

    const stripeObjMock = {
      elements: () => elementsMock,
      confirmCardPayment: confirmCardPaymentMock,
    };

    const StripeCtorMock = jest.fn(() => stripeObjMock);

    const form = document.getElementById("payment-form");
    form.submit = jest.fn();
    wireFormFields(form);

    runScriptInIsolatedContext(STRIPE_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    window.StripeElementsPage.initStripeElements({
      $,
      StripeCtor: StripeCtorMock,
      locationRef: { reload: jest.fn() },
    });

    form.dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));

    await flushPromises();

    expect($.post).toHaveBeenCalledWith("/checkout/cache_checkout_data/", {
      csrfmiddlewaretoken: "abc123",
      client_secret: "cs_test_456",
      save_info: true,
    });

    expect(confirmCardPaymentMock).toHaveBeenCalledWith(
      "cs_test_456",
      expect.objectContaining({
        payment_method: expect.any(Object),
        shipping: expect.any(Object),
      })
    );

    expect(form.submit).toHaveBeenCalled();
  });

  test("if cache post fails, it reloads the page", async () => {
    const reloadMock = jest.fn();

    // Make $.post fail path run
    $.post = jest.fn(() => ({
      done: () => ({
        fail: (cb) => cb(),
      }),
      fail: (cb) => cb(),
    }));

    const cardMock = {
      mount: jest.fn(),
      addEventListener: jest.fn(),
      update: jest.fn(),
    };

    const elementsMock = { create: jest.fn(() => cardMock) };
    const stripeObjMock = { elements: () => elementsMock, confirmCardPayment: jest.fn() };
    const StripeCtorMock = jest.fn(() => stripeObjMock);

    const form = document.getElementById("payment-form");
    form.submit = jest.fn();
    wireFormFields(form);

    runScriptInIsolatedContext(STRIPE_JS_ABS, {
      window,
      document,
      $,
      console,
      URL,
      module: undefined,
    });

    window.StripeElementsPage.initStripeElements({
      $,
      StripeCtor: StripeCtorMock,
      locationRef: { reload: reloadMock },
    });

    form.dispatchEvent(new window.Event("submit", { bubbles: true, cancelable: true }));

    await flushPromises();

    expect(reloadMock).toHaveBeenCalled();
  });
});
