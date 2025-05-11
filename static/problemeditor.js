document.addEventListener("DOMContentLoaded", () => {
  for (const select of document.querySelectorAll("select")) {
    select.style.fontFamily = "sans-serif";
  }
  // FUTURE WORK: Find a select library that doesn't use JQuery.
  $("form select").select2();
  document.getElementById("newSolutionButton").addEventListener("click", () => {
    createNewSolution();
  });
});
function createNewSolution() {
  let [lastNo, last] = getLastSolution();
  const form = document.querySelector("main > form");
  const submit = form.querySelector("#newSolutionButton");
  let newSolution = cloneAndBlankSolution(
    getDummySolution(),
    (lastNo ?? 0) + 1
  );
  form.insertBefore(newSolution, submit);
  $("form select").select2();
}

function getDummySolution() {
  return document.querySelector("#dummySolutionHolder > .solutionWrapper");
}

function cloneAndBlankSolution(solution, newSolutionNumber) {
  // TODO: edit labels (regex? replace)
  // Could just regex the entire innerhtml lol
  const cloned = solution.cloneNode(true);
  cloned.setAttribute("data-solution-no", newSolutionNumber);

  const textarea = cloned.querySelector("textarea");
  textarea.name = `sol${newSolutionNumber}-solution_text`;
  textarea.id = `sol${newSolutionNumber}-solution_text`;
  textarea.innerHTML = "";
  const technique = cloned.querySelector("select");
  technique.name = `sol${newSolutionNumber}-techniques`;
  technique.id = `sol${newSolutionNumber}-techniques`;

  let a = document.querySelector("#additional_solutions");
  a.setAttribute("value", parseInt(a.value, 10) + 1);

  return cloned;
}

function getLastSolution() {
  const solutions = [
    ...document.querySelectorAll("div.solutionWrapper[data-solution-no]"),
  ];
  let n = solutions.map((e) =>
    parseInt(e.getAttribute("data-solution-no"), 10)
  );
  let max = Math.max(...n);
  if (max === -Infinity) {
    return [null, null];
  }
  return [
    max,
    solutions
      .filter((n) => max.toString() === n.getAttribute("data-solution-no"))
      .at(0),
  ];
}
