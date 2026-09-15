/* sections.jsx — work/catalogue grid, a full-bleed cream editorial band,
   and the permanently-black footer with its single "Contact" CTA. */
const { Card, Badge, Lockup, Link, Button } = window.AUstosDesignSystem_7fee69;

function SiteWork({ data }) {
  return (
    <section className="wk-section">
      <div className="wk-section__head">
        <h2 className="type-h2" style={{ margin: 0 }}>{data.sectionTitle}</h2>
        <Link href="#" variant="secondary" arrow>{data.sectionLink}</Link>
      </div>
      <div className="wk-grid">
        {data.items.map((it, i) => (
          <Card key={i} eyebrow={it.kind} title={it.title} marked={i === 0}>
            {it.body}
          </Card>
        ))}
      </div>
    </section>
  );
}

/* Full-bleed cream band — the one place cream appears, with hairline rules
   top and bottom, never an inset card. */
function SiteBand({ data }) {
  return (
    <section className="wk-band-outer band-cream">
      <div className="wk-band">
        <blockquote className="type-pullquote" style={{ border: 0, padding: 0, margin: 0, maxWidth: '20ch' }}>
          {data.bandQuote}
        </blockquote>
        <div className="wk-band__aside">
          <p className="type-body" style={{ margin: 0 }}>{data.bandBody}</p>
          <div className="wk-band__actions">
            <Button variant="primary">{data.bandCta}</Button>
            <Link href="#" variant="secondary">{data.bandLink}</Link>
          </div>
        </div>
      </div>
    </section>
  );
}

/* Footer — permanently off-black. Plain white link labels, no red rule.
   The one "Contact" CTA reads the same word everywhere. */
function SiteFooter({ brand, data }) {
  return (
    <footer className="wk-footer">
      <div className="wk-footer__brand">
        <Lockup brand={brand} size={20} mono style={{ color: 'var(--white)' }} />
        <p className="type-footnote wk-footer__note">{data.footerNote}</p>
        <Button variant="primary" className="wk-footer-cta" style={{ background: 'var(--white)', color: 'var(--off-black)', borderColor: 'var(--white)', marginTop: 'var(--space-5)' }}>Contact</Button>
      </div>
      <div className="wk-footer__cols">
        {data.footerCols.map((col, i) => (
          <div key={i} className="wk-footer__col">
            <p className="type-h4 wk-footer__colhead">{col.title}</p>
            <ul className="wk-footer__list">
              {col.links.map((l) => <li key={l}><a href="#" className="wk-footer__link reset-link">{l}</a></li>)}
            </ul>
          </div>
        ))}
      </div>
    </footer>
  );
}
window.SiteWork = SiteWork;
window.SiteBand = SiteBand;
window.SiteFooter = SiteFooter;
