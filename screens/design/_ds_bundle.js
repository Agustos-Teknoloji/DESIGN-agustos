/* @ds-bundle: {"format":4,"namespace":"AUstosDesignSystem_7fee69","components":[{"name":"Button","sourcePath":"components/actions/Button.jsx"},{"name":"Link","sourcePath":"components/actions/Link.jsx"},{"name":"Badge","sourcePath":"components/content/Badge.jsx"},{"name":"Card","sourcePath":"components/content/Card.jsx"},{"name":"LazGunesi","sourcePath":"components/identity/LazGunesi.jsx"},{"name":"Lockup","sourcePath":"components/identity/Lockup.jsx"}],"sourceHashes":{"components/actions/Button.jsx":"110fef4fe046","components/actions/Link.jsx":"afbdef9ab725","components/content/Badge.jsx":"d1f835c9fe03","components/content/Card.jsx":"a455d36f6412","components/identity/LazGunesi.jsx":"a8a08b016f80","components/identity/Lockup.jsx":"2d6d13d882ba","ui_kits/iesdesk/app.jsx":"3728fa1ebe48","ui_kits/iesdesk/dashboard.jsx":"9a41c080d7f8","ui_kits/iesdesk/sidebar.jsx":"c229d1ef43e9","ui_kits/website/app.jsx":"75f8ab65d3f6","ui_kits/website/header.jsx":"510dcc42446f","ui_kits/website/hero.jsx":"6f03767a4fc0","ui_kits/website/sections.jsx":"186131bb1ab5","ui_kits/website/tweaks-panel.jsx":"6591467622ed"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.AUstosDesignSystem_7fee69 = window.AUstosDesignSystem_7fee69 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/actions/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Boxed action for lower-section CTAs and product UI. One size everywhere
   (44px min height, 6px radius, no shadow, no arrow — the arrow glyph is
   reserved for text links). Filled black is the committing action and never
   changes color on hover; outline is the real alternative and fills black
   with a white label on hover. 'brand' is a filled-RED variant reserved for
   the one approved exception: a dark-theme hero's primary CTA — never use it
   on a white/light surface. */

function Button({
  children,
  variant = 'outline',
  // 'primary' (ink fill) | 'brand' (red fill — dark-hero exception only) | 'outline' | 'ghost'
  as = 'button',
  href,
  style,
  ...rest
}) {
  const Tag = href ? 'a' : as;
  const base = {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5em',
    fontFamily: 'var(--display)',
    fontWeight: 600,
    fontSize: 15,
    lineHeight: 1,
    textDecoration: 'none',
    cursor: 'pointer',
    padding: '0.7em 1.1em',
    minHeight: 44,
    boxSizing: 'border-box',
    borderRadius: 'var(--radius-md)',
    border: '1px solid transparent',
    transition: 'background var(--dur) var(--ease), color var(--dur) var(--ease), border-color var(--dur) var(--ease)',
    background: 'transparent',
    color: 'var(--ink)'
  };
  const variants = {
    primary: {
      background: 'var(--ink)',
      color: 'var(--paper-white)',
      borderColor: 'var(--ink)'
    },
    brand: {
      background: 'var(--red)',
      color: 'var(--white)',
      borderColor: 'var(--red)'
    },
    outline: {
      background: 'transparent',
      color: 'var(--ink)',
      borderColor: 'var(--ink)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--ink-soft)',
      borderColor: 'transparent'
    }
  };
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: `ds-btn ds-btn--${variant}`,
    href: href,
    style: {
      ...base,
      ...variants[variant],
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/Button.jsx", error: String((e && e.message) || e) }); }

// components/actions/Link.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* The content link — one of the two places red is allowed: a permanent 2px
   red rule. Ink at rest; ink turns red on hover, the rule stays put. Never
   use for navigation/menu items — those are plain labels (see base.css
   .plain-label), which show the red rule only on hover/current. */

function Link({
  children,
  variant = 'primary',
  // 'primary' (ink) | 'secondary' (ink-soft)
  arrow = false,
  href = '#',
  style,
  ...rest
}) {
  const color = variant === 'secondary' ? 'var(--ink-soft)' : 'var(--ink)';
  const weight = variant === 'secondary' ? 500 : 600;
  return /*#__PURE__*/React.createElement("a", _extends({
    href: href,
    className: `ds-link ds-link--${variant}`,
    style: {
      color,
      fontWeight: weight,
      fontFamily: arrow ? 'var(--display)' : 'inherit',
      textDecoration: 'none',
      display: arrow ? 'inline-flex' : 'inline',
      alignItems: 'baseline',
      gap: '0.4em',
      backgroundImage: 'linear-gradient(var(--red), var(--red))',
      backgroundSize: '100% 2px',
      backgroundPosition: '0 calc(100% - 1px)',
      backgroundRepeat: 'no-repeat',
      paddingBottom: 3,
      transition: 'color var(--dur) var(--ease)',
      ...style
    },
    onMouseEnter: e => {
      e.currentTarget.style.color = 'var(--red)';
      rest.onMouseEnter && rest.onMouseEnter(e);
    },
    onMouseLeave: e => {
      e.currentTarget.style.color = color;
      rest.onMouseLeave && rest.onMouseLeave(e);
    }
  }, rest), children, arrow && /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true"
  }, "\u2192"));
}
Object.assign(__ds_scope, { Link });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/Link.jsx", error: String((e && e.message) || e) }); }

// components/content/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Small sentence-case label — meta, status, categories. Red is never a
   badge's own colour (it is not a content link or a menu item), so variants
   stay within the ink scale: neutral (hairline outline) and solid (ink
   fill). No uppercase, no wide tracking. */

function Badge({
  children,
  variant = 'neutral',
  // 'neutral' | 'solid'
  style,
  ...rest
}) {
  const variants = {
    neutral: {
      color: 'var(--ink-soft)',
      border: '1px solid var(--rule)',
      background: 'transparent'
    },
    solid: {
      color: 'var(--paper-white)',
      border: '1px solid var(--ink)',
      background: 'var(--ink)'
    }
  };
  return /*#__PURE__*/React.createElement("span", _extends({
    className: `ds-badge ds-badge--${variant}`,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      fontFamily: 'var(--display)',
      fontSize: 12.5,
      fontWeight: 600,
      textTransform: 'none',
      letterSpacing: 0,
      lineHeight: 1,
      padding: '0.45em 0.7em',
      borderRadius: 'var(--radius-sm)',
      whiteSpace: 'nowrap',
      ...variants[variant],
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Badge.jsx", error: String((e && e.message) || e) }); }

// components/content/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Editorial surface card. White-on-white with a hairline rule, 10px radius,
   no shadow. Optional left rule (marked) uses ink, not red — red never
   decorates a card. */

function Card({
  children,
  eyebrow,
  title,
  marked = false,
  // adds a 2px ink rule on the leading edge
  as = 'article',
  style,
  ...rest
}) {
  const Tag = as;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: `ds-card${marked ? ' ds-card--marked' : ''}`,
    style: {
      background: 'var(--paper-white)',
      border: '1px solid var(--rule)',
      borderLeft: marked ? '2px solid var(--ink)' : '1px solid var(--rule)',
      borderRadius: 'var(--radius-lg)',
      padding: '24px 26px',
      ...style
    }
  }, rest), eyebrow && /*#__PURE__*/React.createElement("div", {
    className: "type-h4",
    style: {
      margin: 0
    }
  }, eyebrow), title && /*#__PURE__*/React.createElement("h3", {
    className: "type-h2",
    style: {
      margin: eyebrow ? '0.6em 0 0' : 0,
      fontSize: 20
    }
  }, title), children && /*#__PURE__*/React.createElement("div", {
    className: "type-body",
    style: {
      margin: eyebrow || title ? '0.6em 0 0' : 0,
      fontSize: 15
    }
  }, children));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Card.jsx", error: String((e && e.message) || e) }); }

// components/identity/LazGunesi.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* Laz Güneşi — the publisher's mark. 18 swirling blades, rotational sun.
   Geometry extracted verbatim from the official Illustrator artwork
   (laz-gunesi-amblem.pdf) — two cubic Béziers per blade. One symbol, forever;
   every brand carries it in brand color. Fills with currentColor so it inherits
   --brand (or any color) from its context. Mirrors assets/laz-gunesi.svg. */

const INNER = `<g>
<path d="M 49.98 28.47 C 49.83 19.48 60.99 4.73 78.18 14.04 C 64.81 13.93 53.64 19.06 49.98 28.47 Z"/>
<path d="M 42.61 29.77 C 39.4 21.37 44.84 3.69 64.18 6.57 C 51.58 11.04 42.83 19.68 42.61 29.77 Z"/>
<path d="M 36.14 33.51 C 30.25 26.72 29.31 8.25 48.47 4.34 C 38.16 12.85 32.89 23.96 36.14 33.51 Z"/>
<path d="M 31.34 39.25 C 23.48 34.88 16.28 17.84 32.94 7.62 C 26.16 19.14 25.02 31.38 31.34 39.25 Z"/>
<path d="M 28.79 46.28 C 19.91 44.87 7.32 31.31 19.48 16.01 C 17.05 29.15 20.15 41.05 28.79 46.28 Z"/>
<path d="M 28.79 53.76 C 19.97 55.47 3.5 47.04 9.69 28.49 C 11.9 41.68 18.89 51.79 28.79 53.76 Z"/>
<path d="M 31.36 60.79 C 23.65 65.41 5.29 63.12 4.77 43.58 C 11.36 55.21 21.38 62.32 31.36 60.79 Z"/>
<path d="M 36.17 66.51 C 30.51 73.49 12.48 77.62 5.3 59.43 C 15.47 68.11 27.32 71.37 36.17 66.51 Z"/>
<path d="M 42.65 70.24 C 39.72 78.74 24.19 88.79 11.22 74.15 C 23.75 78.83 36 77.84 42.65 70.24 Z"/>
<path d="M 50.02 71.54 C 50.17 80.53 39.01 95.28 21.82 85.96 C 35.19 86.07 46.37 80.95 50.02 71.54 Z"/>
<path d="M 57.39 70.23 C 60.6 78.63 55.16 96.31 35.82 93.43 C 48.42 88.96 57.17 80.32 57.39 70.23 Z"/>
<path d="M 63.86 66.48 C 69.75 73.27 70.69 91.75 51.53 95.66 C 61.84 87.15 67.11 76.04 63.86 66.48 Z"/>
<path d="M 68.66 60.75 C 76.52 65.11 83.72 82.16 67.06 92.38 C 73.84 80.86 74.98 68.62 68.66 60.75 Z"/>
<path d="M 71.21 53.72 C 80.09 55.13 92.68 68.68 80.52 83.99 C 82.95 70.84 79.85 58.95 71.21 53.72 Z"/>
<path d="M 71.21 46.24 C 80.03 44.53 96.5 52.96 90.31 71.5 C 88.1 58.32 81.11 48.2 71.21 46.24 Z"/>
<path d="M 68.64 39.21 C 76.35 34.59 94.71 36.88 95.23 56.42 C 88.64 44.78 78.62 37.67 68.64 39.21 Z"/>
<path d="M 63.83 33.49 C 69.49 26.5 87.52 22.37 94.7 40.56 C 84.53 31.88 72.68 28.63 63.83 33.49 Z"/>
<path d="M 57.34 29.75 C 60.28 21.25 75.81 11.21 88.78 25.84 C 76.25 21.16 64 22.16 57.34 29.75 Z"/>
</g>`;
function LazGunesi({
  size = '1em',
  color,
  title = 'Laz Güneşi',
  style,
  ...rest
}) {
  return /*#__PURE__*/React.createElement("svg", _extends({
    viewBox: "0 0 100 100",
    width: size,
    height: size,
    role: "img",
    "aria-label": title,
    style: {
      fill: color || 'currentColor',
      display: 'block',
      ...style
    },
    dangerouslySetInnerHTML: {
      __html: INNER
    }
  }, rest));
}
Object.assign(__ds_scope, { LazGunesi });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/identity/LazGunesi.jsx", error: String((e && e.message) || e) }); }

// components/identity/Lockup.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* The publisher lockup: symbol + lowercase wordmark, both in brand color so
   the mark reads as one unit. Identity, not a link — quiet hover, no underline. */

const WORDMARKS = {
  agustos: 'ağustos',
  pataraz: 'pataraz',
  pld: 'pld türkiye',
  iesdesk: 'iesdesk',
  specquick: 'specquick'
};
function Lockup({
  brand = 'agustos',
  name,
  size = 24,
  mono = false,
  as = 'span',
  href,
  style,
  ...rest
}) {
  const wordmark = name || WORDMARKS[brand] || brand;
  const Tag = href ? 'a' : as;
  const color = mono ? 'var(--ink)' : 'var(--brand)';
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: `lockup brand-${brand}${mono ? ' lockup--mono' : ''}`,
    href: href,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.4em',
      fontSize: size,
      textDecoration: 'none',
      color,
      ...style
    },
    "aria-label": wordmark
  }, rest), /*#__PURE__*/React.createElement("span", {
    className: "lockup__symbol",
    style: {
      width: '1.4em',
      height: '1.4em',
      flex: 'none',
      transform: 'translateY(0.08em)',
      color: 'inherit'
    }
  }, /*#__PURE__*/React.createElement(__ds_scope.LazGunesi, {
    size: "100%"
  })), /*#__PURE__*/React.createElement("span", {
    className: "lockup__name",
    style: {
      fontFamily: 'var(--display)',
      fontWeight: 650,
      letterSpacing: 0,
      textTransform: 'lowercase',
      lineHeight: 1,
      color: 'inherit'
    }
  }, wordmark));
}
Object.assign(__ds_scope, { Lockup });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/identity/Lockup.jsx", error: String((e && e.message) || e) }); }

// ui_kits/iesdesk/app.jsx
try { (() => {
/* app.jsx — composes IESDesk. White substrate always (product UI never uses
   the cream band — that's a marketing-site-only surface), opt-in warm dark
   via data-theme on <html>. Brand scope is iesdesk — off-black, like every
   secondary brand; accents below use ink/surface, never colour. */

function PqApp() {
  const [view, setView] = React.useState('validation');
  const [theme, setTheme] = React.useState('light');
  React.useEffect(() => {
    if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');else document.documentElement.removeAttribute('data-theme');
  }, [theme]);
  return /*#__PURE__*/React.createElement("div", {
    className: "pq brand-iesdesk"
  }, /*#__PURE__*/React.createElement("a", {
    className: "skip-link",
    href: "#pq-main"
  }, "Skip to content"), /*#__PURE__*/React.createElement(window.PqSidebar, {
    view: view,
    setView: setView,
    theme: theme,
    setTheme: setTheme
  }), /*#__PURE__*/React.createElement("div", {
    id: "pq-main",
    className: "pq-stage"
  }, /*#__PURE__*/React.createElement(window.PqDashboard, {
    view: view
  })));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(PqApp, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/iesdesk/app.jsx", error: String((e && e.message) || e) }); }

// ui_kits/iesdesk/dashboard.jsx
try { (() => {
/* dashboard.jsx — IESDesk main views: topbar, stat tiles, and the validation
   table. Numbers use the display family + tabular figures (the "dashboard
   numerals" role). Status is carried by text + glyph, never colour alone —
   there is no brand hue to lean on here, so "Valid" is a solid ink pill;
   everything else is ink on white. */
const {
  Button,
  Badge,
  Link
} = window.AUstosDesignSystem_7fee69;
function Status({
  kind
}) {
  if (kind === 'valid') return /*#__PURE__*/React.createElement(Badge, {
    variant: "solid"
  }, "\u2713 Valid");
  if (kind === 'flagged') return /*#__PURE__*/React.createElement("span", {
    className: "pq-status pq-status--flag"
  }, "\u26A0 Flagged");
  if (kind === 'error') return /*#__PURE__*/React.createElement("span", {
    className: "pq-status pq-status--err"
  }, "\u2715 Error");
  return /*#__PURE__*/React.createElement("span", {
    className: "pq-status pq-status--skip"
  }, "\u2013 Skipped");
}
const STATS = [{
  label: 'Files in batch',
  value: '4,218',
  sub: 'IES · LDT'
}, {
  label: 'Valid',
  value: '4,061',
  sub: '96.3% pass',
  featured: true
}, {
  label: 'Flagged',
  value: '157',
  sub: '142 fixable'
}, {
  label: 'Median efficacy',
  value: '118',
  sub: 'lm / W'
}];
const ROWS = [{
  file: 'osram-kreios-g3-840.ies',
  fmt: 'IES',
  flux: '3,240',
  eff: '129',
  beam: '38°',
  status: 'valid'
}, {
  file: 'pataraz-linea-spot-927.ldt',
  fmt: 'LDT',
  flux: '1,180',
  eff: '112',
  beam: '24°',
  status: 'valid'
}, {
  file: 'pataraz-run-2700k.ldt',
  fmt: 'LDT',
  flux: '4,860',
  eff: '121',
  beam: '—',
  status: 'valid'
}, {
  file: 'erco-optec-spot-30.ies',
  fmt: 'IES',
  flux: '2,010',
  eff: '—',
  beam: '30°',
  status: 'flagged'
}, {
  file: 'generic-panel-600x600.ies',
  fmt: 'IES',
  flux: '3,600',
  eff: '108',
  beam: '—',
  status: 'valid'
}, {
  file: 'unnamed-export-0042.ldt',
  fmt: 'LDT',
  flux: '—',
  eff: '—',
  beam: '—',
  status: 'error'
}, {
  file: 'pataraz-qu0-fixed-930.ies',
  fmt: 'IES',
  flux: '1,540',
  eff: '124',
  beam: '15°',
  status: 'valid'
}, {
  file: 'tracklight-batch-legacy.ldt',
  fmt: 'LDT',
  flux: '2,720',
  eff: '96',
  beam: '40°',
  status: 'flagged'
}];
function StatTile({
  s
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: 'pq-stat' + (s.featured ? ' pq-stat--featured' : '')
  }, /*#__PURE__*/React.createElement("div", {
    className: "type-h4 pq-stat__label"
  }, s.label), /*#__PURE__*/React.createElement("div", {
    className: "pq-stat__value pq-num"
  }, s.value), /*#__PURE__*/React.createElement("div", {
    className: "pq-stat__sub"
  }, s.sub));
}
function PqDashboard({
  view
}) {
  return /*#__PURE__*/React.createElement("section", {
    className: "pq-main"
  }, /*#__PURE__*/React.createElement("header", {
    className: "pq-topbar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-topbar__lead"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-crumb"
  }, /*#__PURE__*/React.createElement("span", null, "Batches"), /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true",
    className: "pq-crumb__sep"
  }, "/"), /*#__PURE__*/React.createElement("span", {
    className: "pq-crumb__here"
  }, "catalogue-2026-q2")), /*#__PURE__*/React.createElement("h1", {
    className: "type-h1 pq-topbar__title"
  }, "Validation run")), /*#__PURE__*/React.createElement("div", {
    className: "pq-topbar__actions"
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "ghost"
  }, "Re-run"), /*#__PURE__*/React.createElement(Button, {
    variant: "primary"
  }, "Export dataset"))), /*#__PURE__*/React.createElement("div", {
    className: "pq-scroll"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-progress"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-progress__head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "type-h4"
  }, "Processing complete"), /*#__PURE__*/React.createElement("span", {
    className: "pq-num pq-progress__pct"
  }, "4,218 / 4,218")), /*#__PURE__*/React.createElement("div", {
    className: "pq-progress__track"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-progress__fill",
    style: {
      width: '100%'
    }
  })), /*#__PURE__*/React.createElement("p", {
    className: "pq-progress__note"
  }, "Parsed locally in 11.4s \xB7 LM-63 + EULUMDAT \xB7 units normalized to SI.")), /*#__PURE__*/React.createElement("div", {
    className: "pq-stats"
  }, STATS.map(s => /*#__PURE__*/React.createElement(StatTile, {
    key: s.label,
    s: s
  }))), /*#__PURE__*/React.createElement("div", {
    className: "pq-table-head"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "type-h2 pq-table-title"
  }, "Files"), /*#__PURE__*/React.createElement("div", {
    className: "pq-table-tools"
  }, /*#__PURE__*/React.createElement("span", {
    className: "pq-filter is-active"
  }, "All"), /*#__PURE__*/React.createElement("span", {
    className: "pq-filter"
  }, "Flagged"), /*#__PURE__*/React.createElement("span", {
    className: "pq-filter"
  }, "Errors"), /*#__PURE__*/React.createElement(Link, {
    href: "#",
    variant: "secondary"
  }, "Download report"))), /*#__PURE__*/React.createElement("div", {
    className: "pq-table",
    role: "table",
    "aria-label": "Validation results"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-tr pq-tr--head",
    role: "row"
  }, /*#__PURE__*/React.createElement("span", {
    role: "columnheader"
  }, "File"), /*#__PURE__*/React.createElement("span", {
    role: "columnheader"
  }, "Format"), /*#__PURE__*/React.createElement("span", {
    role: "columnheader",
    className: "pq-r"
  }, "Flux (lm)"), /*#__PURE__*/React.createElement("span", {
    role: "columnheader",
    className: "pq-r"
  }, "Efficacy (lm/W)"), /*#__PURE__*/React.createElement("span", {
    role: "columnheader",
    className: "pq-r"
  }, "Beam"), /*#__PURE__*/React.createElement("span", {
    role: "columnheader"
  }, "Status")), ROWS.map(r => /*#__PURE__*/React.createElement("div", {
    className: "pq-tr",
    role: "row",
    key: r.file
  }, /*#__PURE__*/React.createElement("span", {
    role: "cell",
    className: "pq-file"
  }, /*#__PURE__*/React.createElement("code", null, r.file)), /*#__PURE__*/React.createElement("span", {
    role: "cell",
    className: "pq-fmt"
  }, r.fmt), /*#__PURE__*/React.createElement("span", {
    role: "cell",
    className: "pq-r pq-num"
  }, r.flux), /*#__PURE__*/React.createElement("span", {
    role: "cell",
    className: "pq-r pq-num"
  }, r.eff), /*#__PURE__*/React.createElement("span", {
    role: "cell",
    className: "pq-r pq-num"
  }, r.beam), /*#__PURE__*/React.createElement("span", {
    role: "cell"
  }, /*#__PURE__*/React.createElement(Status, {
    kind: r.status
  })))))));
}
window.PqDashboard = PqDashboard;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/iesdesk/dashboard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/iesdesk/sidebar.jsx
try { (() => {
/* sidebar.jsx — IESDesk product sidebar.
   Lockup (iesdesk, off-black) + functional nav + storage meter + theme toggle.
   Product UI: white/dark substrate. No brand hue to ration — accents are
   ink and the light-gray functional surface instead. */
const {
  Lockup
} = window.AUstosDesignSystem_7fee69;
const NAV = [{
  id: 'batches',
  label: 'Batches',
  glyph: '▦',
  count: 6
}, {
  id: 'files',
  label: 'Files',
  glyph: '≣',
  count: '4,218'
}, {
  id: 'validation',
  label: 'Validation',
  glyph: '◬',
  count: 157
}, {
  id: 'exports',
  label: 'Exports',
  glyph: '↧',
  count: 12
}, {
  id: 'formats',
  label: 'Formats',
  glyph: '⌗'
}];
function PqSidebar({
  view,
  setView,
  theme,
  setTheme
}) {
  return /*#__PURE__*/React.createElement("aside", {
    className: "pq-side"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-side__brand"
  }, /*#__PURE__*/React.createElement(Lockup, {
    brand: "iesdesk",
    size: 19
  })), /*#__PURE__*/React.createElement("nav", {
    className: "pq-nav",
    "aria-label": "Primary"
  }, NAV.map(n => /*#__PURE__*/React.createElement("button", {
    key: n.id,
    className: 'pq-nav__item' + (n.id === view ? ' is-active' : ''),
    onClick: () => setView(n.id),
    "aria-current": n.id === view ? 'page' : undefined
  }, /*#__PURE__*/React.createElement("span", {
    className: "pq-nav__glyph",
    "aria-hidden": "true"
  }, n.glyph), /*#__PURE__*/React.createElement("span", {
    className: "pq-nav__label"
  }, n.label), n.count != null && /*#__PURE__*/React.createElement("span", {
    className: "pq-nav__count"
  }, n.count)))), /*#__PURE__*/React.createElement("div", {
    className: "pq-side__foot"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-meter",
    "aria-label": "Local cache"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-meter__head"
  }, /*#__PURE__*/React.createElement("span", null, "Local cache"), /*#__PURE__*/React.createElement("span", {
    className: "pq-num"
  }, "1.8 / 4 GB")), /*#__PURE__*/React.createElement("div", {
    className: "pq-meter__track"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pq-meter__fill",
    style: {
      width: '45%'
    }
  })), /*#__PURE__*/React.createElement("p", {
    className: "pq-side__note"
  }, "Files never leave this machine.")), /*#__PURE__*/React.createElement("button", {
    className: "pq-theme",
    onClick: () => setTheme(theme === 'dark' ? 'light' : 'dark'),
    "aria-pressed": theme === 'dark'
  }, /*#__PURE__*/React.createElement("span", {
    "aria-hidden": "true"
  }, theme === 'dark' ? '☾' : '☀'), theme === 'dark' ? 'Dark' : 'Light')));
}
window.PqSidebar = PqSidebar;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/iesdesk/sidebar.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/app.jsx
try { (() => {
/* app.jsx — composes the Ağustos marketing site. Per-brand content map
   demonstrates the multi-brand axis: same structure, name flexes (colour is
   fixed to the publisher — see colors.css). White substrate always; cream
   is the one full-bleed band inside SiteBand. */

const SITE = {
  agustos: {
    nav: ['Work', 'Services', 'Catalogue', 'Studio'],
    headline: 'Light, placed with intent.',
    deck: 'Ağustos Teknoloji designs, specifies, and distributes architectural lighting — from the photometric study to the fixture on site.',
    primary: ['See selected work', 'Browse the catalogue'],
    secondary: 'Talk to the studio',
    trust: '2009–2026 · 240+ projects across Türkiye · partner to leading European luminaire makers',
    sectionTitle: 'Selected work',
    sectionLink: 'All projects',
    items: [{
      kind: 'Cultural',
      title: 'A museum, relit',
      body: 'Gallery-grade tunable white and a concealed track system for a restored Ottoman hall.'
    }, {
      kind: 'Retail',
      title: 'Flagship, Nişantaşı',
      body: 'Accent and ambient layers tuned to the merchandise, commissioned on site.'
    }, {
      kind: 'Workplace',
      title: 'HQ, Maslak',
      body: 'Low-glare UGR<19 office field with daylight-linked dimming throughout.'
    }],
    bandQuote: 'One symbol, forever.',
    bandBody: 'Every project ships with its photometric study, IES files, and a commissioning report. The work is documented as carefully as it is designed.',
    bandCta: 'Request pricing',
    bandLink: 'Download a sample dossier',
    footerNote: 'Ağustos Teknoloji · architectural lighting, agency & distribution · İstanbul, Türkiye.',
    legal: {
      label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(),
      href: 'https://agustos.com'
    },
    copyright: {
      label: '© Ağustos Teknoloji',
      href: 'https://agustos.com'
    },
    footerCols: [{
      title: 'Work',
      links: ['Projects', 'Sectors', 'Process']
    }, {
      title: 'Trade',
      links: ['Catalogue', 'IES files', 'Become a partner']
    }, {
      title: 'Studio',
      links: ['About', 'Contact', 'Careers']
    }]
  },
  pataraz: {
    nav: ['Luminaires', 'Collections', 'Specs', 'Where to buy'],
    headline: 'Luminaires, made premium.',
    deck: 'Pataraz builds architectural-grade fixtures with the optics and finish of the imports — at a price that specifies on real projects.',
    primary: ['Explore collections', 'Download specs'],
    secondary: 'Find a distributor',
    trust: 'CRI 90+ · 5-year warranty · TSE & CE certified · stocked in İstanbul and Ankara',
    sectionTitle: 'Collections',
    sectionLink: 'Full range',
    items: [{
      kind: 'Track',
      title: 'Pataraz Linea',
      body: '48V magnetic track with interchangeable spot, flood, and linear modules.'
    }, {
      kind: 'Downlight',
      title: 'Pataraz Qu0',
      body: 'Deep-baffle anti-glare downlight, fixed and adjustable, three beam angles.'
    }, {
      kind: 'Linear',
      title: 'Pataraz Run',
      body: 'Continuous recessed and surface runs with seamless joints and diffusers.'
    }],
    bandQuote: 'Optics first.',
    bandBody: 'Each fixture is published with full photometric data and IES files. Specify with confidence; commission without surprises.',
    bandCta: 'Request a sample',
    bandLink: 'View the spec library',
    footerNote: 'Pataraz · premium architectural luminaires · a brand from Emre\u2019s house.',
    legal: {
      label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(),
      href: 'https://pataraz.com'
    },
    copyright: {
      label: '© Pataraz',
      href: 'https://pataraz.com'
    },
    footerCols: [{
      title: 'Range',
      links: ['Track', 'Downlights', 'Linear']
    }, {
      title: 'Specify',
      links: ['IES files', 'Datasheets', 'BIM objects']
    }, {
      title: 'Trade',
      links: ['Distributors', 'Warranty', 'Contact']
    }]
  },
  pld: {
    nav: ['Archive', 'Issues', 'Index', 'About'],
    headline: 'The record of light in Türkiye.',
    deck: 'PLD Türkiye is the standing archive of professional lighting design — projects, people, and writing, kept in one place.',
    primary: ['Read the archive', 'Browse by issue'],
    secondary: 'Submit a project',
    trust: 'Est. 2014 · 48 issues · 600+ documented projects · open editorial index',
    sectionTitle: 'From the archive',
    sectionLink: 'All issues',
    items: [{
      kind: 'Essay',
      title: 'On glare, again',
      body: 'Why UGR keeps failing the rooms it is supposed to protect — a field reading.'
    }, {
      kind: 'Project',
      title: 'A mosque, after dark',
      body: 'Documenting a restrained exterior scheme that resists the floodlight reflex.'
    }, {
      kind: 'Interview',
      title: 'The specifier\u2019s desk',
      body: 'A working lighting designer on what survives between render and reality.'
    }],
    bandQuote: 'Kept, not lost.',
    bandBody: 'The archive is editorial, not promotional. Every entry carries its date, its credits, and its place in the record.',
    bandCta: 'Subscribe',
    bandLink: 'See the editorial index',
    footerNote: 'PLD Türkiye · professional lighting design, archived · independent publication.',
    legal: {
      label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(),
      href: 'https://pldturkiye.com'
    },
    copyright: {
      label: '© PLD Türkiye',
      href: 'https://pldturkiye.com'
    },
    footerCols: [{
      title: 'Read',
      links: ['Latest', 'Issues', 'Index']
    }, {
      title: 'Contribute',
      links: ['Submit', 'Pitch an essay', 'Credits']
    }, {
      title: 'About',
      links: ['Masthead', 'Ethics', 'Contact']
    }]
  },
  iesdesk: {
    nav: ['Product', 'Docs', 'Pricing', 'Changelog'],
    headline: 'Photometric data, batched.',
    deck: 'IESDesk reads, validates, and converts IES and LDT files at scale — so a 4,000-fixture catalogue becomes one clean dataset.',
    primary: ['Start a batch', 'Read the docs'],
    secondary: 'See pricing',
    trust: 'IES LM-63 · EULUMDAT · CIE outputs · runs locally, no upload required',
    sectionTitle: 'What it does',
    sectionLink: 'Full feature list',
    items: [{
      kind: 'Ingest',
      title: 'Read anything',
      body: 'Parse IES and LDT in bulk, flag malformed files, and normalize units automatically.'
    }, {
      kind: 'Validate',
      title: 'Catch errors early',
      body: 'Photometric sanity checks: flux, efficacy, symmetry, and angle coverage.'
    }, {
      kind: 'Export',
      title: 'Clean datasets',
      body: 'Emit CSV, JSON, and converted formats with consistent metadata across the set.'
    }],
    bandQuote: 'Trust the dataset.',
    bandBody: 'Everything runs on your machine. Files never leave the room; the only thing that leaves is a clean, documented export.',
    bandCta: 'Download for desktop',
    bandLink: 'View a sample report',
    footerNote: 'IESDesk · lighting-data tooling · part of Emre\u2019s house.',
    legal: {
      label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(),
      href: 'https://iesdesk.com'
    },
    copyright: {
      label: '© IESDesk',
      href: 'https://iesdesk.com'
    },
    footerCols: [{
      title: 'Product',
      links: ['Features', 'Formats', 'Changelog']
    }, {
      title: 'Developers',
      links: ['Docs', 'CLI', 'API']
    }, {
      title: 'Company',
      links: ['Pricing', 'Support', 'Contact']
    }]
  },
  specquick: {
    nav: ['Product', 'Templates', 'Pricing', 'Changelog'],
    headline: 'A spec sheet, in a minute.',
    deck: 'SpecQuick turns a product\u2019s photometric and mechanical data into a print-ready, on-brand spec sheet — no layout work required.',
    primary: ['Generate a sheet', 'See templates'],
    secondary: 'See pricing',
    trust: 'A4 & Letter · exports to PDF · matches every brand in the portfolio automatically',
    sectionTitle: 'What it does',
    sectionLink: 'Full feature list',
    items: [{
      kind: 'Template',
      title: 'One layout, any brand',
      body: 'A single spec-sheet template resolves to the correct brand mark and colour automatically.'
    }, {
      kind: 'Data',
      title: 'Pull from IESDesk',
      body: 'Photometric figures come straight from a validated IESDesk dataset — no retyping.'
    }, {
      kind: 'Export',
      title: 'Print-ready PDF',
      body: 'Fixed A4/Letter output, ready to attach to a quote or submit to a specifier.'
    }],
    bandQuote: 'Documented, not designed twice.',
    bandBody: 'The sheet a specifier receives is generated from the same dataset the fixture was validated against — never a separate, hand-built document.',
    bandCta: 'Generate a sheet',
    bandLink: 'View a sample sheet',
    footerNote: 'SpecQuick · spec-sheet tooling · part of Emre\u2019s house.',
    legal: {
      label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(),
      href: 'https://specquick.com'
    },
    copyright: {
      label: '© SpecQuick',
      href: 'https://specquick.com'
    },
    footerCols: [{
      title: 'Product',
      links: ['Features', 'Templates', 'Changelog']
    }, {
      title: 'Developers',
      links: ['Docs', 'API']
    }, {
      title: 'Company',
      links: ['Pricing', 'Support', 'Contact']
    }]
  }
};
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "layout": "sidebar",
  "heroScale": "medium"
} /*EDITMODE-END*/;
function App() {
  const {
    useTweaks,
    TweaksPanel,
    TweakSection,
    TweakRadio
  } = window;
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [brand, setBrand] = React.useState('agustos');
  const [theme, setTheme] = React.useState('light');
  const data = SITE[brand];
  const isSidebar = t.layout === 'sidebar';
  const content = /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("main", {
    id: "main"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-main"
  }, /*#__PURE__*/React.createElement(window.SiteHero, {
    data: data,
    scale: t.heroScale
  }), /*#__PURE__*/React.createElement(window.SiteWork, {
    data: data
  })), /*#__PURE__*/React.createElement(window.SiteBand, {
    data: data
  })), !isSidebar && /*#__PURE__*/React.createElement(window.SiteFooter, {
    brand: brand,
    data: data
  }));
  const cls = 'wk brand-' + brand + (isSidebar ? ' wk--sidebar' : '');
  return /*#__PURE__*/React.createElement("div", {
    className: cls,
    "data-theme": theme === 'dark' ? 'dark' : undefined
  }, /*#__PURE__*/React.createElement("a", {
    className: "skip-link",
    href: "#main"
  }, "Skip to content"), isSidebar ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(window.SiteSidebar, {
    brand: brand,
    setBrand: setBrand,
    nav: data.nav,
    legal: data.legal,
    theme: theme,
    setTheme: setTheme
  }), /*#__PURE__*/React.createElement("div", {
    className: "wk-shell"
  }, content)) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(window.SiteHeader, {
    brand: brand,
    setBrand: setBrand,
    nav: data.nav
  }), content), /*#__PURE__*/React.createElement(TweaksPanel, null, /*#__PURE__*/React.createElement(TweakSection, {
    label: "Layout"
  }), /*#__PURE__*/React.createElement(TweakRadio, {
    label: "Navigation",
    value: t.layout,
    options: ['topbar', 'sidebar'],
    onChange: v => setTweak('layout', v)
  }), /*#__PURE__*/React.createElement(TweakSection, {
    label: "Hero"
  }), /*#__PURE__*/React.createElement(TweakRadio, {
    label: "Headline scale",
    value: t.heroScale,
    options: ['medium', 'large'],
    onChange: v => setTweak('heroScale', v)
  })));
}
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/app.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/header.jsx
try { (() => {
/* header.jsx — site header: lockup + editorial nav + brand switcher.
   The switcher demonstrates the multi-brand axis (name only — colour is
   fixed to the publisher). Nav items are plain labels: the red rule reveals
   only on hover / the current item (see .plain-label in base.css). */
const {
  Lockup,
  Button
} = window.AUstosDesignSystem_7fee69;
const BRANDS = [{
  slug: 'agustos',
  name: 'ağustos'
}, {
  slug: 'pataraz',
  name: 'pataraz'
}, {
  slug: 'pld',
  name: 'pld türkiye'
}, {
  slug: 'iesdesk',
  name: 'iesdesk'
}, {
  slug: 'specquick',
  name: 'specquick'
}];
function SiteHeader({
  brand,
  setBrand,
  nav
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "wk-header"
  }, /*#__PURE__*/React.createElement("a", {
    className: "lockup",
    href: "#",
    "aria-label": "home"
  }, /*#__PURE__*/React.createElement(Lockup, {
    brand: brand,
    size: 22
  })), /*#__PURE__*/React.createElement("nav", {
    className: "wk-nav wk-nav--center",
    "aria-label": "Primary"
  }, nav.map(n => /*#__PURE__*/React.createElement("a", {
    key: n,
    className: "wk-nav__link plain-label",
    href: "#"
  }, n))), /*#__PURE__*/React.createElement("div", {
    className: "wk-switch",
    role: "group",
    "aria-label": "Brand"
  }, BRANDS.map(b => /*#__PURE__*/React.createElement("button", {
    key: b.slug,
    className: 'wk-switch__btn brand-' + b.slug + (b.slug === brand ? ' is-active' : ''),
    onClick: () => setBrand(b.slug),
    title: 'View as ' + b.name
  }, b.name))));
}
/* SiteSidebar — "Website with Side Menu": a narrow left rail holding the
   lockup, utility actions (search / language / theme), a vertical nav, the
   CTA, and — new — its own footer block anchored to the bottom. The rail
   scrolls internally (own overflow), so the footer sits flush at the bottom
   when content is short and simply scrolls into view when it's tall. */
function SiteSidebar({
  brand,
  setBrand,
  nav,
  legal,
  theme,
  setTheme
}) {
  const [openGroup, setOpenGroup] = React.useState(null);
  const toggle = g => setOpenGroup(openGroup === g ? null : g);
  const chevron = open => /*#__PURE__*/React.createElement("svg", {
    width: "10",
    height: "10",
    viewBox: "0 0 10 10",
    fill: "none",
    style: {
      transform: open ? 'rotate(180deg)' : 'none',
      transition: 'transform var(--dur) var(--ease)'
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M2 4l3 3 3-3",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }));
  const navIcons = [/*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "2",
    width: "5",
    height: "5",
    rx: "1",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "9",
    y: "2",
    width: "5",
    height: "5",
    rx: "1",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "2",
    y: "9",
    width: "5",
    height: "5",
    rx: "1",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("rect", {
    x: "9",
    y: "9",
    width: "5",
    height: "5",
    rx: "1",
    stroke: "currentColor",
    strokeWidth: "1.4"
  })), /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M8 2l6 3.2-6 3.2-6-3.2L8 2Z",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M2 9.2l6 3.2 6-3.2",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  })), /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M2.5 2.8c1.6-.6 3.5-.6 5.5.3 2-.9 3.9-.9 5.5-.3v9.7c-1.6-.6-3.5-.6-5.5.3-2-.9-3.9-.9-5.5-.3V2.8Z",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 3.1v9.7",
    stroke: "currentColor",
    strokeWidth: "1.4"
  })), /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M2.5 14V6.5L8 2l5.5 4.5V14",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 14v-4h4v4",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }))];
  const pastBrandsIcon = /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "8",
    cy: "8",
    r: "6",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 4.5V8l2.5 1.5",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinecap: "round"
  }));
  const socialIcon = /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "4",
    cy: "8",
    r: "1.8",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "3.5",
    r: "1.8",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12.5",
    r: "1.8",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M5.6 7.1l4.8-2.6M5.6 8.9l4.8 2.6",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }));
  const legalIcon = /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M4 2h6l2.5 2.5V14H4V2Z",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M6 8h4M6 10.5h4",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinecap: "round"
  }));
  return /*#__PURE__*/React.createElement("aside", {
    className: "wk-sidebar"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__scroll"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__top"
  }, /*#__PURE__*/React.createElement("a", {
    className: "lockup wk-sidebar__brand",
    href: "#",
    "aria-label": "home"
  }, /*#__PURE__*/React.createElement(Lockup, {
    brand: brand,
    size: 20
  })), /*#__PURE__*/React.createElement("nav", {
    className: "wk-sidebar__nav",
    "aria-label": "Primary"
  }, nav.map((n, i) => /*#__PURE__*/React.createElement("a", {
    key: n,
    className: "wk-sidebar__link plain-label",
    href: "#"
  }, navIcons[i % navIcons.length], n)), /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__link plain-label",
    href: "#"
  }, pastBrandsIcon, "Past brands"), /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__group"
  }, /*#__PURE__*/React.createElement("button", {
    className: "wk-sidebar__link plain-label wk-sidebar__group-toggle",
    "aria-expanded": openGroup === 'social',
    onClick: () => toggle('social')
  }, socialIcon, "Social", chevron(openGroup === 'social')), openGroup === 'social' && /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__submenu"
  }, /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__sublink plain-label",
    href: "#"
  }, "LinkedIn"), /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__sublink plain-label",
    href: "#"
  }, "Instagram"), /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__sublink plain-label",
    href: "#"
  }, "YouTube"))), /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__group"
  }, /*#__PURE__*/React.createElement("button", {
    className: "wk-sidebar__link plain-label wk-sidebar__group-toggle",
    "aria-expanded": openGroup === 'legal',
    onClick: () => toggle('legal')
  }, legalIcon, "Legal", chevron(openGroup === 'legal')), openGroup === 'legal' && /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__submenu"
  }, /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__sublink plain-label",
    href: "#"
  }, "Cookies & local storage"), /*#__PURE__*/React.createElement("a", {
    className: "wk-sidebar__sublink plain-label",
    href: "#"
  }, "Privacy & KVKK notice")))), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    className: "wk-sidebar__cta",
    style: {
      width: 103,
      height: 44
    }
  }, "Contact"), /*#__PURE__*/React.createElement("div", {
    className: "wk-sidebar__utility"
  }, /*#__PURE__*/React.createElement("button", {
    className: "wk-util-pill",
    "aria-label": "Search",
    title: "Search"
  }, /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "7",
    cy: "7",
    r: "5",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M11 11L14.5 14.5",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinecap: "round"
  })), "Search"), /*#__PURE__*/React.createElement("button", {
    className: "wk-util-pill",
    onClick: () => {},
    title: "Change language",
    "aria-label": "Change language"
  }, /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "8",
    cy: "8",
    r: "6.5",
    stroke: "currentColor",
    strokeWidth: "1.4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 1.5c2 2 2 11 0 13M1.5 8h13",
    stroke: "currentColor",
    strokeWidth: "1.4"
  })), "T\xFCrk\xE7e"), /*#__PURE__*/React.createElement("button", {
    className: "wk-util-pill",
    "aria-label": "Toggle theme",
    "aria-pressed": theme === 'dark',
    title: "Toggle theme",
    onClick: () => setTheme(theme === 'dark' ? 'light' : 'dark')
  }, theme === 'dark' ? /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M13.5 9.5A6 6 0 016.5 2.5 6 6 0 1013.5 9.5Z",
    stroke: "currentColor",
    strokeWidth: "1.4",
    strokeLinejoin: "round"
  })) : /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 16 16",
    fill: "none"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "8",
    cy: "8",
    r: "2.6",
    fill: "currentColor"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M8 1.3v1.8M8 12.9v1.8M1.3 8h1.8M12.9 8h1.8M3.4 3.4l1.3 1.3M11.3 11.3l1.3 1.3M12.6 3.4l-1.3 1.3M4.7 11.3l-1.3 1.3",
    stroke: "currentColor",
    strokeWidth: "1.2",
    strokeLinecap: "round"
  })), theme === 'dark' ? 'Dark' : 'Light'))), /*#__PURE__*/React.createElement("a", {
    href: legal.href,
    className: "wk-sidebar__legal"
  }, legal.label)));
}
window.SiteHeader = SiteHeader;
window.SiteSidebar = SiteSidebar;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/header.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/hero.jsx
try { (() => {
/* hero.jsx — editorial homepage hero. Top-aligned opening, full measure.
   No eyebrow above the headline — the headline carries the opening.
   Headline (.type-hero-md / .type-hero) → deck → action links → trust. */
const {
  Link
} = window.AUstosDesignSystem_7fee69;
function SiteHero({
  data,
  scale = 'medium'
}) {
  const headlineClass = scale === 'large' ? 'type-hero' : 'type-hero-md';
  return /*#__PURE__*/React.createElement("header", {
    className: "wk-hero"
  }, /*#__PURE__*/React.createElement("p", {
    className: "wk-hero__crumb"
  }, "Home"), /*#__PURE__*/React.createElement("h1", {
    className: headlineClass + ' wk-hero__headline'
  }, data.headline), /*#__PURE__*/React.createElement("p", {
    className: "type-hero-deck"
  }, data.deck), /*#__PURE__*/React.createElement("div", {
    className: "hero-links"
  }, data.primary.map(p => /*#__PURE__*/React.createElement(Link, {
    key: p,
    href: "#",
    arrow: true
  }, p)), /*#__PURE__*/React.createElement(Link, {
    href: "#",
    variant: "secondary",
    arrow: true
  }, data.secondary)), /*#__PURE__*/React.createElement("p", {
    className: "hero-trust"
  }, data.trust));
}
window.SiteHero = SiteHero;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/hero.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/sections.jsx
try { (() => {
/* sections.jsx — work/catalogue grid, a full-bleed cream editorial band,
   and the permanently-black footer with its single "Contact" CTA. */
const {
  Card,
  Badge,
  Lockup,
  Link,
  Button
} = window.AUstosDesignSystem_7fee69;
function SiteWork({
  data
}) {
  return /*#__PURE__*/React.createElement("section", {
    className: "wk-section"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-section__head"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "type-h2",
    style: {
      margin: 0
    }
  }, data.sectionTitle), /*#__PURE__*/React.createElement(Link, {
    href: "#",
    variant: "secondary",
    arrow: true
  }, data.sectionLink)), /*#__PURE__*/React.createElement("div", {
    className: "wk-grid"
  }, data.items.map((it, i) => /*#__PURE__*/React.createElement(Card, {
    key: i,
    eyebrow: it.kind,
    title: it.title,
    marked: i === 0
  }, it.body))));
}

/* Full-bleed cream band — the one place cream appears, with hairline rules
   top and bottom, never an inset card. */
function SiteBand({
  data
}) {
  return /*#__PURE__*/React.createElement("section", {
    className: "wk-band-outer band-cream"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-band"
  }, /*#__PURE__*/React.createElement("blockquote", {
    className: "type-pullquote",
    style: {
      border: 0,
      padding: 0,
      margin: 0,
      maxWidth: '20ch'
    }
  }, data.bandQuote), /*#__PURE__*/React.createElement("div", {
    className: "wk-band__aside"
  }, /*#__PURE__*/React.createElement("p", {
    className: "type-body",
    style: {
      margin: 0
    }
  }, data.bandBody), /*#__PURE__*/React.createElement("div", {
    className: "wk-band__actions"
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "primary"
  }, data.bandCta), /*#__PURE__*/React.createElement(Link, {
    href: "#",
    variant: "secondary"
  }, data.bandLink)))));
}

/* Footer — permanently off-black. Plain white link labels, no red rule.
   The one "Contact" CTA reads the same word everywhere. */
function SiteFooter({
  brand,
  data
}) {
  return /*#__PURE__*/React.createElement("footer", {
    className: "wk-footer"
  }, /*#__PURE__*/React.createElement("div", {
    className: "wk-footer__brand"
  }, /*#__PURE__*/React.createElement(Lockup, {
    brand: brand,
    size: 20,
    mono: true,
    style: {
      color: 'var(--white)'
    }
  }), /*#__PURE__*/React.createElement("p", {
    className: "type-footnote wk-footer__note"
  }, data.footerNote), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    className: "wk-footer-cta",
    style: {
      background: 'var(--white)',
      color: 'var(--off-black)',
      borderColor: 'var(--white)',
      marginTop: 'var(--space-5)'
    }
  }, "Contact")), /*#__PURE__*/React.createElement("div", {
    className: "wk-footer__cols"
  }, data.footerCols.map((col, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "wk-footer__col"
  }, /*#__PURE__*/React.createElement("p", {
    className: "type-h4 wk-footer__colhead"
  }, col.title), /*#__PURE__*/React.createElement("ul", {
    className: "wk-footer__list"
  }, col.links.map(l => /*#__PURE__*/React.createElement("li", {
    key: l
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    className: "wk-footer__link reset-link"
  }, l))))))));
}
window.SiteWork = SiteWork;
window.SiteBand = SiteBand;
window.SiteFooter = SiteFooter;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/sections.jsx", error: String((e && e.message) || e) }); }

// ui_kits/website/tweaks-panel.jsx
try { (() => {
// @ds-adherence-ignore -- omelette starter scaffold (raw elements/hex/px by design)

/* BEGIN USAGE */
// tweaks-panel.jsx
// Reusable Tweaks shell + form-control helpers.
// Exports (to window): useTweaks, TweaksPanel, TweakSection, TweakRow, TweakSlider,
//   TweakToggle, TweakRadio, TweakSelect, TweakText, TweakNumber, TweakColor, TweakButton.
//
// Owns the host protocol (listens for __activate_edit_mode / __deactivate_edit_mode,
// posts __edit_mode_available / __edit_mode_set_keys / __edit_mode_dismissed) so
// individual prototypes don't re-roll it. Ships a consistent set of controls so you
// don't hand-draw <input type="range">, segmented radios, steppers, etc.
//
// Usage (in an HTML file that loads React + Babel):
//
//   const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
//     "primaryColor": "#D97757",
//     "palette": ["#D97757", "#29261b", "#f6f4ef"],
//     "fontSize": 16,
//     "density": "regular",
//     "dark": false
//   }/*EDITMODE-END*/;
//
//   function App() {
//     const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
//     return (
//       <div style={{ fontSize: t.fontSize, color: t.primaryColor }}>
//         Hello
//         <TweaksPanel>
//           <TweakSection label="Typography" />
//           <TweakSlider label="Font size" value={t.fontSize} min={10} max={32} unit="px"
//                        onChange={(v) => setTweak('fontSize', v)} />
//           <TweakRadio  label="Density" value={t.density}
//                        options={['compact', 'regular', 'comfy']}
//                        onChange={(v) => setTweak('density', v)} />
//           <TweakSection label="Theme" />
//           <TweakColor  label="Primary" value={t.primaryColor}
//                        options={['#D97757', '#2A6FDB', '#1F8A5B', '#7A5AE0']}
//                        onChange={(v) => setTweak('primaryColor', v)} />
//           <TweakColor  label="Palette" value={t.palette}
//                        options={[['#D97757', '#29261b', '#f6f4ef'],
//                                  ['#475569', '#0f172a', '#f1f5f9']]}
//                        onChange={(v) => setTweak('palette', v)} />
//           <TweakToggle label="Dark mode" value={t.dark}
//                        onChange={(v) => setTweak('dark', v)} />
//         </TweaksPanel>
//       </div>
//     );
//   }
//
// TweakRadio is the segmented control for 2–3 short options (auto-falls-back to
// TweakSelect past ~16/~10 chars per label); reach for TweakSelect directly when
// options are many or long. For color tweaks always curate 3-4 options rather than
// a free picker; an option can also be a whole 2–5 color palette (the stored value
// is the array). The Tweak* controls are a floor, not a ceiling — build custom
// controls inside the panel if a tweak calls for UI they don't cover.
/* END USAGE */
// ─────────────────────────────────────────────────────────────────────────────

const __TWEAKS_STYLE = `
  .twk-panel{position:fixed;right:16px;bottom:16px;z-index:2147483646;width:280px;
    max-height:calc(100vh - 32px);display:flex;flex-direction:column;
    transform:scale(var(--dc-inv-zoom,1));transform-origin:bottom right;
    background:rgba(250,249,247,.78);color:#29261b;
    -webkit-backdrop-filter:blur(24px) saturate(160%);backdrop-filter:blur(24px) saturate(160%);
    border:.5px solid rgba(255,255,255,.6);border-radius:14px;
    box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 12px 40px rgba(0,0,0,.18);
    font:11.5px/1.4 ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}
  .twk-hd{display:flex;align-items:center;justify-content:space-between;
    padding:10px 8px 10px 14px;cursor:move;user-select:none}
  .twk-hd b{font-size:12px;font-weight:600;letter-spacing:.01em}
  .twk-x{appearance:none;border:0;background:transparent;color:rgba(41,38,27,.55);
    width:22px;height:22px;border-radius:6px;cursor:default;font-size:13px;line-height:1}
  .twk-x:hover{background:rgba(0,0,0,.06);color:#29261b}
  .twk-body{padding:2px 14px 14px;display:flex;flex-direction:column;gap:10px;
    overflow-y:auto;overflow-x:hidden;min-height:0;
    scrollbar-width:thin;scrollbar-color:rgba(0,0,0,.15) transparent}
  .twk-body::-webkit-scrollbar{width:8px}
  .twk-body::-webkit-scrollbar-track{background:transparent;margin:2px}
  .twk-body::-webkit-scrollbar-thumb{background:rgba(0,0,0,.15);border-radius:4px;
    border:2px solid transparent;background-clip:content-box}
  .twk-body::-webkit-scrollbar-thumb:hover{background:rgba(0,0,0,.25);
    border:2px solid transparent;background-clip:content-box}
  .twk-row{display:flex;flex-direction:column;gap:5px}
  .twk-row-h{flex-direction:row;align-items:center;justify-content:space-between;gap:10px}
  .twk-lbl{display:flex;justify-content:space-between;align-items:baseline;
    color:rgba(41,38,27,.72)}
  .twk-lbl>span:first-child{font-weight:500}
  .twk-val{color:rgba(41,38,27,.5);font-variant-numeric:tabular-nums}

  .twk-sect{font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;
    color:rgba(41,38,27,.45);padding:10px 0 0}
  .twk-sect:first-child{padding-top:0}

  .twk-field{appearance:none;box-sizing:border-box;width:100%;min-width:0;height:26px;padding:0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;
    background:rgba(255,255,255,.6);color:inherit;font:inherit;outline:none}
  .twk-field:focus{border-color:rgba(0,0,0,.25);background:rgba(255,255,255,.85)}
  select.twk-field{padding-right:22px;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path fill='rgba(0,0,0,.5)' d='M0 0h10L5 6z'/></svg>");
    background-repeat:no-repeat;background-position:right 8px center}

  .twk-slider{appearance:none;-webkit-appearance:none;width:100%;height:4px;margin:6px 0;
    border-radius:999px;background:rgba(0,0,0,.12);outline:none}
  .twk-slider::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;
    width:14px;height:14px;border-radius:50%;background:#fff;
    border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}
  .twk-slider::-moz-range-thumb{width:14px;height:14px;border-radius:50%;
    background:#fff;border:.5px solid rgba(0,0,0,.12);box-shadow:0 1px 3px rgba(0,0,0,.2);cursor:default}

  .twk-seg{position:relative;display:flex;padding:2px;border-radius:8px;
    background:rgba(0,0,0,.06);user-select:none}
  .twk-seg-thumb{position:absolute;top:2px;bottom:2px;border-radius:6px;
    background:rgba(255,255,255,.9);box-shadow:0 1px 2px rgba(0,0,0,.12);
    transition:left .15s cubic-bezier(.3,.7,.4,1),width .15s}
  .twk-seg.dragging .twk-seg-thumb{transition:none}
  .twk-seg button{appearance:none;position:relative;z-index:1;flex:1;border:0;
    background:transparent;color:inherit;font:inherit;font-weight:500;min-height:22px;
    border-radius:6px;cursor:default;padding:4px 6px;line-height:1.2;
    overflow-wrap:anywhere}

  .twk-toggle{position:relative;width:32px;height:18px;border:0;border-radius:999px;
    background:rgba(0,0,0,.15);transition:background .15s;cursor:default;padding:0}
  .twk-toggle[data-on="1"]{background:#34c759}
  .twk-toggle i{position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;
    background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.25);transition:transform .15s}
  .twk-toggle[data-on="1"] i{transform:translateX(14px)}

  .twk-num{display:flex;align-items:center;box-sizing:border-box;min-width:0;height:26px;padding:0 0 0 8px;
    border:.5px solid rgba(0,0,0,.1);border-radius:7px;background:rgba(255,255,255,.6)}
  .twk-num-lbl{font-weight:500;color:rgba(41,38,27,.6);cursor:ew-resize;
    user-select:none;padding-right:8px}
  .twk-num input{flex:1;min-width:0;height:100%;border:0;background:transparent;
    font:inherit;font-variant-numeric:tabular-nums;text-align:right;padding:0 8px 0 0;
    outline:none;color:inherit;-moz-appearance:textfield}
  .twk-num input::-webkit-inner-spin-button,.twk-num input::-webkit-outer-spin-button{
    -webkit-appearance:none;margin:0}
  .twk-num-unit{padding-right:8px;color:rgba(41,38,27,.45)}

  .twk-btn{appearance:none;height:26px;padding:0 12px;border:0;border-radius:7px;
    background:rgba(0,0,0,.78);color:#fff;font:inherit;font-weight:500;cursor:default}
  .twk-btn:hover{background:rgba(0,0,0,.88)}
  .twk-btn.secondary{background:rgba(0,0,0,.06);color:inherit}
  .twk-btn.secondary:hover{background:rgba(0,0,0,.1)}

  .twk-swatch{appearance:none;-webkit-appearance:none;width:56px;height:22px;
    border:.5px solid rgba(0,0,0,.1);border-radius:6px;padding:0;cursor:default;
    background:transparent;flex-shrink:0}
  .twk-swatch::-webkit-color-swatch-wrapper{padding:0}
  .twk-swatch::-webkit-color-swatch{border:0;border-radius:5.5px}
  .twk-swatch::-moz-color-swatch{border:0;border-radius:5.5px}

  .twk-chips{display:flex;gap:6px}
  .twk-chip{position:relative;appearance:none;flex:1;min-width:0;height:46px;
    padding:0;border:0;border-radius:6px;overflow:hidden;cursor:default;
    box-shadow:0 0 0 .5px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.06);
    transition:transform .12s cubic-bezier(.3,.7,.4,1),box-shadow .12s}
  .twk-chip:hover{transform:translateY(-1px);
    box-shadow:0 0 0 .5px rgba(0,0,0,.18),0 4px 10px rgba(0,0,0,.12)}
  .twk-chip[data-on="1"]{box-shadow:0 0 0 1.5px rgba(0,0,0,.85),
    0 2px 6px rgba(0,0,0,.15)}
  .twk-chip>span{position:absolute;top:0;bottom:0;right:0;width:34%;
    display:flex;flex-direction:column;box-shadow:-1px 0 0 rgba(0,0,0,.1)}
  .twk-chip>span>i{flex:1;box-shadow:0 -1px 0 rgba(0,0,0,.1)}
  .twk-chip>span>i:first-child{box-shadow:none}
  .twk-chip svg{position:absolute;top:6px;left:6px;width:13px;height:13px;
    filter:drop-shadow(0 1px 1px rgba(0,0,0,.3))}
`;

// ── useTweaks ───────────────────────────────────────────────────────────────
// Single source of truth for tweak values. setTweak persists via the host
// (__edit_mode_set_keys → host rewrites the EDITMODE block on disk).
function useTweaks(defaults) {
  const [values, setValues] = React.useState(defaults);
  // Accepts either setTweak('key', value) or setTweak({ key: value, ... }) so a
  // useState-style call doesn't write a "[object Object]" key into the persisted
  // JSON block.
  const setTweak = React.useCallback((keyOrEdits, val) => {
    const edits = typeof keyOrEdits === 'object' && keyOrEdits !== null ? keyOrEdits : {
      [keyOrEdits]: val
    };
    setValues(prev => ({
      ...prev,
      ...edits
    }));
    window.parent.postMessage({
      type: '__edit_mode_set_keys',
      edits
    }, '*');
    // Same-window signal so in-page listeners (deck-stage rail thumbnails)
    // can react — the parent message only reaches the host, not peers.
    window.dispatchEvent(new CustomEvent('tweakchange', {
      detail: edits
    }));
  }, []);
  return [values, setTweak];
}

// ── TweaksPanel ─────────────────────────────────────────────────────────────
// Floating shell. Registers the protocol listener BEFORE announcing
// availability — if the announce ran first, the host's activate could land
// before our handler exists and the toolbar toggle would silently no-op.
// The close button posts __edit_mode_dismissed so the host's toolbar toggle
// flips off in lockstep; the host echoes __deactivate_edit_mode back which
// is what actually hides the panel.
function TweaksPanel({
  title = 'Tweaks',
  children
}) {
  const [open, setOpen] = React.useState(false);
  const dragRef = React.useRef(null);
  const offsetRef = React.useRef({
    x: 16,
    y: 16
  });
  const PAD = 16;
  const clampToViewport = React.useCallback(() => {
    const panel = dragRef.current;
    if (!panel) return;
    const w = panel.offsetWidth,
      h = panel.offsetHeight;
    const maxRight = Math.max(PAD, window.innerWidth - w - PAD);
    const maxBottom = Math.max(PAD, window.innerHeight - h - PAD);
    offsetRef.current = {
      x: Math.min(maxRight, Math.max(PAD, offsetRef.current.x)),
      y: Math.min(maxBottom, Math.max(PAD, offsetRef.current.y))
    };
    panel.style.right = offsetRef.current.x + 'px';
    panel.style.bottom = offsetRef.current.y + 'px';
  }, []);
  React.useEffect(() => {
    if (!open) return;
    clampToViewport();
    if (typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', clampToViewport);
      return () => window.removeEventListener('resize', clampToViewport);
    }
    const ro = new ResizeObserver(clampToViewport);
    ro.observe(document.documentElement);
    return () => ro.disconnect();
  }, [open, clampToViewport]);
  React.useEffect(() => {
    const onMsg = e => {
      const t = e?.data?.type;
      if (t === '__activate_edit_mode') setOpen(true);else if (t === '__deactivate_edit_mode') setOpen(false);
    };
    window.addEventListener('message', onMsg);
    window.parent.postMessage({
      type: '__edit_mode_available'
    }, '*');
    return () => window.removeEventListener('message', onMsg);
  }, []);
  const dismiss = () => {
    setOpen(false);
    window.parent.postMessage({
      type: '__edit_mode_dismissed'
    }, '*');
  };
  const onDragStart = e => {
    const panel = dragRef.current;
    if (!panel) return;
    const r = panel.getBoundingClientRect();
    const sx = e.clientX,
      sy = e.clientY;
    const startRight = window.innerWidth - r.right;
    const startBottom = window.innerHeight - r.bottom;
    const move = ev => {
      offsetRef.current = {
        x: startRight - (ev.clientX - sx),
        y: startBottom - (ev.clientY - sy)
      };
      clampToViewport();
    };
    const up = () => {
      window.removeEventListener('mousemove', move);
      window.removeEventListener('mouseup', up);
    };
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
  };
  if (!open) return null;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("style", null, __TWEAKS_STYLE), /*#__PURE__*/React.createElement("div", {
    ref: dragRef,
    className: "twk-panel",
    "data-omelette-chrome": "",
    style: {
      right: offsetRef.current.x,
      bottom: offsetRef.current.y
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-hd",
    onMouseDown: onDragStart
  }, /*#__PURE__*/React.createElement("b", null, title), /*#__PURE__*/React.createElement("button", {
    className: "twk-x",
    "aria-label": "Close tweaks",
    onMouseDown: e => e.stopPropagation(),
    onClick: dismiss
  }, "\u2715")), /*#__PURE__*/React.createElement("div", {
    className: "twk-body"
  }, children)));
}

// ── Layout helpers ──────────────────────────────────────────────────────────

function TweakSection({
  label,
  children
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "twk-sect"
  }, label), children);
}
function TweakRow({
  label,
  value,
  children,
  inline = false
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: inline ? 'twk-row twk-row-h' : 'twk-row'
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-lbl"
  }, /*#__PURE__*/React.createElement("span", null, label), value != null && /*#__PURE__*/React.createElement("span", {
    className: "twk-val"
  }, value)), children);
}

// ── Controls ────────────────────────────────────────────────────────────────

function TweakSlider({
  label,
  value,
  min = 0,
  max = 100,
  step = 1,
  unit = '',
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label,
    value: `${value}${unit}`
  }, /*#__PURE__*/React.createElement("input", {
    type: "range",
    className: "twk-slider",
    min: min,
    max: max,
    step: step,
    value: value,
    onChange: e => onChange(Number(e.target.value))
  }));
}
function TweakToggle({
  label,
  value,
  onChange
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "twk-row twk-row-h"
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-lbl"
  }, /*#__PURE__*/React.createElement("span", null, label)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "twk-toggle",
    "data-on": value ? '1' : '0',
    role: "switch",
    "aria-checked": !!value,
    onClick: () => onChange(!value)
  }, /*#__PURE__*/React.createElement("i", null)));
}
function TweakRadio({
  label,
  value,
  options,
  onChange
}) {
  const trackRef = React.useRef(null);
  const [dragging, setDragging] = React.useState(false);
  // The active value is read by pointer-move handlers attached for the lifetime
  // of a drag — ref it so a stale closure doesn't fire onChange for every move.
  const valueRef = React.useRef(value);
  valueRef.current = value;

  // Segments wrap mid-word once per-segment width runs out. The track is
  // ~248px (280 panel − 28 body pad − 4 seg pad), each button loses 12px
  // to its own padding, and 11.5px system-ui averages ~6.3px/char — so 2
  // options fit ~16 chars each, 3 fit ~10. Past that (or >3 options), fall
  // back to a dropdown rather than wrap.
  const labelLen = o => String(typeof o === 'object' ? o.label : o).length;
  const maxLen = options.reduce((m, o) => Math.max(m, labelLen(o)), 0);
  const fitsAsSegments = maxLen <= ({
    2: 16,
    3: 10
  }[options.length] ?? 0);
  if (!fitsAsSegments) {
    // <select> emits strings — map back to the original option value so the
    // fallback stays type-preserving (numbers, booleans) like the segment path.
    const resolve = s => {
      const m = options.find(o => String(typeof o === 'object' ? o.value : o) === s);
      return m === undefined ? s : typeof m === 'object' ? m.value : m;
    };
    return /*#__PURE__*/React.createElement(TweakSelect, {
      label: label,
      value: value,
      options: options,
      onChange: s => onChange(resolve(s))
    });
  }
  const opts = options.map(o => typeof o === 'object' ? o : {
    value: o,
    label: o
  });
  const idx = Math.max(0, opts.findIndex(o => o.value === value));
  const n = opts.length;
  const segAt = clientX => {
    const r = trackRef.current.getBoundingClientRect();
    const inner = r.width - 4;
    const i = Math.floor((clientX - r.left - 2) / inner * n);
    return opts[Math.max(0, Math.min(n - 1, i))].value;
  };
  const onPointerDown = e => {
    setDragging(true);
    const v0 = segAt(e.clientX);
    if (v0 !== valueRef.current) onChange(v0);
    const move = ev => {
      if (!trackRef.current) return;
      const v = segAt(ev.clientX);
      if (v !== valueRef.current) onChange(v);
    };
    const up = () => {
      setDragging(false);
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("div", {
    ref: trackRef,
    role: "radiogroup",
    onPointerDown: onPointerDown,
    className: dragging ? 'twk-seg dragging' : 'twk-seg'
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-seg-thumb",
    style: {
      left: `calc(2px + ${idx} * (100% - 4px) / ${n})`,
      width: `calc((100% - 4px) / ${n})`
    }
  }), opts.map(o => /*#__PURE__*/React.createElement("button", {
    key: o.value,
    type: "button",
    role: "radio",
    "aria-checked": o.value === value
  }, o.label))));
}
function TweakSelect({
  label,
  value,
  options,
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("select", {
    className: "twk-field",
    value: value,
    onChange: e => onChange(e.target.value)
  }, options.map(o => {
    const v = typeof o === 'object' ? o.value : o;
    const l = typeof o === 'object' ? o.label : o;
    return /*#__PURE__*/React.createElement("option", {
      key: v,
      value: v
    }, l);
  })));
}
function TweakText({
  label,
  value,
  placeholder,
  onChange
}) {
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("input", {
    className: "twk-field",
    type: "text",
    value: value,
    placeholder: placeholder,
    onChange: e => onChange(e.target.value)
  }));
}
function TweakNumber({
  label,
  value,
  min,
  max,
  step = 1,
  unit = '',
  onChange
}) {
  const clamp = n => {
    if (min != null && n < min) return min;
    if (max != null && n > max) return max;
    return n;
  };
  const startRef = React.useRef({
    x: 0,
    val: 0
  });
  const onScrubStart = e => {
    e.preventDefault();
    startRef.current = {
      x: e.clientX,
      val: value
    };
    const decimals = (String(step).split('.')[1] || '').length;
    const move = ev => {
      const dx = ev.clientX - startRef.current.x;
      const raw = startRef.current.val + dx * step;
      const snapped = Math.round(raw / step) * step;
      onChange(clamp(Number(snapped.toFixed(decimals))));
    };
    const up = () => {
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerup', up);
    };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', up);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "twk-num"
  }, /*#__PURE__*/React.createElement("span", {
    className: "twk-num-lbl",
    onPointerDown: onScrubStart
  }, label), /*#__PURE__*/React.createElement("input", {
    type: "number",
    value: value,
    min: min,
    max: max,
    step: step,
    onChange: e => onChange(clamp(Number(e.target.value)))
  }), unit && /*#__PURE__*/React.createElement("span", {
    className: "twk-num-unit"
  }, unit));
}

// Relative-luminance contrast pick — checkmarks drawn over a swatch need to
// read on both #111 and #fafafa without per-option configuration. Hex input
// only (#rgb / #rrggbb); named or rgb()/hsl() colors fall through to "light".
function __twkIsLight(hex) {
  const h = String(hex).replace('#', '');
  const x = h.length === 3 ? h.replace(/./g, c => c + c) : h.padEnd(6, '0');
  const n = parseInt(x.slice(0, 6), 16);
  if (Number.isNaN(n)) return true;
  const r = n >> 16 & 255,
    g = n >> 8 & 255,
    b = n & 255;
  return r * 299 + g * 587 + b * 114 > 148000;
}
const __TwkCheck = ({
  light
}) => /*#__PURE__*/React.createElement("svg", {
  viewBox: "0 0 14 14",
  "aria-hidden": "true"
}, /*#__PURE__*/React.createElement("path", {
  d: "M3 7.2 5.8 10 11 4.2",
  fill: "none",
  strokeWidth: "2.2",
  strokeLinecap: "round",
  strokeLinejoin: "round",
  stroke: light ? 'rgba(0,0,0,.78)' : '#fff'
}));

// TweakColor — curated color/palette picker. Each option is either a single
// hex string or an array of 1-5 hex strings; the card adapts — a lone color
// renders solid, a palette renders colors[0] as the hero (left ~2/3) with the
// rest stacked in a sharp column on the right. onChange emits the
// option in the shape it was passed (string stays string, array stays array).
// Without options it falls back to the native color input for back-compat.
function TweakColor({
  label,
  value,
  options,
  onChange
}) {
  if (!options || !options.length) {
    return /*#__PURE__*/React.createElement("div", {
      className: "twk-row twk-row-h"
    }, /*#__PURE__*/React.createElement("div", {
      className: "twk-lbl"
    }, /*#__PURE__*/React.createElement("span", null, label)), /*#__PURE__*/React.createElement("input", {
      type: "color",
      className: "twk-swatch",
      value: value,
      onChange: e => onChange(e.target.value)
    }));
  }
  // Native <input type=color> emits lowercase hex per the HTML spec, so
  // compare case-insensitively. String() guards JSON.stringify(undefined),
  // which returns the primitive undefined (no .toLowerCase).
  const key = o => String(JSON.stringify(o)).toLowerCase();
  const cur = key(value);
  return /*#__PURE__*/React.createElement(TweakRow, {
    label: label
  }, /*#__PURE__*/React.createElement("div", {
    className: "twk-chips",
    role: "radiogroup"
  }, options.map((o, i) => {
    const colors = Array.isArray(o) ? o : [o];
    const [hero, ...rest] = colors;
    const sup = rest.slice(0, 4);
    const on = key(o) === cur;
    return /*#__PURE__*/React.createElement("button", {
      key: i,
      type: "button",
      className: "twk-chip",
      role: "radio",
      "aria-checked": on,
      "data-on": on ? '1' : '0',
      "aria-label": colors.join(', '),
      title: colors.join(' · '),
      style: {
        background: hero
      },
      onClick: () => onChange(o)
    }, sup.length > 0 && /*#__PURE__*/React.createElement("span", null, sup.map((c, j) => /*#__PURE__*/React.createElement("i", {
      key: j,
      style: {
        background: c
      }
    }))), on && /*#__PURE__*/React.createElement(__TwkCheck, {
      light: __twkIsLight(hero)
    }));
  })));
}
function TweakButton({
  label,
  onClick,
  secondary = false
}) {
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: secondary ? 'twk-btn secondary' : 'twk-btn',
    onClick: onClick
  }, label);
}
Object.assign(window, {
  useTweaks,
  TweaksPanel,
  TweakSection,
  TweakRow,
  TweakSlider,
  TweakToggle,
  TweakRadio,
  TweakSelect,
  TweakText,
  TweakNumber,
  TweakColor,
  TweakButton
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/website/tweaks-panel.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Link = __ds_scope.Link;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.LazGunesi = __ds_scope.LazGunesi;

__ds_ns.Lockup = __ds_scope.Lockup;

})();
