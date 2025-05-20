export function $(query, subject) {
  return (subject ?? document).querySelector(query);
}

export function $$(query, subject) {
  return (subject ?? document).querySelectorAll(query);
}
