# Future work

Things todo.

## Editor

- Currently, the markdown will allow any tag like `<script>window.location="google.com"</script>` to be put into the text fields. This is a major security issue. Before any real-world deployment this must be resolved.

Add WYSIWYG Editor

- Mathquil seems like a good options
- Keep plain text code editor for advanced math operations and tricky formatting.

Improve plaintext problem editor to be more like a code editor.

- Add line numbers, proper TAB support, etc.
- There should be a library for this.

Add easy view to add missing problems to a category

## Auth

Add user permissions system:

- Admin (do everything)
- Contributor (Can create and edit problems without review)
- Reviewer (Can review problems and add them to the problem list)
- Guest (can create problem drafts and request for them to be reviewed )

Add user profiles

Allow public user signup

## Problems

Create separate table for solutions. One problem can have many solutions

- This will solve part of the difficulty of tagging problems.
  The problems themselves will be tagged based upon the statement
  The solutions will be tagged based on their content

Add problem quantity to sources

**Fix Markdown XSS**
