(() => {
  "use strict";

  const root = document.getElementById("publications");
  if (!root) return;

  const container = root.querySelector("#publication-groups");
  const search = root.querySelector("#publication-search");
  const type = root.querySelector("#publication-type");
  const index = root.querySelector("#publication-index");
  const counter = root.querySelector("#publication-result-count");
  const empty = root.querySelector("#publication-empty");
  const buttons = [...root.querySelectorAll("[data-group]")];
  const topics = JSON.parse(document.getElementById("publication-topics").textContent);
  const normalize = (text) => text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const publications = [...container.querySelectorAll(".publication-entry")].map((element) => ({
    element,
    year: element.dataset.year,
    topic: element.dataset.topic,
    type: element.dataset.type,
    search: normalize(element.textContent),
  }));
  let groupBy = "year";

  function render() {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    const visible = publications.filter((publication) =>
      (type.value === "all" || publication.type === type.value) &&
      terms.every((term) => publication.search.includes(term))
    );
    const keys = groupBy === "year"
      ? [...new Set(visible.map((publication) => publication.year))]
      : topics.map((topic) => topic.id);
    const fragment = document.createDocumentFragment();
    const links = document.createDocumentFragment();

    for (const key of keys) {
      const members = visible.filter((publication) => publication[groupBy] === key);
      if (!members.length) continue;

      const title = groupBy === "year" ? key : topics.find((topic) => topic.id === key).label;
      const id = `publications-${groupBy}-${key}`;
      const section = document.createElement("section");
      section.className = "publication-group";
      section.setAttribute("aria-labelledby", id);
      const heading = document.createElement("h2");
      heading.id = id;
      heading.tabIndex = -1;
      heading.textContent = `${title} `;
      const count = document.createElement("span");
      count.className = "publication-group-count";
      count.textContent = `(${members.length})`;
      heading.append(count);
      section.append(heading, ...members.map((publication) => publication.element));
      fragment.append(section);

      const link = document.createElement("a");
      link.href = `#${id}`;
      link.textContent = title;
      links.append(link);
    }

    container.replaceChildren(fragment);
    index.replaceChildren(links);
    index.setAttribute("aria-label", groupBy === "year" ? "Publication years" : "Research areas");
    index.hidden = !visible.length;
    empty.hidden = Boolean(visible.length);
    counter.textContent = `${visible.length} of ${publications.length} records`;
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.group === groupBy));
    }
  }

  for (const button of buttons) {
    button.addEventListener("click", () => {
      groupBy = button.dataset.group;
      render();
    });
  }
  search.addEventListener("input", render);
  type.addEventListener("change", render);
  root.querySelector(".publications-controls").hidden = false;
  render();
})();
