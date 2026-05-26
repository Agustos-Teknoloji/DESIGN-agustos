---
title: Why we chose cream paper
deck: Raw web colors fight the substrate. Designed colors integrate with it.
date: 2026-05-08
lang: en
brand: agustos
---

The default web background is white. The default print background is, in practice, cream, paper has a hue, and that hue carries warmth that pure white doesn't.

We picked `#fefcf2` for the branded contexts of this system because it does two things at once: it signals "this is editorial, not a dashboard," and it asks every brand colour to be evaluated against a non-neutral substrate.

## What cream costs

Cream costs you the certainty that your raw brand colour will look right. The original Pataraz blue was `#0000FF`: the spec colour, the truest blue that exists in sRGB. On white, it's striking. On cream, it fights.

We refined it to `#1a24cc`. Slightly darker, slightly less saturated, tilted a touch warmer. Same blue identity, sitting with the paper instead of fighting it.

> Brand colours must be selected (or refined) for the cream substrate. Raw web colours fight the paper; designed colours integrate.
>
> <cite>Ağustos Design System v1.0 · Rule 4</cite>

## What cream gives you back

Three things:

1. A reason to design every colour, rather than picking from a swatch palette.
2. A default state that already feels published, not in-progress.
3. A consistent register across web, PDF, and docx, they all sit on the same paper.

The only contexts where we drop cream are working ones: email, dashboards, generic web. There the substrate is white, and the typography carries the brand on its own.

---

The `--paper` variable swaps in one line. Same tokens, same rules, different paper. It's the only structural choice the system asks you to make per page.
