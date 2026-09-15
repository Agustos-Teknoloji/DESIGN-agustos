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
    items: [
      { kind: 'Cultural', title: 'A museum, relit', body: 'Gallery-grade tunable white and a concealed track system for a restored Ottoman hall.' },
      { kind: 'Retail', title: 'Flagship, Nişantaşı', body: 'Accent and ambient layers tuned to the merchandise, commissioned on site.' },
      { kind: 'Workplace', title: 'HQ, Maslak', body: 'Low-glare UGR<19 office field with daylight-linked dimming throughout.' },
    ],
    bandQuote: 'One symbol, forever.',
    bandBody: 'Every project ships with its photometric study, IES files, and a commissioning report. The work is documented as carefully as it is designed.',
    bandCta: 'Request pricing',
    bandLink: 'Download a sample dossier',
    footerNote: 'Ağustos Teknoloji · architectural lighting, agency & distribution · İstanbul, Türkiye.',
    legal: { label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(), href: 'https://agustos.com' },
    copyright: { label: '© Ağustos Teknoloji', href: 'https://agustos.com' },
    footerCols: [
      { title: 'Work', links: ['Projects', 'Sectors', 'Process'] },
      { title: 'Trade', links: ['Catalogue', 'IES files', 'Become a partner'] },
      { title: 'Studio', links: ['About', 'Contact', 'Careers'] },
    ],
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
    items: [
      { kind: 'Track', title: 'Pataraz Linea', body: '48V magnetic track with interchangeable spot, flood, and linear modules.' },
      { kind: 'Downlight', title: 'Pataraz Qu0', body: 'Deep-baffle anti-glare downlight, fixed and adjustable, three beam angles.' },
      { kind: 'Linear', title: 'Pataraz Run', body: 'Continuous recessed and surface runs with seamless joints and diffusers.' },
    ],
    bandQuote: 'Optics first.',
    bandBody: 'Each fixture is published with full photometric data and IES files. Specify with confidence; commission without surprises.',
    bandCta: 'Request a sample',
    bandLink: 'View the spec library',
    footerNote: 'Pataraz · premium architectural luminaires · a brand from Emre\u2019s house.',
    legal: { label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(), href: 'https://pataraz.com' },
    copyright: { label: '© Pataraz', href: 'https://pataraz.com' },
    footerCols: [
      { title: 'Range', links: ['Track', 'Downlights', 'Linear'] },
      { title: 'Specify', links: ['IES files', 'Datasheets', 'BIM objects'] },
      { title: 'Trade', links: ['Distributors', 'Warranty', 'Contact'] },
    ],
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
    items: [
      { kind: 'Essay', title: 'On glare, again', body: 'Why UGR keeps failing the rooms it is supposed to protect — a field reading.' },
      { kind: 'Project', title: 'A mosque, after dark', body: 'Documenting a restrained exterior scheme that resists the floodlight reflex.' },
      { kind: 'Interview', title: 'The specifier\u2019s desk', body: 'A working lighting designer on what survives between render and reality.' },
    ],
    bandQuote: 'Kept, not lost.',
    bandBody: 'The archive is editorial, not promotional. Every entry carries its date, its credits, and its place in the record.',
    bandCta: 'Subscribe',
    bandLink: 'See the editorial index',
    footerNote: 'PLD Türkiye · professional lighting design, archived · independent publication.',
    legal: { label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(), href: 'https://pldturkiye.com' },
    copyright: { label: '© PLD Türkiye', href: 'https://pldturkiye.com' },
    footerCols: [
      { title: 'Read', links: ['Latest', 'Issues', 'Index'] },
      { title: 'Contribute', links: ['Submit', 'Pitch an essay', 'Credits'] },
      { title: 'About', links: ['Masthead', 'Ethics', 'Contact'] },
    ],
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
    items: [
      { kind: 'Ingest', title: 'Read anything', body: 'Parse IES and LDT in bulk, flag malformed files, and normalize units automatically.' },
      { kind: 'Validate', title: 'Catch errors early', body: 'Photometric sanity checks: flux, efficacy, symmetry, and angle coverage.' },
      { kind: 'Export', title: 'Clean datasets', body: 'Emit CSV, JSON, and converted formats with consistent metadata across the set.' },
    ],
    bandQuote: 'Trust the dataset.',
    bandBody: 'Everything runs on your machine. Files never leave the room; the only thing that leaves is a clean, documented export.',
    bandCta: 'Download for desktop',
    bandLink: 'View a sample report',
    footerNote: 'IESDesk · lighting-data tooling · part of Emre\u2019s house.',
    legal: { label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(), href: 'https://iesdesk.com' },
    copyright: { label: '© IESDesk', href: 'https://iesdesk.com' },
    footerCols: [
      { title: 'Product', links: ['Features', 'Formats', 'Changelog'] },
      { title: 'Developers', links: ['Docs', 'CLI', 'API'] },
      { title: 'Company', links: ['Pricing', 'Support', 'Contact'] },
    ],
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
    items: [
      { kind: 'Template', title: 'One layout, any brand', body: 'A single spec-sheet template resolves to the correct brand mark and colour automatically.' },
      { kind: 'Data', title: 'Pull from IESDesk', body: 'Photometric figures come straight from a validated IESDesk dataset — no retyping.' },
      { kind: 'Export', title: 'Print-ready PDF', body: 'Fixed A4/Letter output, ready to attach to a quote or submit to a specifier.' },
    ],
    bandQuote: 'Documented, not designed twice.',
    bandBody: 'The sheet a specifier receives is generated from the same dataset the fixture was validated against — never a separate, hand-built document.',
    bandCta: 'Generate a sheet',
    bandLink: 'View a sample sheet',
    footerNote: 'SpecQuick · spec-sheet tooling · part of Emre\u2019s house.',
    legal: { label: '© Ağustos Teknoloji, 1996–' + new Date().getFullYear(), href: 'https://specquick.com' },
    copyright: { label: '© SpecQuick', href: 'https://specquick.com' },
    footerCols: [
      { title: 'Product', links: ['Features', 'Templates', 'Changelog'] },
      { title: 'Developers', links: ['Docs', 'API'] },
      { title: 'Company', links: ['Pricing', 'Support', 'Contact'] },
    ],
  },
};

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "layout": "sidebar",
  "heroScale": "medium"
}/*EDITMODE-END*/;

function App() {
  const { useTweaks, TweaksPanel, TweakSection, TweakRadio } = window;
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [brand, setBrand] = React.useState('agustos');
  const [theme, setTheme] = React.useState('light');
  const data = SITE[brand];
  const isSidebar = t.layout === 'sidebar';

  const content = (
    <React.Fragment>
      <main id="main">
        <div className="wk-main">
          <window.SiteHero data={data} scale={t.heroScale} />
          <window.SiteWork data={data} />
        </div>
        <window.SiteBand data={data} />
      </main>
      {!isSidebar && <window.SiteFooter brand={brand} data={data} />}
    </React.Fragment>
  );

  const cls = 'wk brand-' + brand + (isSidebar ? ' wk--sidebar' : '');

  return (
    <div className={cls} data-theme={theme === 'dark' ? 'dark' : undefined}>
      <a className="skip-link" href="#main">Skip to content</a>
      {isSidebar ? (
        <React.Fragment>
          <window.SiteSidebar brand={brand} setBrand={setBrand} nav={data.nav} legal={data.legal} theme={theme} setTheme={setTheme} />
          <div className="wk-shell">{content}</div>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <window.SiteHeader brand={brand} setBrand={setBrand} nav={data.nav} />
          {content}
        </React.Fragment>
      )}

      <TweaksPanel>
        <TweakSection label="Layout" />
        <TweakRadio
          label="Navigation"
          value={t.layout}
          options={['topbar', 'sidebar']}
          onChange={(v) => setTweak('layout', v)}
        />
        <TweakSection label="Hero" />
        <TweakRadio
          label="Headline scale"
          value={t.heroScale}
          options={['medium', 'large']}
          onChange={(v) => setTweak('heroScale', v)}
        />
      </TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
