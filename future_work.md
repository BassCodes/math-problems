# Future work

Things todo.

## General Layout

Rework layout to be responsive. Grid, Flexbox?

Grid works, but is difficult to get responsive.
Flexbox is difficult to get working, but is easier to get responsive. Preliminary testing has shown flexbox to probably be inadequate.

## Problem List Search

Filter problems by Source, Branch, Type, and Technique

Nice looking filters (probably using select2)

Number of results matched

## Editor

Add views to edit Tags (Type, Branch, Technique)

- Create
- Edit
- Delete

Integrate tag create views into problem editor

## Drafts

Allow creating of draft problems

Get deleted after three months of inactivity.

Draft problems get sent into review

Draft problems are reviewed by Reviewers and are then published

Draft solutions?

Draft edits?

## Auth

Add user permissions system:

- Admin (do everything)
- Contributor (Can create and edit problems without review)
- Reviewer (Can review problems and add them to the problem list)
- Guest (can create problem drafts and request for them to be reviewed )

Write migrations to create these permissions

Allow public user signup

### Solved Problems

Allow users to mark problems as solved
Add solved problems to user profile

Filter problems list by solved/unsolved

markers on problems for solved
markers on sources for solved problems

## Problems

Pagination to problem list

# Long Term

## Editor

Add WYSIWYG Editor

- Mathquil seems like a good option
