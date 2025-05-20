class PreviewRenderBox {
  /** @type { HTMLElement | null } */
  #heading = null;
  /** @type { HTMLElement } */
  #element;
  constructor(headingName = null) {
    if (headingName) {
      this.#heading = document.createElement("h2");
      this.#heading.textContent = headingName;
    }
    this.#element = document.createElement("div");
    this.#element.id = "";
  }

  /**
   * @param {string} newHtml
   */
  updateInnerHtml(newHtml) {
    if (newHtml === "") {
      this.#element.innerHTML = '<div class="muted">(no content)</div>';
    } else {
      this.#element.innerHTML = newHtml;
      MathJax.typeset([this.#element]);
    }
  }

  getBody() {
    return this.#element;
  }

  delete() {
    this.#element.remove();
    this.#heading?.remove?.();
  }

  hide() {
    if (this.#heading) {
      this.#heading.style.display = "none";
    }
    this.#element.style.display = "none";
  }

  show() {
    if (this.#heading) {
      this.#heading.style.display = "";
    }
    this.#element.style.display = "";
  }

  getElements() {
    if (this.#heading) {
      return [this.#heading, this.#element];
    } else {
      return [this.#element];
    }
  }
}

export class PreviewRenderer {
  /** @type { HTMLElement } */
  #box = null;
  /** @type { Map<string, PreviewRenderBox> } */
  #subBoxes = new Map();
  constructor() {}

  /**
   * @param {HTMLElement} element
   */
  attachBox(element) {
    this.#box = element;
  }

  removeBox(id) {
    this.getPreviewBox(id).delete();
  }

  /**
   * @param {string} id
   * @param {string} headingName
   */

  addPreviewBox(id, headingName) {
    const p = new PreviewRenderBox(headingName);
    this.#subBoxes.set(id, p);
    this.#box.append(...p.getElements());
  }
  /**
   * @param {string} id
   * @returns {PreviewRenderBox | undefined}
   */
  getPreviewBox(id) {
    return this.#subBoxes.get(id);
  }
}
