import { markdownify } from "../inlined/markdown.mjs";

import { $, $$ } from "../util/notjquery.mjs";

import { FormEditor } from "./form_editor.mjs";
import {
  ButtonField,
  CheckboxField,
  CodeEditorTextareaField,
  NumberField,
} from "./fields.mjs";
import { PreviewRenderer } from "./preview_renderer";

// I admit, it's a bit jankey. JavaScript; I love it.
// We'll probably rewrite our codebase in typescript or whatever.....js

class ProblemEditForm extends FormEditor {
  /** @type {  CodeEditorTextareaField[] } */
  #existingSolutionCount = undefined;
  constructor() {
    super();
  }
  attachForm(form) {
    this.addField(
      "problemText",
      new CodeEditorTextareaField($("#problemTextField > textarea", form))
    );
    this.addField(
      "answerText",
      new CodeEditorTextareaField($("#answerTextField > textarea", form))
    );
    this.addField(
      "hasAnswer",
      new CheckboxField($("#hasAnswerField > input", form))
    );
    this.addField(
      "newSolution",
      new ButtonField($("button#newSolutionButton", form))
    );
    this.addField(
      "additionalSolutions",
      new NumberField($("input#additional_solutions", form))
    );

    const solutionCount = $$(".solutionWrapper", form).length;
    this.#existingSolutionCount = solutionCount;
    for (const [solutionNo, element] of $$(
      ".solutionTextField > textarea",
      form
    ).entries()) {
      this.createNewSolution(solutionNo, element);
    }

    for (let i = 0; i < this.getField("additionalSolutions").value(); i++) {
      this.createNewSolution(this.#existingSolutionCount + i);
    }

    super.attachForm(form);
  }

  rigFields() {
    this.getField("hasAnswer").changeEvent((f) => {
      if (f.value()) {
        this.getField("answerText").show();
      } else {
        this.getField("answerText").hide();
      }
    });

    this.getField("newSolution").changeEvent((f) => {
      this.createNewSolution().rig(this);
    });

    super.rigFields();
  }

  createNewSolution(number, existing) {
    // Add new field to dom

    let newSolutionNumber;
    if (number !== undefined) {
      newSolutionNumber = number;
    } else {
      newSolutionNumber =
        this.#existingSolutionCount +
        this.getField("additionalSolutions").value();
      this.getField("additionalSolutions").modifyValue((v) => v + 1);
    }
    console.assert(!isNaN(newSolutionNumber), "Solution number is NaN");

    let element;
    if (existing) {
      element = existing;
    } else {
      let clone = cloneNewSolutionElement(newSolutionNumber);
      // Delete solution button
      let del = document.createElement("button");
      del.type = "button";
      del.textContent = "Remove Solution";
      del.id = `deleteSolution${newSolutionNumber}`;
      del.addEventListener("click", () => {
        this.deleteField(`solution${newSolutionNumber}`, {
          removeDom: true,
        });
        this.getField("additionalSolutions").modifyValue((v) => v - 1);
      });
      clone.appendChild(del);
      $("#solutionsBox").appendChild(clone);
      element = $("textarea", clone);
    }
    window.$("main form select").select2();

    return this.addField(
      `solution${newSolutionNumber}`,
      new CodeEditorTextareaField(element)
    );
  }
}

function cloneNewSolutionElement(newNumber) {
  let clone = $("#dummySolutionHolder > .solutionWrapper").cloneNode(true);
  let cloneHtml = clone.innerHTML
    .toString()
    .replaceAll("REPLACEME", newNumber.toString());
  clone.innerHTML = cloneHtml;
  clone.style.display = "";
  return clone;
}

class EditorFormPreviewRenderer extends PreviewRenderer {
  /**
   *
   * @param {FormEditor} editor
   */
  constructor(editor) {
    super();
    this.attachBox($(".previewBar"));
    this.addPreviewBox("problem", "Problem");
    this.addPreviewBox("answer", "Answer");

    for (const [id, field] of editor.fields()) {
      this.takeEditorFieldForSolution(editor, id, field);
    }
    editor.addFieldCreateEvent((e, name) => {
      const field = e.getField(name);
      this.takeEditorFieldForSolution(editor, name, field);
    });

    editor.getField("hasAnswer").changeEvent((f) => {
      if (f.value()) {
        this.getPreviewBox("answer").show();
      } else {
        this.getPreviewBox("answer").hide();
      }
    });

    editor.getField("problemText").changeEvent((field) => {
      let md = markdownify(field.value());
      this.getPreviewBox("problem").updateInnerHtml(md);
    });
    editor.getField("answerText").changeEvent((field) => {
      let md = markdownify(field.value());
      this.getPreviewBox("answer").updateInnerHtml(md);
    });
  }

  takeEditorFieldForSolution(editor, id, field) {
    if (id.startsWith("solution")) {
      const solutionNoString = id.substring("solution".length);
      const solutionNo = parseInt(solutionNoString, 10) + 1;
      this.addPreviewBox(id, `Solution #${solutionNo}`);
      field.changeEvent((field) => {
        let md = markdownify(field.value());
        this.getPreviewBox(id).updateInnerHtml(md);
      });
      editor.addFieldDeleteEvent(id, () => {
        this.removeBox(id);
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const editor = new ProblemEditForm();
  editor.attachForm($("main form"));
  const preview = new EditorFormPreviewRenderer(editor);

  editor.rigFields();

  // This one is real jquery. Unfortunately select2 requires jquery.
  window.$("main form select").select2();
});
