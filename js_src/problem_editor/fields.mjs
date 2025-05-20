import { CodeEditor } from "../util/code_editor.mjs";
import { bindEditorAndFormInput } from "../util/code_editor.mjs";

/**
 * @abstract
 */
export class Field {
  #isRigged = false;
  _fireEventOnRig = true;
  /** @type { Array<(f:Field) => ()>   } */
  #eventHandlers = [];

  /**
   * DO NOT OVERRIDE
   * @param {FormEditor} editor
   */
  rig(editor) {
    this.rigOverride(editor);
    if (this._fireEventOnRig === true) {
      this.#eventHandlers.forEach((handler) => {
        handler(this);
      });
    }
    this.#isRigged = true;
  }
  /**
   * Fires when the contents of this field is updated or initially set.
   * NO NOT OVERRIDE
   * @param {(f:Field) => ()} handler
   */
  changeEvent(handler) {
    this.#eventHandlers.push(handler);
    this.changeEventOverride(handler);
  }
  /**
   * NO NOT OVERRIDE
   */
  delete({ removeDom }) {
    this.#eventHandlers = [];
    if (removeDom) {
      this.removeDom();
    }
  }

  modifyValue(callback) {
    this.setValue(callback(this.value()));
  }

  isRigged() {
    return this.#isRigged;
  }

  rigOverride() {
    throw new Error("Not implemented");
  }

  changeEventOverride(handler) {
    throw new Error("Not implemented");
  }

  removeDom() {
    throw new Error("Not implemented");
  }

  value() {
    throw new Error("Not implemented");
  }

  setValue(newValue) {
    throw new Error("Not implemented");
  }

  hide() {
    throw new Error("Not implemented");
  }
  show() {
    throw new Error("Not Implemented");
  }
}

export class CheckboxField extends Field {
  /** @type {HTMLInputElement} */
  #element;
  constructor(element) {
    super();
    this.#element = element;
  }

  value() {
    return this.#element.checked;
  }

  setValue(newValue) {
    this.#element.checked = newValue;
  }

  changeEventOverride(handler) {
    this.#element.addEventListener("change", () => handler(this));
  }

  rigOverride(editor) {}
}

export class NumberField extends Field {
  /** @type {HTMLInputElement} */
  #element;
  constructor(element) {
    super();
    this.#element = element;
  }

  value() {
    return parseInt(this.#element.value, 10);
  }

  setValue(newValue) {
    console.log(this.#element);

    this.#element.value = newValue;
  }

  changeEventOverride(handler) {
    this.#element.addEventListener("change", () => handler(this));
  }

  rigOverride(editor) {}
}

export class ButtonField extends Field {
  _fireEventOnRig = false;
  /** @type {HTMLButtonElement} */
  #element;
  constructor(element) {
    super();
    this.#element = element;
  }

  value() {
    throw new Error("value() called for button field. Buttons have no value.");
  }

  setValue(newValue) {
    throw new Error(
      "setValue() called for button field. Buttons have no value."
    );
  }

  changeEventOverride(handler) {
    this.#element.addEventListener("click", () => {
      handler(this);
    });
  }

  rigOverride(editor) {}
}

export class CodeEditorTextareaField extends Field {
  /** @type {HTMLElement} */
  #element;
  /** @type {CodeEditor} */
  #editor = new CodeEditor();
  constructor(element) {
    super();
    this.#element = element;
  }

  rigOverride(editor) {
    bindEditorAndFormInput(this.#editor, this.#element);
  }

  value() {
    return this.#editor.getText();
  }

  setValue(value) {
    this.#editor.setText(value);
  }

  changeEventOverride(handler) {
    this.#editor.changeEvent(() => {
      handler(this);
    });
  }

  removeDom() {
    let element = this.#element;
    let parent = element.parentNode;
    if ([...parent.parentNode.classList].includes("solutionWrapper")) {
      parent.parentElement.remove();
    }
    this.#editor = null;
    this.#element = null;
    element.remove();
    parent.innerHTML = "";
    element = null;
    parent = null;
  }

  hide() {
    this.#element.parentNode.style.display = "none";
  }

  show() {
    this.#element.parentNode.style.display = "";
  }
}
