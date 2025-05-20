import { Field } from "./fields.mjs";

export class FormEditor {
  /** @type {Map<string, Field>} */
  #fields = new Map();
  /** @type { HTMLFormElement } */
  _form = null;
  /** @type { boolean } */
  #rigged = false;
  /** @type { Map<string,Array<(e:FormEditor) => ()>>} */
  #fieldDeleteHandlers = new Map();
  /** @type { Array<(formEditor: FormEditor,name:string) => ()>}  */
  #fieldCreateHandlers = [];

  /**
   * @param {HTMLFormElement} form  */
  attachForm(form) {
    if (this._form != null) {
      throw new Error("Already attached");
    }
    this._form = form;
  }

  /** @param {string} name  */
  /** @returns {Field} */
  getField(name) {
    return this.#fields.get(name);
  }

  /**
   * @param {string} name
   * @param {Field} field
   * @returns {Field} the field you passed. Used for chaining.
   */
  addField(name, field) {
    console.assert(field instanceof Field);

    console.log(`ADDING FIELD "${name}" Type ${field.constructor.name}`);
    if (this.#fields.has(name)) {
      throw new Error(`Attempted to add field that already exists: ${name}`);
    } else {
      this.#fields.set(name, field);
      for (const handler of this.#fieldCreateHandlers) {
        handler(this, name);
      }
      return field;
    }
  }

  deleteField(name) {
    if (this.#fields.has(name)) {
      if (this.#fieldDeleteHandlers.has(name)) {
        for (const handler of this.#fieldDeleteHandlers.get(name)) {
          handler(this);
        }
        this.#fieldDeleteHandlers.set(name, []);
      }
      console.log(`DELETING FIELD "${name}"`);
      let field = this.getField(name);
      field.delete({ removeDom: true });
      this.#fields.delete(name);
    } else {
      throw new Error(`Attempted to delete field that does not exist: ${name}`);
    }
  }

  addFieldDeleteEvent(name, handler) {
    if (this.#fields.has(name)) {
      if (this.#fieldDeleteHandlers.has(name)) {
        this.#fieldDeleteHandlers.get(name).push(handler);
      } else {
        this.#fieldDeleteHandlers.set(name, [handler]);
      }
    } else {
      throw new Error(
        `Attempted to add field delete handler to field that does not exist; ${name}`
      );
    }
  }

  /**
   *
   * @param {(formEditor: FormEditor,name:string) => ()} handler
   */
  addFieldCreateEvent(handler) {
    if (this.#fieldCreateHandlers.includes(handler)) {
      throw new Error("Attempted to double-add field create handler");
    }
    this.#fieldCreateHandlers.push(handler);
  }

  rigFields() {
    if (this.#rigged) {
      throw new Error("Already rigged");
    }
    for (const [name, field] of this.#fields.entries()) {
      if (!field.isRigged()) {
        field.rig(this);
      }
    }
  }

  /**
   *
   * @returns {MapIterator<string,Field>}
   */
  fields() {
    return this.#fields.entries();
  }
}
