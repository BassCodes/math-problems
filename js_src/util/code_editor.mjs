import { EditorView, basicSetup, minimalSetup } from "codemirror";
import { EditorSelection } from "@codemirror/state";
import { keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";

// Configuration for codemirror

const ruleAt80Columns = EditorView.theme({
  ".cm-content": {
    backgroundImage: "linear-gradient(to right, #ccc 1px, transparent 1px)",
    backgroundSize: "ch 1em",
    backgroundPosition: "80ch 0",
    backgroundRepeat: "no-repeat",
  },
});

const duplicateLine = ({ state, dispatch }) => {
  const changes = state.changeByRange((range) => {
    const line = state.doc.lineAt(range.head);
    const duplicatedText = line.text + "\n";
    return {
      changes: {
        from: line.to,
        insert: "\n" + line.text,
      },
      range: EditorSelection.cursor(range.head + duplicatedText.length),
    };
  });

  dispatch(state.update(changes, { scrollIntoView: true, userEvent: "input" }));
  return true;
};

export class CodeEditor {
  #element;
  #editor;
  #listeners;
  constructor() {
    const element = document.createElement("div");
    element.classList.add("fancy-editor");

    const editor = new EditorView({
      extensions: [
        basicSetup,
        ruleAt80Columns,
        keymap.of([
          ...defaultKeymap,
          {
            key: "Mod-d", // Ctrl+D or Cmd+D
            run: duplicateLine,
          },
        ]),
        EditorView.updateListener.of((v) => {
          if (v.docChanged) {
            for (const listener of this.#listeners) listener();
          }
        }),
      ],
      parent: element,
    });

    this.#element = element;
    this.#editor = editor;
    this.#listeners = [];
  }

  getText() {
    return this.#editor.state.doc.toString();
  }

  setText(text) {
    if (text === "") {
      text = "\n\n";
    }
    this.#editor.dispatch({
      changes: {
        from: 0,
        to: this.#editor.state.doc.length,
        insert: text,
      },
    });
  }

  changeEvent(handler) {
    this.#listeners.push(handler);
  }

  getElement() {
    return this.#element;
  }
}

/**
 * @param {CodeEditor} editor - Text editor object
 * @param {HTMLElement} formField - Textarea/Text input field element
 * @returns {Function} Sync function. Syncs the editor text back into the input field
 */
export function bindEditorAndFormInput(editor, formField) {
  formField.style.display = "none";
  editor.setText(formField.value);
  formField.insertAdjacentElement("afterend", editor.getElement());
  editor.changeEvent(() => {
    formField.value = editor.getText();
  });
}
