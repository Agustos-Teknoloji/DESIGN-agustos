# "On this page" contents list: design

**Date:** 2026-09-30
**Status:** design approved by Emre in chat on 2026-09-30; written spec for review
**Kit release:** v7.4.0 (a new class is a minor version)
**Repositories:** DESIGN-agustos (the component), APP-iesdesk (iesdesk.com), WEBSITE-agustos (agustos.com)

## Goal

A reader of a long legal page can jump to the section that they need. The IESDesk privacy notice has 9 sections and about 2,150 words. The agustos.com privacy policy has 8 sections in each language.

Kit v7.3.1 (MEMORY 2026-09-30 reading-line) keeps the side zone to the right of the reading line free "until a page needs a side column". This is the first side column.

## Decisions

Emre chose each option on 2026-09-30.

| Question | Choice | Rejected |
|---|---|---|
| Which pages | The legal pages on both sites: the IESDesk privacy notice and beta terms, and the agustos.com privacy policy in Turkish and English | IESDesk only (the two sites differ); every long content page (a rule for "long enough" and lists where nobody needs them) |
| Behaviour while scrolling | The list stays in view, with no script | A marker on the current section (it needs a script, a new IESDesk JavaScript exception); a list that scrolls away |
| Phones and small screens | One folded line under the page opening; a tap opens the list | An open list (nine lines push the text below the first screen); no list |

He approved the reader view from a live preview on iesdesk.com/privacy, and the build outline in chat.

## What the reader sees

### 1280px and wider

- The list sits in the side zone, from the side zone start (reading line plus `--space-xl`) to the frame's right edge.
- Its top is level with the page title.
- A heading "On this page" (Turkish: "Bu sayfada") sits above a numbered list of the section titles. The numbers are not shown.
- The list stays in view while the reader scrolls. It stops at the end of the page content and never covers the closing band or the footer.
- If the list is taller than the window, it scrolls inside itself.
- A link jumps to its section. The kit scroll offset (`scroll-padding-top`) puts the section below the sticky header.

### Below 1280px

- One line, "On this page" with a "+" at the right, sits between the page opening and the first section, with a hairline above and below.
- A tap or Enter opens the list, and the "+" becomes "−".
- The items are the same links.

### Style

- The links use `--ink-soft`, and `--ink` on hover and focus. There is no red, because red is identity and signal, not navigation.
- A 1px `--rule` line runs down the left of the list, the grammar of `blockquote`.
- The type is `--size-body-compact`.
- Each link is at least `--control-min` (44px) tall, the kit target size.

### Content rules

- Items are the page's main sections (its `h2` headings) only.
- An item's label is the exact text of its section heading.
- The list comes directly after the page opening: the title, the deck and the date.

## The kit component

### Markup

```html
<details class="agustos-contents">
  <summary class="agustos-contents__toggle">On this page</summary>
  <nav class="agustos-contents__nav" aria-label="On this page">
    <p class="agustos-contents__title">On this page</p>
    <ol class="agustos-contents__list">
      <li><a class="agustos-contents__link" href="#controller">Who is responsible</a></li>
    </ol>
  </nav>
</details>
```

- The element is a direct child of `.container--reading`.
- The page renders it closed. It needs no script at any width.
- `__toggle` is the folded line below 1280px. `__title` is the heading at 1280px and wider. Each size shows one of the two, so a screen reader never hears "collapsed" beside an open list.

### CSS (`tokens/web.css.tmpl`)

- `.container--reading` gets `position: relative`, so the component can take the full height of the page content.
- Below 1280px:
  - `.agustos-contents` has a 1px `--rule` border above and below, and `--space-2xl` below it.
  - `__toggle` is a 44px row with the text on the left and a "+" on the right ("−" when open). The browser marker is hidden.
  - `__title` is hidden.
- 1280px and wider:
  - `.agustos-contents` is absolute: `inset-block: 0`, the start edge at `calc(var(--measure-gutter) + var(--measure-body) + var(--space-xl))`, the end edge at `var(--measure-gutter)`. Its top padding is the container's top padding (`recipes.hero.paddingBlockStart`), so the heading starts level with the title. It loses its borders and margin.
  - Inside `@supports selector(::details-content)`:
    - `::details-content` is `content-visibility: visible`, `display: block`, `position: sticky`, and `top: calc(var(--site-header-height) + var(--space-xl))`.
    - Its `max-height` is the window height less that top and `--space-xl`, with `overflow-y: auto`.
    - `__toggle` is `display: none`, and `__title` is shown.
  - Without `::details-content` support (Safari before 18.4), the folded line stays in the side zone. One tap opens the list. It does not stay in view, and nothing breaks.
- The list, the links, the hover and the focus ring use existing tokens only. The focus ring is the kit 2px `--signal` ring.

### Other kit deliverables

- `tokens/design-tokens.json`: register the six classes: `agustos-contents`, `__toggle`, `__nav`, `__title`, `__list` and `__link`.
- `ui/UI-KIT.md.tmpl`: one line in the Column paragraph and the new classes in the Layout row. `UI-KIT.md` stays at 200 lines or fewer.
- `DESIGN.md`: the component in the layout table, and a note that it is a disclosure, not one of the absent dropdowns.
- `ui/starter.html.tmpl`: one rendered instance.
- `screens/`: no change. The static screen has no page long enough.
- Checker `AG031` (warn, on full pages): an `agustos-contents` element that is not a direct child of `container--reading`. AG029 and AG030 are taken (v7.3.2, v7.3.3).
- Tests for the CSS rules, the class registry, the starter instance and AG031.
- `VERSION` 7.4.0, `CHANGELOG.md`, a `MEMORY.md` record, `TODO.md`.

## iesdesk.com (APP-iesdesk)

- Vendor kit v7.4.0. It carries v7.3.2 and v7.3.3. IESDesk needs no change for them: its marketing header sets no `aria-current`, no view has a disabled link, and the marketing layout loads `agustos-chrome.js`.
- New partial `app/views/shared/_page_contents.html.erb`, with the local `items`: an array of `[id, label]` pairs. It renders the component with the English labels.
- `app/views/legal/privacy.html.erb` and `terms.html.erb` render the partial directly after their `header.iesdesk-hero`:
  - Privacy: `controller` Who is responsible, `data` The data we keep, and why, `retention` How long we keep data, `processors` Who else handles data, `transfers` Transfers abroad, `cookies` Cookies and browser storage, `rights` Your rights, `no-sale` No sale of data, `changes` Changes to this notice.
  - Terms: `beta` A free service in beta, `account` Your account, `files` Your files, `limits` Limits, `outputs` Outputs come with no warranty, `feedback` Feedback, `changes` Changes to these terms, `law` Law and courts, `contact` Contact.
- No text of the notice or the terms changes. No JavaScript changes.
- An integration test: on each page, each contents link points at a `section[id]`, and its label equals that section's `h2` text. Each `section[id]` directly under the container has one link.
- `AGENTS.md` design system section: one line for the component. `MEMORY.md` and `CHANGELOG.md`.

## agustos.com (WEBSITE-agustos)

- Vendor kit v7.4.0. It carries v7.3.2 and v7.3.3: copy the kit Astro adapter's `Header.astro`, `HeaderSearch.astro` and `HeaderUtility.astro` (a parent item on a nested route takes `aria-current="true"`), and fix each AG029 and AG030 finding of the checker.
- New component `src/components/PageContents.astro`, with the props `items` (`{ id, label }[]`) and `lang`. The label is "Bu sayfada" for `tr` and "On this page" for `en`.
- `src/pages/gizlilik-politikasi.astro`:
  - Give each `h2` an `id`: `veri-sorumlusu`, `islenen-veriler`, `toplama-yontemi`, `aktarim`, `saklama-suresi`, `haklariniz`, `satis-ve-paylasma`, `degisiklikler`.
  - Move the date line (`p.policy-updated`) out of `.policy-body` to directly after the `h1`, then render the component.
- `src/pages/en/privacy-policy.astro`: the same, with the ids `data-controller`, `data-we-process`, `collection-and-legal-grounds`, `sharing`, `retention`, `your-rights`, `sale-and-sharing`, `changes`.
- No copy changes and no URL changes.
- A test on the built pages: each contents link points at an existing `id`, and its label equals the heading text.
- `MEMORY.md` and `CHANGELOG.md`.

## Proof

For each of the four pages, in a browser:

| Check | Widths |
|---|---|
| The list sits in the side zone, level with the title, and stays in view to the end of the content | 1440, 1280 |
| At 1280x720, a list taller than the window scrolls inside itself | 1280x720 |
| The folded line opens and closes; the "+" and "−" change | 1024, 390 |
| A link jumps to its section, below the sticky header | 1440, 390 |
| The list never covers the footer or the closing band | 1440 |
| No width scrolls sideways | all |
| Tab reaches every link at 1280px and wider; the focus ring shows | 1440 |

Check the wide-screen layout in Chrome, Firefox and Safari 18.4 or later. Check the Safari fallback where an older Safari is available. Then run each repository's full gate: `scripts/ci.sh`, `bin/rails test` with `test:system` and `bin/ci`, and `npm run build`.

## Rollout

1. Kit PR, tag `v7.4.0`. Emre approved the preview on 2026-09-30, which counts as the before/after preview of the monthly-release rule.
2. The agustos.com PR goes live on merge.
3. The IESDesk PR reaches dev.iesdesk.com on merge. iesdesk.com gets it with the next release.

## Out of scope

- A marker on the current section while scrolling.
- Lists on short pages, blog posts, the cookie policies, About and Contact.
- Sub-heading items.
