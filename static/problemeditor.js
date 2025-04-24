document.addEventListener("DOMContentLoaded", () => {
  const form = $$("#problem-form");

  for (const select of form.querySelectorAll("select")) {
    select.style.fontFamily = "sans-serif";
  }
  // FUTURE WORK: Find a select library that doesn't use JQuery.
  $("#source-box > select").select2();
  $("#category-box > select").select2();
  $("#technique-box > select").select2();
});

// Utility functions

function $$(query) {
  return document.querySelector(query);
}

function El(tag, params) {
  const el = document.createElement(tag);

  if (params?.id) {
    el.id = params.id;
  }
  if (params?.text) {
    el.textContent = params.text;
  }

  return el;
}
