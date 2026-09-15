/* header.jsx — site header: lockup + editorial nav + brand switcher.
   The switcher demonstrates the multi-brand axis (name only — colour is
   fixed to the publisher). Nav items are plain labels: the red rule reveals
   only on hover / the current item (see .plain-label in base.css). */
const { Lockup, Button } = window.AUstosDesignSystem_7fee69;

const BRANDS = [
  { slug: 'agustos', name: 'ağustos' },
  { slug: 'pataraz', name: 'pataraz' },
  { slug: 'pld', name: 'pld türkiye' },
  { slug: 'iesdesk', name: 'iesdesk' },
  { slug: 'specquick', name: 'specquick' },
];

function SiteHeader({ brand, setBrand, nav }) {
  return (
    <div className="wk-header">
      <a className="lockup" href="#" aria-label="home">
        <Lockup brand={brand} size={22} />
      </a>
      <nav className="wk-nav wk-nav--center" aria-label="Primary">
        {nav.map((n) => (
          <a key={n} className="wk-nav__link plain-label" href="#">{n}</a>
        ))}
      </nav>
      <div className="wk-switch" role="group" aria-label="Brand">
        {BRANDS.map((b) => (
          <button
            key={b.slug}
            className={'wk-switch__btn brand-' + b.slug + (b.slug === brand ? ' is-active' : '')}
            onClick={() => setBrand(b.slug)}
            title={'View as ' + b.name}
          >
            {b.name}
          </button>
        ))}
      </div>
    </div>
  );
}
/* SiteSidebar — "Website with Side Menu": a narrow left rail holding the
   lockup, utility actions (search / language / theme), a vertical nav, the
   CTA, and — new — its own footer block anchored to the bottom. The rail
   scrolls internally (own overflow), so the footer sits flush at the bottom
   when content is short and simply scrolls into view when it's tall. */
function SiteSidebar({ brand, setBrand, nav, legal, theme, setTheme }) {
  const [openGroup, setOpenGroup] = React.useState(null);
  const toggle = (g) => setOpenGroup(openGroup === g ? null : g);
  const chevron = (open) => (
    <svg width="10" height="10" viewBox="0 0 10 10" fill="none" style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform var(--dur) var(--ease)' }}>
      <path d="M2 4l3 3 3-3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
  const navIcons = [
    <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><rect x="2" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4"/><rect x="9" y="2" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4"/><rect x="2" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4"/><rect x="9" y="9" width="5" height="5" rx="1" stroke="currentColor" strokeWidth="1.4"/></svg>,
    <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M8 2l6 3.2-6 3.2-6-3.2L8 2Z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/><path d="M2 9.2l6 3.2 6-3.2" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/></svg>,
    <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M2.5 2.8c1.6-.6 3.5-.6 5.5.3 2-.9 3.9-.9 5.5-.3v9.7c-1.6-.6-3.5-.6-5.5.3-2-.9-3.9-.9-5.5-.3V2.8Z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/><path d="M8 3.1v9.7" stroke="currentColor" strokeWidth="1.4"/></svg>,
    <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M2.5 14V6.5L8 2l5.5 4.5V14" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/><path d="M6 14v-4h4v4" stroke="currentColor" strokeWidth="1.4"/></svg>,
  ];
  const pastBrandsIcon = <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.4"/><path d="M8 4.5V8l2.5 1.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>;
  const socialIcon = <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="4" cy="8" r="1.8" stroke="currentColor" strokeWidth="1.4"/><circle cx="12" cy="3.5" r="1.8" stroke="currentColor" strokeWidth="1.4"/><circle cx="12" cy="12.5" r="1.8" stroke="currentColor" strokeWidth="1.4"/><path d="M5.6 7.1l4.8-2.6M5.6 8.9l4.8 2.6" stroke="currentColor" strokeWidth="1.4"/></svg>;
  const legalIcon = <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M4 2h6l2.5 2.5V14H4V2Z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/><path d="M6 8h4M6 10.5h4" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>;
  return (
    <aside className="wk-sidebar">
      <div className="wk-sidebar__scroll">
        <div className="wk-sidebar__top">
          <a className="lockup wk-sidebar__brand" href="#" aria-label="home">
            <Lockup brand={brand} size={20} />
          </a>
          <nav className="wk-sidebar__nav" aria-label="Primary">
            {nav.map((n, i) => (
              <a key={n} className="wk-sidebar__link plain-label" href="#">{navIcons[i % navIcons.length]}{n}</a>
            ))}
            <a className="wk-sidebar__link plain-label" href="#">{pastBrandsIcon}Past brands</a>
            <div className="wk-sidebar__group">
              <button className="wk-sidebar__link plain-label wk-sidebar__group-toggle" aria-expanded={openGroup === 'social'} onClick={() => toggle('social')}>
                {socialIcon}Social{chevron(openGroup === 'social')}
              </button>
              {openGroup === 'social' && (
                <div className="wk-sidebar__submenu">
                  <a className="wk-sidebar__sublink plain-label" href="#">LinkedIn</a>
                  <a className="wk-sidebar__sublink plain-label" href="#">Instagram</a>
                  <a className="wk-sidebar__sublink plain-label" href="#">YouTube</a>
                </div>
              )}
            </div>
            <div className="wk-sidebar__group">
              <button className="wk-sidebar__link plain-label wk-sidebar__group-toggle" aria-expanded={openGroup === 'legal'} onClick={() => toggle('legal')}>
                {legalIcon}Legal{chevron(openGroup === 'legal')}
              </button>
              {openGroup === 'legal' && (
                <div className="wk-sidebar__submenu">
                  <a className="wk-sidebar__sublink plain-label" href="#">Cookies & local storage</a>
                  <a className="wk-sidebar__sublink plain-label" href="#">Privacy & KVKK notice</a>
                </div>
              )}
            </div>
          </nav>
          <Button variant="primary" className="wk-sidebar__cta" style={{ width: 103, height: 44 }}>Contact</Button>
          <div className="wk-sidebar__utility">
            <button className="wk-util-pill" aria-label="Search" title="Search">
              <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="7" cy="7" r="5" stroke="currentColor" strokeWidth="1.4"/><path d="M11 11L14.5 14.5" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round"/></svg>
              Search
            </button>
            <button className="wk-util-pill" onClick={() => {}} title="Change language" aria-label="Change language">
              <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6.5" stroke="currentColor" strokeWidth="1.4"/><path d="M8 1.5c2 2 2 11 0 13M1.5 8h13" stroke="currentColor" strokeWidth="1.4"/></svg>
              Türkçe
            </button>
            <button
              className="wk-util-pill"
              aria-label="Toggle theme"
              aria-pressed={theme === 'dark'}
              title="Toggle theme"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><path d="M13.5 9.5A6 6 0 016.5 2.5 6 6 0 1013.5 9.5Z" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round"/></svg>
              ) : (
                <svg width="15" height="15" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="2.6" fill="currentColor"/><path d="M8 1.3v1.8M8 12.9v1.8M1.3 8h1.8M12.9 8h1.8M3.4 3.4l1.3 1.3M11.3 11.3l1.3 1.3M12.6 3.4l-1.3 1.3M4.7 11.3l-1.3 1.3" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/></svg>
              )}
              {theme === 'dark' ? 'Dark' : 'Light'}
            </button>
          </div>
        </div>
        <a href={legal.href} className="wk-sidebar__legal">{legal.label}</a>
      </div>
    </aside>
  );
}

window.SiteHeader = SiteHeader;
window.SiteSidebar = SiteSidebar;
