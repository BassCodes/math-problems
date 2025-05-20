// "use strict";
// document.addEventListener("DOMContentLoaded", () => {
//   main();
// });

// let activatedStuff = null;

// function main() {
//   activatedStuff = parseUrlSearch();
//   monitorDataboxInput(
//     document.querySelector(".search-databox[data-type=source]"),
//     "source"
//   );
//   monitorDataboxInput(
//     document.querySelector(".search-databox[data-type=category]"),
//     "category"
//   );
//   monitorDataboxInput(
//     document.querySelector(".search-databox[data-type=technique]"),
//     "technique"
//   );
// }

// function parseUrlSearch() {
//   const FILTER_MAPPING = { sou: "source", tec: "technique", cat: "category" };

//   let activated = {
//     source: new Set(),
//     technique: new Set(),
//     category: new Set(),
//   };

//   const search = window.location.search;

//   for (let prop of search.split("&")) {
//     try {
//       if (!prop) {
//         continue;
//       }
//       if (prop.startsWith("?")) {
//         prop = prop.substring(1);
//       }
//       const split = prop.split("=");
//       const filterTypeAbbreviate = split[0];
//       const values = split[1];
//       const filterType = FILTER_MAPPING[filterTypeAbbreviate];
//       const valuesArray = new Set(JSON.parse(values));
//       activated[filterType] = valuesArray;
//     } catch (e) {
//       continue;
//     }
//   }

//   return activated;
// }

// function monitorDataboxInput(dataBox, filterType) {
//   const searchBox = dataBox.querySelector("input[type=search]");
//   const listItems = [...dataBox.querySelectorAll("li")];
//   const inactiveIds = new Set();
//   const inactiveTitles = new Map();
//   const idToListItem = new Map();

//   for (const item of [...dataBox.querySelectorAll("#available-filters  li")]) {
//     const id = parseInt(item.getAttribute("data-id"));
//     const name = item.textContent.trim();
//     inactiveIds.add(parseInt(id, 10));
//     inactiveTitles.set(id, name.toLowerCase());
//     idToListItem.set(id, item);
//   }
//   for (const item of listItems) {
//     const id = parseInt(item.getAttribute("data-id"), 10);
//     const checkbox = item.querySelector("input[type=checkbox]");

//     checkbox.addEventListener("input", (e) => {
//       const checked = e.target.checked;
//       if (checked) {
//         activatedStuff[filterType].add(id);
//       } else {
//         activatedStuff[filterType].delete(id);
//       }
//       sendRequest();
//     });
//   }

//   searchBox.addEventListener("input", (e) => {
//     const text = searchBox.value.toLowerCase();

//     let matchingIds = [];
//     for (const [id, title] of inactiveTitles.entries()) {
//       if (title.includes(text)) {
//         matchingIds.push(id);
//       }
//     }
//     matchingIds = new Set(matchingIds);
//     const nonMatchingIds = inactiveIds.difference(matchingIds);

//     matchingIds.forEach((id) => {
//       idToListItem.get(id).classList.remove("hidden");
//     });
//     nonMatchingIds.forEach((id) => {
//       idToListItem.get(id).classList.add("hidden");
//     });
//   });
// }

// function sendRequest() {
//   const filters = activatedStuff;
//   let searchString = "?";
//   for (const key of Object.keys(filters)) {
//     const values = filters[key];
//     const trimmedTagType = key.substring(0, 3);

//     const valuesArray = [...values];
//     valuesArray.sort();
//     const queryString = `${trimmedTagType}=[${valuesArray.toString()}]&`;
//     searchString += queryString;
//   }

//   let current = window.location.search;
//   if ("?" !== searchString && current !== searchString) {
//     console.log("changing to ", searchString);
//     window.location.search = searchString;
//   }
// }

// // function main() {
// //   console.log("Started main");

// //   document.querySelectorAll(".search-databox").forEach((databox) => {
// //     watchDatabox(databox);
// //   });

// //   document.getElementById("show_source").addEventListener("input", (event) => {
// //     console.log(event.target.checked);
// //     document.querySelectorAll("h2#source-name").forEach((e) => {
// //       if (event.target.checked) {
// //         e.classList.remove("hidden");
// //       } else {
// //         e.classList.add("hidden");
// //       }
// //     });
// //     document.querySelectorAll("div#problem-number").forEach((e) => {
// //       if (event.target.checked) {
// //         e.classList.remove("hidden");
// //       } else {
// //         e.classList.add("hidden");
// //       }
// //     });
// //   });
// // }

// // function updateActivated() {
// //   let searchString = "?";
// //   for (const [tagType, values] of activatedTagTypes.entries()) {
// //     const trimmedTagType = tagType.substring(0, 3);
// //     if (values.size === 0) {
// //       continue;
// //     }
// //     const valuesArray = [...values];
// //     valuesArray.sort();
// //     const queryString = `${trimmedTagType}=[${valuesArray.toString()}]&`;
// //     searchString += queryString;
// //   }

// //   let current = window.location.search;
// //   if (current !== searchString && "?" + current !== searchString) {
// //     console.log("changing to ", searchString);
// //     window.location.search = searchString;
// //   }
// // }

// // function watchDatabox(databox) {
// //   const dataType = databox.getAttribute("data-type");
// //   const activatedIds = new Set();
// //   activatedTagTypes.set(dataType, activatedIds);
// //   const searchBox = databox.querySelector("input[type=search]");
// //   const listItems = [...databox.querySelectorAll("li")];
// //   const allIds = new Set(listItems.map((i) => i.getAttribute("data-id")));
// //   const titles = new Map();
// //   const idToListItem = new Map();
// //   const checkboxes = new Map();

// //   for (const item of listItems) {
// //     const id = item.getAttribute("data-id");
// //     const name = item.textContent.trim();
// //     idToListItem.set(id, item);
// //     titles.set(id, name.toLowerCase());
// //     checkboxes.set(id, item.querySelector("input[type=checkbox]"));
// //   }

// //   for (const [id, checkbox] of checkboxes) {
// //     checkbox.addEventListener("input", () => {
// //       checkboxChanged(id, checkbox);
// //       updateActivated();
// //     });

// //     checkboxChanged(id, checkbox);
// //   }
// //   function checkboxChanged(id, checkbox) {
// //     if (checkbox.checked) {
// //       activatedIds.add(id);
// //       console.log(id, "checked");
// //     } else {
// //       activatedIds.delete(id);
// //     }
// //   }

// //   searchBox.addEventListener("input", (e) => {
// //     const text = searchBox.value.toLowerCase();

// //     let matchingIds = [];
// //     for (const [id, title] of titles.entries()) {
// //       if (title.includes(text)) {
// //         matchingIds.push(id);
// //       }
// //     }
// //     matchingIds = new Set(matchingIds);
// //     console.log(matchingIds);
// //     const nonMatchingIds = allIds.difference(matchingIds);

// //     matchingIds.forEach((id) => {
// //       idToListItem.get(id).classList.remove("hidden");
// //     });
// //     nonMatchingIds.forEach((id) => {
// //       idToListItem.get(id).classList.add("hidden");
// //     });
// //   });
// //   updateActivated();
// // }
