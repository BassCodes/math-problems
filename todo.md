## Styles

- Horizontal rules look bad in doc scope
- Spruce up signup form
- Fix list style on sources pages
- Find external font to appease brave browser (doesn't want to use Palatino system font)
- Not all pages have .doc class
- Make layout responsive

## Functional

- Docker setup?

- Create _through_ model for Problem<->Source to hold number (not sure about this)

- Test unicode codepoint icons on other fonts/machines

- Move markdown to templates dir

- Djlint considers regroup to be a block instead of inline

- Give problem \_\_str\_\_ name from source name

- Django Slugify?

- Add problem_history foreign key to solution_history when solution deleted (see problems/signals.py)

- Fix bug in problem history where all dates become the same

- Add limits to everything

  - Number of solutions
  - Problem/Solution/Answer text length

- Drafts system

- Problem list pagination
