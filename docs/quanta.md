# Quanta and Clara

Quanta is the experimental design system started for Volto as Pastanaga's
successor. Clara took its system structure, not its palette or namespace.

## Adopted

- primitive → semantic → component token layers;
- complete status roles (fill, text, surface, border, on-fill) for success,
  warning, danger and info;
- rhythmic spacing and motion scales;
- accessibility checks as code: `tests/test_color_contrast.py` measures the
  real sRGB values instead of trusting documented ratios.

## Kept from Clara

- `--plone-*` as the only public runtime API, `--clara-*` as the brand ladder;
- the official Plone logo blue `#0083be` as primary identity, with `#006293`
  for normal-size link text (exact blue is only 4.21:1 on white);
- a 16px body and a 15px label floor;
- Source Sans 3 and Literata;
- the fluid `--plone-space-*` scale and intrinsic layout primitives;
- flat, tonal depth with hairlines instead of shadows.

## Rejected

- a parallel `--quanta-*` API (guarded by `tests/test_token_drift.py`);
- Quanta's HSL cobalt, its 14px body and its Metropolis type;
- generic elevation and card components.
