# Writing

How this project writes prose, for humans and agents alike. It governs
`README.md`, `CHANGES`, commit messages, docstrings, source comments, and the
Sphinx documentation under `docs/` — every surface a reader reaches.

For environment setup, the gates, and pull request workflow, see
[CONTRIBUTING.md](CONTRIBUTING.md).

## Voice

Three surfaces, one voice. A docstring says what a caller may rely on; a
`CHANGES` entry says what changed; prose says what happens. All three are
present tense, lead with the thing being described, and stop. Why it was built
that way belongs in the commit message, which is timestamped and attached to
the diff.

The most useful editing operation is deleting the introductory sentence.

Lead with verbs and name concrete things. Put identifiers in backticks. Prefer
short declarative sentences, one operational fact each. Do not explain Python
to Python developers; do explain this project's semantics.

Type annotations describe shape. Documentation describes meaning. A sentence
that restates a signature has said nothing.

Use MUST, SHOULD, and MAY only where the normative sense is meant. Say what
actually happens rather than that something is "supported".

| Instead of                       | Prefer                            |
| --------------------------------- | ---------------------------------- |
| "We added…"                      | "`bootstrap.get_session` now…"    |
| "New and improved"               | "`Unhn.to_dict` now…"             |
| "powerful", "seamless"           | state the capability              |
| "easily", "simply", "just"       | omit                              |
| "simple", "obvious", "intuitive" | omit                              |
| "robust"                         | name the failure that is handled  |
| "comprehensive"                  | name what is covered              |
| "production-ready"               | state the guarantee               |
| "optimized", "blazingly fast"    | give the magnitude                |
| "various fixes"                  | name the components               |
| "under the hood"                 | omit unless observable            |
| "please note that", "note that"  | state the fact                    |
| "leverage", "utilize"            | "use"                             |
| "delve into"                     | "read", or omit                   |
| "best practices"                 | name the practice                 |
| "in order to"                    | "to"                              |

## Who you are writing for

The default reader writes Python and wants UNIHAN queryable through
SQLAlchemy — `get_session()`, `bootstrap_unihan()`, then ordinary ORM queries
against `Unhn` and its related tables. They can write a SQLAlchemy query, but
you cannot assume they know the UNIHAN dataset's field vocabulary
(`kMandarin`, `kHanyuPinyin`), the ETL layer underneath (unihan-etl's download
and normalization), or where the default SQLite database lands (an XDG data
directory). Serve them first.

A second, smaller reader works *on* unihan-db or the wider cihai stack:
tuning `UNIHAN_FILES` and `UNIHAN_FIELDS`, the importer's record-to-ORM
wiring, or contributing. Serve them too, but mark their material opt-in —
"for the rarer cases", "advanced" — so the default reader knows they can
stop. Never make the common case pay a comprehension tax for the advanced
one.

Rules that follow:

- **Second person, present tense, active.** "You query the readings", not
  "Readings are queried". Address the reader who is doing the thing.
- **Concept before API surface.** Open by saying what the table or helper
  *is* and what it does for the reader. The signature — the parameters, the
  column list — is the last detail they need, not the first. A page that
  opens with a function signature has buried the idea under its mechanics.
- **Say when they can stop.** Lead with the default and the reassurance:
  `get_session()` plus `bootstrap_unihan()` covers most uses, the defaults
  work, the advanced parts are optional. Let a skimmer leave after one
  paragraph.
- **Grant permission, do not demand attention.** "Reach for this when…",
  "for the rarer cases" — tell readers they are in the right place without
  implying they must read on.
- **Progressive disclosure.** Order by how many readers need it: the default
  bootstrap, then the one option a few will tune (a custom database URL),
  then narrowing the file and field lists, then the importer internals. Each
  step is for a smaller audience than the last.
- **Lean on the pipeline.** The reader thinks download → load → query:
  unihan-etl fetches and normalizes UNIHAN, `bootstrap_unihan` loads it once,
  and everything after is ordinary SQLAlchemy against `Unhn` and the tables
  that hang off it. Reinforce that chain when explaining where a step
  happens or what a helper wraps.
- **Name the trade-off.** If a call costs something — the first bootstrap
  downloads the UNIHAN archive and imports for minutes, a re-run skips the
  import only when `Unhn` already has rows — say so, and say what it buys
  ("one slow load, then every query is local SQLite"). State it; do not sell
  it.
- **Frame by concept, not by mechanism.** Do not headline a feature by its
  UNIHAN field code in prose; `kHanyuPinyin` names the dataset's surface,
  which is the reader's last concern. Name the concept — Mandarin readings,
  dictionary locations, variant forms. Field codes belong in a reference
  table or the API docs, and only there.

## What stays precise

Warm the framing, never the facts. Column lists, UNIHAN field tables, exact
error strings, database URL templates, and class or function
cross-references carry meaning in their exact form — leave them alone. The
friendly voice belongs in the sentences *around* a precise block,
introducing it, not inside it paraphrasing it into vagueness.

`docs/index.md` is the closest worked example: a concept-first opening that
says what unihan-db *is* and routes each reader to the right project (the
ETL pipeline lives in unihan-etl, end-user lookups in cihai) before any
code, then a three-step at-a-glance example — create the schema, load the
data, query a character. Read it before reshaping another page.

## README

A README is the shortest path from "what is this?" to competent use, not the
project's autobiography.

The first sentence is a contract. It says what abstraction the reader has
been handed, concretely enough to tell this package apart from the
neighbouring one.

Get to a runnable command or snippet before anything the reader can skip. A
logo, a mission statement, a comparison matrix and three paragraphs of
history in front of the install line all cost the same thing.

State the minimum Python version in prose, not only in badges.
`requires-python` in `pyproject.toml` is the authority; the README must
agree with it.

Name the distribution, the import, and the package differently wherever they
differ: the PyPI distribution is `unihan-db`, the import is `unihan_db`.
unihan-db ships no console script — do not imply one exists.

Examples are executable, not illustrative fiction. Document the semantic
model, not the flag list.

State defaults explicitly — defaults are API. State negative guarantees
where they exist: "creates no network connection until you call
`bootstrap_unihan`". They establish boundaries faster than any amount of
description.

Headings stay conventional and stable, because people deep-link them.
Badges are few and load-bearing.

## Documented examples that run

`pytest` executes documented examples through two independent mechanisms.
`addopts` in `[tool.pytest.ini_options]` sets `--doctest-modules`, which
collects `>>> ` examples from docstrings in `testpaths`. The `gp-libs` dev
dependency registers a second pytest plugin,
`pytest_doctest_docutils` (entry point `sphinx`), which reads Markdown and
reStructuredText files in `testpaths` for executable blocks. `testpaths` is
`src/unihan_db`, `tests`, and `docs` — `README.md` is not listed, so nothing
in it executes.

**Docstrings** (`src/unihan_db/**`) use the NumPy `Examples` section with
bare `>>> ` prompts:

    Examples
    --------
    >>> from unihan_db.tables import Base, Unhn

No docstring in this package currently has one; `--doctest-modules` is wired
and ready the day one is added.

**Docs pages** (`docs/**`) mark an executable Python session with the MyST
```` ```{doctest} ```` directive, not a `>>> ` prompt inside a plain
```` ```python ```` fence — a `python`-tagged fence on a docs page is prose,
and the docutils collector does not execute it.
`docs/how-to/custom-database.md` and `docs/how-to/query-related-tables.md`
are worked examples; write a new one the same way. Each
```` ```{doctest} ```` block collects as a single pytest item, so put a
whole worked session — imports through assertion — in one block rather than
splitting it across several.

`ELLIPSIS` and `NORMALIZE_WHITESPACE` are enabled globally
(`doctest_optionflags` in `pyproject.toml`), so `...` elides variable output
and whitespace differences do not fail a comparison. `# doctest: +SKIP` is
not permitted — it tests nothing. Do not downgrade a doctest to a
non-executed block to make it pass; fix the example or fix the code.

The root `conftest.py`'s autouse `add_doctest_fixtures` fixture is the only
source of names a doctest may use without importing them: it sets
`doctest_namespace["tmp_path"]` and, for a `DoctestItem`, redirects `HOME` to
a temporary directory. `docs/conf.py`'s `doctest_global_setup` mirrors both
for the separate Sphinx doctest builder that `just build-docs` runs (see
[Documentation](CONTRIBUTING.md#documentation)) — so a doctest can create a
throwaway SQLite file safely, but a real `bootstrap_unihan()` run against
live UNIHAN data belongs in `tests/`, not in a doctest; it downloads from
unicode.org and doctests run offline.

**README's own example is not a test.** The `## Example usage` block is a
plain ```` ```python ```` fence with no prompts, deliberately: GitHub renders
Markdown but does not execute Sphinx or pytest directives, so `README.md`
cannot reuse `{literalinclude}` the way `docs/index.md` and
`docs/quickstart.md` do. `tests/test_example.py` guards the real
`examples/01_bootstrap.py` script instead;
`tests/test_docs_examples.py::test_docs_pages_use_tested_examples` further
asserts that `docs/index.md` embeds that script via `{literalinclude}`
rather than a hand-copied snippet that could drift. No equivalent check
covers the README's copy — keep it in sync with `examples/01_bootstrap.py`
by hand when that script changes.

## MyST roles and cross-references

Class references use `{class}`, methods use `{meth}`, functions use
`{func}`, modules use `{mod}`, exceptions use `{exc}`, attributes use
`{attr}`, internal anchors use `{ref}`, doc-path links use `{doc}`.
SQLAlchemy and Python objects resolve through intersphinx. Any class,
method, function, exception, or attribute that has its own rendered page
must be cited via the matching role — never with plain backticks. Plain
backticks are correct for code syntax, environment variables, parameter
names, and file paths that are not doc pages.

Link the first prose mention of any symbol that has a useful destination on
that page: Python objects, unihan-db APIs, SQLAlchemy APIs, topic pages, and
external tools or projects. Use the most specific target available. After
the first linked mention on a page, later mentions can stay plain unless the
distance or context makes another link useful. Do not rely on a later
reference section to satisfy the first-mention rule — if the first
occurrence would be a heading, grid-card teaser, or introductory sentence,
link that occurrence or retitle the heading so the first prose mention can
carry the link. Leave command examples, code blocks, and literal
configuration values as code; link the surrounding prose instead.

A `{ref}` must match its target's anchor exactly — anchors in this repo are
lowercase and hyphenated (`api`, `quickstart`, `developmental-releases`,
`code-style`). `just build-docs` catches a broken cross-reference; the
doctests do not, so build the docs before you commit.

## The changelog

`CHANGES` is the changelog, rendered as the Sphinx changelog page. Its shape
is modeled on Django's release notes — deliverables get titles and prose,
not bullets. Older entries used a flat `### Section` + bullet shape; new
entries follow the shape below.

**Release entry boilerplate.** Every release header is
`## unihan-db X.Y.Z (YYYY-MM-DD)`. The file opens with a
`## unihan-db X.Y.Z (unreleased)` placeholder block fenced by
`<!-- KEEP THIS PLACEHOLDER ... -->` and `<!-- END PLACEHOLDER ... -->` HTML
comments — new release entries land immediately below the END marker, never
above it.

**Open with a multi-sentence lead paragraph.** Plain prose, no italic. Open
with the version as sentence subject ("unihan-db X.Y.Z ships …") so the lead
is self-contained when excerpted. Two to four sentences telling the reader
what shipped and who cares — user-visible takeaways, not internal mechanism.
Cross-reference detail docs with `{ref}` to keep the lead compact.

**Lead paragraphs are release-time material — off-limits to branches and
pull requests.** The unreleased entry carries no lead paragraph and no
version summary: sections only (`### Breaking changes`, `### What's new`
deliverables, `### Fixes`, …). Speaking for the release — what the version
"is", "ships", or "focuses on" — is presumptuous before its scope is final;
only the person cutting the release writes that, and only when the user
explicitly asks to release. Never write or edit a lead from a feature
branch, and never ask or imply that a release should happen.

**Each deliverable is a section, not a bullet.** Inside `### What's new`,
every distinct deliverable gets a `#### Deliverable title (#NN)` heading
naming it in user vocabulary, followed by one to three prose paragraphs
explaining what shipped. Do not wrap a paragraph in `- ` — bullets are for
enumerable lists, not paragraph containers. Cross-link detail docs with
`{ref}` so prose stays focused.

**The deliverable test.** Before writing an entry, ask: "What's the
deliverable, in user vocabulary?" If you cannot answer in one sentence, the
entry is not ready. Mechanism — helper internals, byte counters,
schema-validation locations — belongs in pull request descriptions and code
comments, not the changelog.

**Fixed subheadings**, in this order when present: `### Breaking changes`,
`### Dependencies`, `### What's new`, `### Fixes`, `### Documentation`,
`### Development`. Dev tooling (helper scripts, internal automation) lives
under `### Development`. For breaking changes, show the migration path with
concrete inline code (a `# Before` / `# After` fenced code block).
Dependency floor bumps use the form ``Minimum `pkg>=X.Y.Z` (was
`>=X.Y.W`)``.

**PR refs `(#NN)`** sit in each deliverable's `####` heading.

**When bullets are appropriate.** Catch-all sections (`### Fixes`,
occasionally `### Documentation`) with three or more genuinely small items
use bullets — one line each, never paragraphs. If a bullet swells past two
lines, promote it to a `#### Title (#NN)` heading with a prose body.

**Anti-patterns.** Fragile metrics — token ceilings, third-party version
pins, percent benchmarks, exact byte counts. Describe the capability, not
the math. Internal jargon — private symbols (leading-underscore
identifiers), algorithm names exposed for the first time, backend
scaffolding. Walls of text dressed up as bullets. Buried breaking changes —
they get their own subheading at the top of the entry.

**Always link autodoc'd APIs** via the roles in
[MyST roles and cross-references](#myst-roles-and-cross-references), never
with plain backticks. Doc pages without explicit ref labels use `{doc}`.

**Summarization style.** When asked "what changed in the latest version?" or
similar, lead with the entry's lead paragraph (paraphrased if needed),
followed by each `####` deliverable heading under `### What's new` with a
one-sentence summary. Cite `(#NN)` only if asked for source links. Do not
invent versions, dates, or numbers not present in `CHANGES`. Do not quote
line numbers or file offsets — those shift as the file evolves.

## Docstrings

The prime directive: never restate the type. The annotation is the source of
truth; the docstring carries what the annotation cannot.

This is documentation debt wearing a docstring:

    def get_char(row: Unhn) -> str:
        """Get the row's character.

        Parameters
        ----------
        row : Unhn
            The row.

        Returns
        -------
        str
            The character.
        """

Document instead the dimensions the type system cannot encode:

- **Mutation.** What it changes in place.
- **Ownership.** What the caller must close, release, or keep alive — a
  `ScopedSession` returned by `get_session()` is one.
- **Ordering.** Whether results come back in a guaranteed order.
- **Timing.** What has finished by the time the call returns —
  `bootstrap_unihan()` has committed rows before it returns; it does not
  return a lazy query.
- **Failure.** Which exceptions are raised and what triggers each.
- **Idempotence.** Whether calling twice does anything the second time —
  `bootstrap_unihan()` is a no-op once `Unhn` has rows.
- **Concurrency.** Whether calls are coalesced, queued, or independent, and
  whether the object is thread-safe, process-safe, or fork-safe.
- **Units and ranges.** What a number means and what values are accepted.
- **Boundary behaviour.** What zero, empty, and the maximum do.
- **Platform.** Behaviour that differs by operating system or dependency
  version — the default database path depends on the OS's XDG data
  directory.
- **Security boundary.** What is executed, and what is only read.

The first sentence stands alone; tooling truncates there. PEP 257 applies:
triple double quotes, an imperative one-line summary ending in a period, a
blank line before any extended description. Do not repeat an introspectable
signature.

This package uses NumPy-style `Parameters` and `Returns` sections, enforced
by `ruff`'s `pydocstyle` rule (`convention = "numpy"` in `pyproject.toml`),
not relitigated in review.

**Classes with fields** — `NamedTuple`, dataclasses — document every field
in an `Attributes` section:

```python
class DocsContentCase(t.NamedTuple):
    """Expected source-level contract for one docs page.

    Attributes
    ----------
    path : pathlib.Path
        Docs page to check, relative to the project root.
    """
```

Autodoc renders every field whether or not you describe it, so an
undocumented `NamedTuple` field ships to the API docs as "Alias for field
number 0" and a dataclass field ships bare. Document all of them — a class
with three fields and two documented still ships a stub for the third.

## Schema and model documentation

SQLAlchemy table classes in `src/unihan_db/tables.py` take a one-line
docstring naming the UNIHAN category or field the table stores — "Table for
kCCCII UNIHAN data.", "Unhn core table." — and nothing else. `docs/api/*.md`
renders every table with `.. automodule:: unihan_db.tables` and
`:undoc-members:`, so a mapped `Column` already carries its type,
nullability, and foreign key in the rendered signature; it does not need a
matching prose entry the way a `NamedTuple` or dataclass field does under
[Docstrings](#docstrings) — the difference is that a `Column` reflects that
information itself, and a bare field annotation does not.

Document a relationship, a polymorphic hierarchy, or a non-obvious
`__mapper_args__` choice with a short docstring or a
[source comment](#source-comments) only when the mapping itself is not
self-explanatory from the column and relationship names — for example, why
a table joins back to `Unhn.char` rather than a surrogate key.

## Source comments

A comment ships only if it passes all three gates. Fail any: delete or
rewrite. Borderline: delete — borderline means the information is
reconstructible, which is what makes deletion cheap.

**Loss.** Three years from now, would losing this cost a maintainer real
time rediscovering intent, an invariant, a constraint, or a failure mode the
code and tests do not already make obvious?

**Elite.** Would SQLite, Redis, the Go standard library, or CPython write
this comment, at this length? Those projects state the constraint and stop.
They do not argue with an imagined objector.

**Upkeep.** Will it stay true without maintenance? A comment that hand-syncs
a value the code owns — a count, an offset, a line reference, a duplicated
constant — is false the first time that value moves.

### Ceiling

One or two lines. A comment reaching four is either carrying several facts,
in which case split it, or arguing, in which case cut it to the fact.

Rationale, alternatives weighed, and the story of how the code got here
belong in the commit message: timestamped, attached to the exact diff, and
free to maintain.

A comment often holds both a constraint and the deliberation that found it.
Keep the constraint, cut the deliberation. "Runs at most once per second"
survives; "this is the right trade for now" does not.

### Keep

- Why over how: upstream quirks, protocol and compatibility constraints,
  performance tradeoffs still part of the contract.
- Invariants, preconditions, ordering, lifetime, and concurrency
  requirements that types and tests cannot express.
- Code that looks wrong but is not, so a later cleanup does not reintroduce
  the bug.
- A high-level sketch of an algorithm whose local operations do not reveal
  the whole.

### Delete

- Narration of the next lines; code translated into English.
- Restated names, types, defaults, or control flow.
- Values duplicated from the code and hand-synced.
- Justification, hedging, or apology for a choice.
- Speculation about future requirements.
- History version control already holds, including commented-out code.
- Ticket and issue numbers. They say nothing to a reader without tracker
  access, and they rot when the tracker moves. Unfinished work goes in the
  tracker, not the source.
- Transient observations — "currently", "for now", "the latest release" —
  that go stale with no nearby edit.

### The upkeep gate in practice

It reaches values that track our own code. It does not reach frozen
external facts.

Bad (Delete):

```python
# There are 321 tests to complete for servers.
```

Good (Keep):

```python
# CPython < 3.11 has no ExceptionGroup, so this branch stays.
```

### Documentation exception

Doctests, minimal usage examples, and `Parameters`, `Returns`, and
`Attributes` entries on public API are exempt from the loss gate — they
serve the caller, not the maintainer. They are exempt from nothing else.
Ceiling: a good man page entry.

## Terminology and capitalization

Pick the domain noun and keep it. If the code calls something a session, do
not call it a connection in one paragraph and a handle in the next. If the
helper is `bootstrap_unihan`, write "bootstrap" everywhere rather than
alternating with "seed", "populate", and "sync".

**The three cihai projects.** unihan-etl fetches and normalizes UNIHAN into
plain data; unihan-db (this repository) loads that data into SQLAlchemy
tables and queries it; cihai does end-user character lookups on top of both.
Name the project that owns the behaviour you are describing — do not
attribute an ETL concern to unihan-db or an ORM concern to unihan-etl.

**UNIHAN** is always capitalized — it is the Unicode Consortium's dataset
name, not an acronym to expand. CJK means Chinese, Japanese, and Korean; use
it for the script/locale family, not as a synonym for "UNIHAN".

**Field codes** (`kMandarin`, `kHanyuPinyin`, `kIRG_GSource`) are the
dataset's own vocabulary: lowercase `k` prefix, camelCase, always in
backticks. Do not invent a friendlier spelling. Name the concept in prose
("Mandarin readings") and cite the field code in backticks only where the
reader needs to match it to a column or table name — see
[Frame by concept, not by mechanism](#who-you-are-writing-for).

**`Unhn`** is the central ORM class and the table most other tables relate
back to (via `char_id` or `Unhn.char`). Call it "the `Unhn` table" or "the
`Unhn` row for a character", not "the UNIHAN table" — UNIHAN is the dataset,
`Unhn` is one mapped class in the schema that stores it.

**Distribution vs. import vs. package.** The PyPI distribution is
`unihan-db` (hyphenated); the import is `unihan_db` (underscored). There is
no console script.

Python and PyPI keep their own capitalisation. Distribution names are
written as they are published.

Do not write counts into prose — how many tables exist, how many UNIHAN
fields are supported. They go stale silently and no reader needs them.
Counts that pin a fixture or guard an invariant are different, and belong in
code.

## Markdown

Prose wraps at 80 columns. Table rows, badge lines, and long links are
exempt, because breaking them harms rendering. A pull request or issue body
does not wrap at all: GitHub renders a single newline as a space in a file
and as a line break in a comment, so a wrapped comment body arrives as
ragged stubs.

GitHub alert blocks — `> [!NOTE]`, `> [!WARNING]` — render as literal text
outside GitHub, so reserve them for at most one load-bearing warning per
document. Write the sentence so it carries the fact on its own, and a
renderer that drops the marker loses nothing.

Do not use a local absolute path or an email address in anything published.

## Code blocks

Code blocks are paste-and-run units: pasting one block runs exactly one
intended action. Doctests and other executed examples are exempt — the test
suite runs them, nobody pastes them.

- **One command per block.** Multiple steps may share a block only when
  explicitly chained with `&&`, `;`, or `\` continuations — the chain is
  then one logical command.
- **Explanations go in prose above the block**, never as `#` comments inside
  it.
- **Command menus are per-command blocks with prose lead-ins**, not tables.
- **Shell commands use the `console` tag with a `$ ` prefix.** This
  separates interactive commands from scripts and enables prompt-aware copy.
- **Split long commands with `\`** — one flag or flag+value pair per
  indented continuation line, positional arguments last.

Good — show the last ten commits as a graph:

```console
$ git log \
    --max-count=10 \
    --graph \
    --oneline
```

Bad:

```console
# Show the last ten commits as a graph
$ git log --max-count=10 --graph --oneline
```

## Commits

```
Scope(type[detail]): concise description

why: Explanation of necessity or impact.

what:
- Specific technical changes made
- Focused on a single topic
```

Keep the subject to 50 characters or fewer, excluding any trailing `(#NN)`
pull request reference, and wrap body lines at 72. Separate the `why:` and
`what:` blocks with a blank line.

Routine maintenance commits drop the colon and take a capitalised
description, which is what distinguishes them at a glance in
`git log --oneline`:

```
py(deps[dev]) Bump dev packages
ai(rules[AGENTS]) Judge comments by three gates
```

Everything that changes behaviour keeps the colon.

Common types:

- **feat**: New features or enhancements
- **fix**: Bug fixes
- **refactor**: Code restructuring without functional change
- **docs**: Documentation updates
- **chore**: Maintenance (dependencies, tooling, config)
- **test**: Test-related updates
- **style**: Code style and formatting
- **ci**: Workflow and pipeline changes
- **py(deps)**: Dependencies
- **py(deps[dev])**: Dev dependencies
- **ai(rules[AGENTS])**: AI rule updates
- **ai(claude[rules])**: Claude Code rules (`CLAUDE.md`)
- **ai(claude[command])**: Claude Code command changes

For a multi-line message, use a heredoc so the formatting survives:

```console
$ git commit -m "$(cat <<'EOF'
Scope(feat[detail]): Concise description

why: Explanation of the change.

what:
- First change
- Second change
EOF
)"
```

### Release commits

Never create tags. Never push tags. The owner handles tagging and tag
pushes, because a tag triggers the publish workflow.

A release commit subject is plain and short: `Tag v<version>`. The detailed
why and what go in the body. Do not use the `Scope(type[detail]):` format
for a release — it buries the lede.

## Slop prevention

Treat AI slop as review-hostile noise, not as proof that text or code is
wrong. The goal is to maximise information density.

- **AI signatures.** No "Generated by", no conversational filler, no
  unexplained emoji, no tool metadata.
- **Brittle references.** No hard-coded line numbers, fragile file counts,
  dated "as of" claims, bare SHAs, or local absolute paths — unless they are
  strict evidentiary artefacts such as a benchmark log.
- **Diff narration.** Do not restate what moved, was renamed, or was
  removed in anything the reader holds alongside the diff: code, docstrings,
  README, `CHANGES`, or a pull request description. The diff and the commit
  message already carry it.
- **Branch-internal narrative.** Do not mention intermediate states,
  abandoned approaches, or "no longer" behaviour unless users of the most
  recently published release actually experienced the old state (the
  published-release test).
- **Low-value scaffolding.** No ownerless TODOs, unused future-proofing,
  debug artefacts, or defensive wrappers around failure modes nothing can
  reach.
- **Prose inflation.** The diction table under [Voice](#voice) governs;
  replace an inflated word with a concrete description of behaviour,
  constraints, or trade-offs.
- **Coded labels.** Write rules and findings as plain imperatives. No
  `[R1]`, `Option B`, or any index a reader has to decode.

Preserve the "why". Never delete a comment documenting an invariant, a
protocol constraint, a platform quirk, or an upstream workaround — those are
the facts [Source comments](#source-comments) keeps, and every other
comment is judged by it.

### Durable source links

Link to a pinned revision, never to trunk. A pinned permalink is not a
brittle reference; an unlinked SHA dropped into prose is. `blob/master/…`
links rot silently — the file moves, lines shift, and the anchor lands on
unrelated code while still resolving.

- Prefer a release tag (`blob/v0.22.0/…`). Most durable, and it tells the
  reader which released version the claim held for.
- Otherwise use a 7-character commit ref (`blob/9a29b1a/…`) reachable from
  trunk. Use when there is no tag or the claim is about unreleased code.
  Never a pull-request-head SHA — it can be rebased or garbage-collected.
- Reserve `blob/master/…` for living documents meant to always show the
  latest state, such as a contributing guide.
- Line anchors (`#L120-L145`) are only safe on a pinned ref.

### The published-release test

Long-running branches accumulate tactical decisions — renames, refactors,
attempts-then-reverts. When deciding what counts as branch-internal, use
trunk or the parent branch as the baseline, not intermediate states inside
the current branch. Ask: did users of the most recently published release
ever experience this old name, old behaviour, or bug? If the answer is no,
it is branch-internal narrative — move it to the commit message and
describe only the final state in the artefact.

Keep in shipped artefacts: deprecations and migration guides for symbols
that actually shipped; `### Fixes` entries for bugs that affected users of a
published release; comments explaining why the current code looks this way
that make sense to a reader who never saw the previous version.

### Cleanup in hindsight

Applying these rules retroactively to an existing branch starts with
establishing scope: diff against the parent branch or trunk to see which
commits the branch actually introduced. For commits the branch introduced,
offer `fixup!` commits landed with `git rebase --autosquash`, or one cleanup
commit at the branch tip — ask which. For commits from trunk or a
colleague's branch, default to leaving them alone; act only on explicit
instruction, and fold any approved cleanup into a single commit rather than
rewriting shared history. If cleaning up prior slop would touch someone
else's work or expand the change beyond its stated goal, stay in lane:
protect the current goal and leave the rest alone.
