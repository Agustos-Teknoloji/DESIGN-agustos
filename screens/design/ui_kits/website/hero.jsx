/* hero.jsx — editorial homepage hero. Top-aligned opening, full measure.
   No eyebrow above the headline — the headline carries the opening.
   Headline (.type-hero-md / .type-hero) → deck → action links → trust. */
const { Link } = window.AUstosDesignSystem_7fee69;

function SiteHero({ data, scale = 'medium' }) {
  const headlineClass = scale === 'large' ? 'type-hero' : 'type-hero-md';
  return (
    <header className="wk-hero">
      <p className="wk-hero__crumb">Home</p>
      <h1 className={headlineClass + ' wk-hero__headline'}>{data.headline}</h1>
      <p className="type-hero-deck">{data.deck}</p>
      <div className="hero-links">
        {data.primary.map((p) => (
          <Link key={p} href="#" arrow>{p}</Link>
        ))}
        <Link href="#" variant="secondary" arrow>{data.secondary}</Link>
      </div>
      <p className="hero-trust">{data.trust}</p>
    </header>
  );
}
window.SiteHero = SiteHero;
