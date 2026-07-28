# Quanta research and Clara integration

This directory records what `plonetheme.clara` learned from the experimental
Quanta design system for Volto. Quanta is a useful source of design-system
ideas; Clara does **not** ship Quanta as a second theme or runtime namespace.

## Current decision

Clara adopts:

- primitive → semantic → component token layers;
- complete, named interaction and status roles;
- rhythmic spacing and motion scales;
- atomic responsibility boundaries;
- accessibility validation as code.

Clara deliberately keeps:

- `--plone-*` as the only public runtime API;
- Plone's official logo blue `#0083be` as primary identity;
- a fixed 16px body and 15px minimum label tier;
- Source Sans 3 + Literata;
- Clara's fluid spacing scale and intrinsic layout primitives;
- flat tonal depth with no decorative shadows.

Clara rejects:

- a parallel `--quanta-*` API;
- Quanta's historical HSL cobalt as Clara's brand colour;
- a 14px body default;
- generic elevation/card patterns;
- copying historical contrast claims without measuring the actual colours.

## Canonical files

| Topic | Canonical source |
|---|---|
| Public token vocabulary and architecture | [`clara-theming-architecture.md`](clara-theming-architecture.md) |
| Clara identity and role decisions | [`../DESIGN.md`](../DESIGN.md) |
| Runtime defaults | [`../theme/scss/_clara-tokens-defaults.scss`](../theme/scss/_clara-tokens-defaults.scss) |
| Clara brand composition | [`../theme/scss/_clara-brand.scss`](../theme/scss/_clara-brand.scss) |
| Bootstrap compile literals | [`../theme/scss/_clara-tokens.scss`](../theme/scss/_clara-tokens.scss) |
| Component bridge | [`../theme/scss/_clara-bridge.scss`](../theme/scss/_clara-bridge.scss) |
| Semantic component states | [`../theme/scss/_clara-states.scss`](../theme/scss/_clara-states.scss) |
| Contrast guard | [`../tests/test_color_contrast.py`](../tests/test_color_contrast.py) |
| Literal/runtime drift guard | [`../tests/test_token_drift.py`](../tests/test_token_drift.py) |

There is intentionally no `_quanta-tokens.scss`: importing a second complete
token tree would violate Clara's customization contract.

## Research documents

- [`quanta-design-system.md`](quanta-design-system.md) — Quanta concepts and
  Clara's adopt/adapt/reject decisions.
- [`quanta-implementation-guide.md`](quanta-implementation-guide.md) — current
  production implementation and extension guide.
- [`quanta-SUMMARY.md`](quanta-SUMMARY.md) — concise findings.
- [`quanta-INDEX.md`](quanta-INDEX.md) — document map.

## Official upstream references

- [plone/quanta-icons](https://github.com/plone/quanta-icons)
- [plone/volto-quanta](https://github.com/plone/volto-quanta)
- [plone/volto-quanta-project](https://github.com/plone/volto-quanta-project)

Upstream Quanta remains experimental. Re-check its repositories before treating
an implementation detail as current Plone policy.
