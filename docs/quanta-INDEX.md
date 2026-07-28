# Quanta documentation index

The Quanta material in this package is research supporting Clara's own
`--plone-*` design language. Start with the current integration guide rather
than historical upstream snippets.

## Reading order

1. [`QUANTA_README.md`](QUANTA_README.md) — scope and current decision.
2. [`quanta-SUMMARY.md`](quanta-SUMMARY.md) — findings and corrections.
3. [`quanta-design-system.md`](quanta-design-system.md) — concept-by-concept
   adoption matrix.
4. [`quanta-implementation-guide.md`](quanta-implementation-guide.md) — actual
   Clara files, roles, component mappings and validation.
5. [`clara-theming-architecture.md`](clara-theming-architecture.md) — normative
   public contract.

## Source-of-truth hierarchy

When documents disagree, use this order:

1. Tests and compiled `clara.min.css`.
2. SCSS under `theme/scss/`.
3. `DESIGN.md` and `clara-theming-architecture.md`.
4. The Quanta research notes.
5. Upstream experimental examples.

## Key values

| Role | Value | Reason |
|---|---|---|
| Primary identity | `#0083be` | Exact official Plone logo blue |
| Normal link | `#006293` | Same hue; AA on every Clara light ground |
| On-primary | `#001018` | Same-hue near-black; AA on exact logo blue |
| Body | `1rem` | 16px content contract |
| Label floor | `0.9375rem` | Nothing renders below 15px |
| Public namespace | `--plone-*` | Shared pagelet/layout contract |
| Private brand namespace | `--clara-*` | Clara composition only |

## Important correction

Historical Quanta notes paired `hsl(207 90% 58%)` with RGB approximations and
contrast ratios that do not match the rendered colour. Clara never trusts those
figures. `tests/test_color_contrast.py` resolves and measures the exact shipped
hex values.

## No Quanta token bundle

There is intentionally no `theme/scss/_quanta-tokens.scss` and no public
`--quanta-*` API. Useful Quanta ideas have been integrated into Clara's existing
layers instead of copied wholesale.
