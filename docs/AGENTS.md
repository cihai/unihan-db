# Documentation voice

This file covers the *voice* of prose under `docs/` — how to frame a
page so a reader meets the idea before its API surface. It complements
the repository-root `AGENTS.md`, which already governs code blocks,
changelog conventions, and MyST roles. When the two overlap, the root
file wins; this one only answers the question it leaves open: how
should the prose sound?

## Who you are writing for

The default reader writes Python and wants UNIHAN queryable through
SQLAlchemy — `get_session()`, `bootstrap_unihan()`, then ordinary ORM
queries against `Unhn` and its related tables. They can write a
SQLAlchemy query, but you cannot assume they know the UNIHAN dataset's
field vocabulary (`kMandarin`, `kHanyuPinyin`), the ETL layer
underneath (unihan-etl's download and normalization), or where the
default SQLite database lands (an XDG data directory).

A second, smaller reader works *on* unihan-db or the wider cihai
stack: tuning `UNIHAN_FILES` and `UNIHAN_FIELDS`, the importer's
record-to-ORM wiring, or contributing. Serve them too, but mark their
material opt-in ("for the rarer cases", "advanced") so the default
reader knows they can stop. Never make the common case pay a
comprehension tax for the advanced one.

## Voice

- **Second person, present tense, active.** "You query the readings",
  not "Readings are queried". Address the reader who is doing the
  thing.
- **Concept before API surface.** Open by saying what the table or
  helper *is* and what it does for the reader. The signature — the
  parameters, the column list — is the last detail they need, not the
  first. A page that opens with a function signature has buried the
  idea under its mechanics.
- **Say when they can stop.** Lead with the default and the
  reassurance: `get_session()` plus `bootstrap_unihan()` covers most
  uses, the defaults work, the advanced parts are optional. Let a
  skimmer leave after one paragraph.
- **Grant permission, don't demand attention.** "Reach for this
  when…", "for the rarer cases" — tell readers they're in the right
  place without implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the
  default bootstrap → the one option a few will tune (a custom
  database URL) → narrowing the file and field lists → the importer
  internals. Each step is for a smaller audience than the last.
- **Lean on the pipeline.** The reader thinks download → load → query:
  unihan-etl fetches and normalizes UNIHAN, `bootstrap_unihan` loads
  it once, and everything after is ordinary SQLAlchemy against `Unhn`
  and the tables that hang off it. Reinforce that chain when you
  explain where a step happens or what a helper wraps.
- **Name the trade-off.** If a call costs something — the first
  bootstrap downloads the UNIHAN archive and imports for minutes, a
  re-run skips the import only when `Unhn` already has rows — say so,
  and say what it buys ("one slow load, then every query is local
  SQLite"). State it; don't sell it.
- **Frame by concept, not by mechanism.** Don't headline a feature by
  its UNIHAN field code in prose; `kHanyuPinyin` names the dataset's
  surface, which is the reader's last concern. Name the concept —
  Mandarin readings, dictionary locations, variant forms. The field
  codes belong in a reference table or the API docs, and only there.

## Examples that run

Doctests under `docs/` execute: `testpaths` includes `docs`, and
pytest-doctest-docutils (from gp-libs) collects every `>>>` block in a
Markdown page. `ELLIPSIS` and `NORMALIZE_WHITESPACE` are on globally,
so variable output can be elided without a per-line flag.

- The root `conftest.py` puts `tmp_path` in the `doctest_namespace`
  and redirects `HOME` and the working directory to temporary paths,
  so a doctest can create a throwaway SQLite file safely.
- Tests run offline. `bootstrap_unihan` against real UNIHAN data
  downloads from unicode.org — keep it out of doctests. Show schema
  creation, in-memory engines, and ORM objects instead, the way
  `tests/` does with its zipped fixtures.
- Fence a `>>>` session as a ```` ```python ```` block; use a
  ```` ```console ```` block for shell commands at a `$` prompt.

## What stays precise

Warm the framing, never the facts. Column lists, UNIHAN field tables,
exact error strings, database URL templates, and class or function
cross-references carry meaning in their exact form — leave them alone.
The friendly voice belongs in the sentences *around* a precise block,
introducing it, not inside it paraphrasing it into vagueness.

## Cross-references

Point the advanced reader at the deep-dive rather than inlining it,
and put the link where their interest peaks — on the phrase that made
them curious ("tune the field list", "how records become rows") — not
as a standalone footnote the eye skips. Use the MyST roles listed in
the root `AGENTS.md` (`{class}`, `{meth}`, `{func}`, `{attr}`,
`{exc}`, `{ref}`, `{doc}`). A `{ref}` must match its target's anchor
exactly — anchors here are lowercase and hyphenated (`api`,
`quickstart`, `developmental-releases`, `code-style`). SQLAlchemy and
Python objects resolve through intersphinx. `just build-docs` catches
a broken cross-reference; the doctests do not — so build the docs
before you commit.

Link the first prose mention of any symbol that has a useful
destination on that page. This includes Python objects, unihan-db
APIs, SQLAlchemy APIs, topic pages, and external tools or projects.
Use the most specific target available: `{class}`, `{meth}`, `{func}`,
`{mod}`, `{exc}`, or `{attr}` for API objects; `{ref}` or `{doc}` for
documentation pages and section anchors; and a Markdown link or
reference link for external projects. After the first linked mention
on a page, later mentions can stay plain unless the distance or
context makes another link useful.

Do not rely on a later reference section to satisfy the first-mention
rule. If the first occurrence would be a heading, grid-card teaser, or
introductory sentence, link that occurrence or retitle the heading so
the first prose mention can carry the link. Leave command examples,
code blocks, and literal configuration values as code; link the
surrounding prose instead.

## A page that does this

`docs/index.md` is the closest worked example: a concept-first opening
that says what unihan-db *is* and routes each reader to the right
project (the ETL pipeline lives in unihan-etl, end-user lookups in
cihai) before any code, then a three-step at-a-glance example — create
the schema, load the data, query a character. Read it before reshaping
another page.

## Before you commit

- Does the page open with what the feature *is*, or with how to call it?
- Can a reader who needs only the default bootstrap stop after the
  first paragraph?
- Is anything framed by its UNIHAN field code that should be named by
  concept instead?
- Are the advanced and importer-level parts clearly marked opt-in?
- Do the doctests still pass (`just test`), and did you leave every
  code block, table, error string, and cross-reference exact?
- Did `just build-docs` stay clean — no new warning, no broken
  cross-reference?
