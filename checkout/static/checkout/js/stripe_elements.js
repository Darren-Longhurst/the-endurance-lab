// checkout/static/checkout/js/stripe_elements.js

function initStripeElements({
  $ = window.$,
  StripeCtor = window.Stripe,
  documentRef = document,
  locationRef = window.location,
} = {}) {
  // Ensure we're on the checkout page
  const form = documentRef.getElementById("payment-form");
  const cardMount = documentRef.getElementById("card-element");
  if (!form || !cardMount) return;

  // Ensure Stripe.js is loaded
  if (typeof StripeCtor !== "function") {
    console.error(
      "Stripe.js is not loaded. Ensure <script src='https://js.stripe.com/v3/'></script> is included before stripe_elements.js"
    );
    return;
  }

  // Helper: json_script outputs JSON; parse it safely
  function readJsonScript(id) {
    const el = documentRef.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      // fallback for unexpected formatting
      return el.textContent;
    }
  }

  const stripePublicKey = readJsonScript("id_stripe_public_key");
  const clientSecret = readJsonScript("id_client_secret");

  if (!stripePublicKey || !clientSecret) {
    console.error(
      "Missing stripe keys. Check stripe_public_key/client_secret are being passed to the template and rendered via json_script."
    );
    return;
  }

  const stripe = StripeCtor(stripePublicKey);
  const elements = stripe.elements();

  const style = {
    base: {
      color: "#000",
      fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#dc3545",
      iconColor: "#dc3545",
    },
  };

  const card = elements.create("card", { style });
  card.mount("#card-element");

  // Handle realtime validation errors on the card element
  // Stripe Elements uses .on(...) but addEventListener often works too—support both.
  const changeHandler = function (event) {
    const errorDiv = documentRef.getElementById("card-errors");
    if (!errorDiv) return;

    if (event && event.error) {
      const html = `
        <span class="icon" role="alert">
          <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
      `;
      $(errorDiv).html(html);
    } else {
      errorDiv.textContent = "";
    }
  };

  if (typeof card.on === "function") {
    card.on("change", changeHandler);
  } else if (typeof card.addEventListener === "function") {
    card.addEventListener("change", changeHandler);
  }

  // Safe trim helper (avoids $.trim issues)
  const trimVal = (v) => String(v ?? "").trim();

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();

    // Lock UI
    if (card && typeof card.update === "function") {
      card.update({ disabled: true });
    }
    $("#submit-button").attr("disabled", true);

    // These rely on jQuery (fine in your real app)
    $("#payment-form").fadeToggle(100);
    $("#loading-overlay").fadeToggle(100);

    // Correct checked state
    const saveInfo = Boolean($("#id-save-info").prop("checked"));

    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    const postData = {
      csrfmiddlewaretoken: csrfToken,
      client_secret: clientSecret,
      save_info: saveInfo,
    };

    const url = "/checkout/cache_checkout_data/";

    $.post(url, postData)
      .done(function () {
        stripe
          .confirmCardPayment(clientSecret, {
            payment_method: {
              card: card,
              billing_details: {
                name: trimVal(form.full_name?.value),
                phone: trimVal(form.phone_number?.value),
                email: trimVal(form.email?.value),
                address: {
                  line1: trimVal(form.street_address1?.value),
                  line2: trimVal(form.street_address2?.value),
                  city: trimVal(form.town_or_city?.value),
                  country: trimVal(form.country?.value),
                  state: trimVal(form.county?.value),
                },
              },
            },
            shipping: {
              name: trimVal(form.full_name?.value),
              phone: trimVal(form.phone_number?.value),
              address: {
                line1: trimVal(form.street_address1?.value),
                line2: trimVal(form.street_address2?.value),
                city: trimVal(form.town_or_city?.value),
                country: trimVal(form.country?.value),
                postal_code: trimVal(form.postcode?.value),
                state: trimVal(form.county?.value),
              },
            },
          })
          .then(function (result) {
            if (result && result.error) {
              const errorDiv = documentRef.getElementById("card-errors");
              const html = `
                <span class="icon" role="alert">
                  <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
              `;
              if (errorDiv) $(errorDiv).html(html);

              $("#payment-form").fadeToggle(100);
              $("#loading-overlay").fadeToggle(100);

              if (card && typeof card.update === "function") {
                card.update({ disabled: false });
              }
              $("#submit-button").attr("disabled", false);
            } else if (
              result &&
              result.paymentIntent &&
              result.paymentIntent.status === "succeeded"
            ) {
              // In browser this works; in jsdom tests it must be mocked.
              form.submit();
            }
          });
      })
      .fail(function () {
        // just reload the page, the error will be in django messages
        locationRef.reload();
      });
  });

  // return handles for testing if needed
  return { stripe, elements, card, clientSecret, stripePublicKey };
}

window.StripeElementsPage = { initStripeElements };

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initStripeElements();
    });
  } else {
    initStripeElements();
  }
}

if (typeof module !== "undefined") {
  module.exports = { initStripeElements };
}
