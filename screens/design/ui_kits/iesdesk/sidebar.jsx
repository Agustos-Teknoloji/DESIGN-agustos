/* sidebar.jsx — IESDesk product sidebar.
   Lockup (iesdesk, off-black) + functional nav + storage meter + theme toggle.
   Product UI: white/dark substrate. No brand hue to ration — accents are
   ink and the light-gray functional surface instead. */
const { Lockup } = window.AUstosDesignSystem_7fee69;

const NAV = [
  { id: 'batches',    label: 'Batches',    glyph: '▦', count: 6 },
  { id: 'files',      label: 'Files',      glyph: '≣', count: '4,218' },
  { id: 'validation', label: 'Validation', glyph: '◬', count: 157 },
  { id: 'exports',    label: 'Exports',    glyph: '↧', count: 12 },
  { id: 'formats',    label: 'Formats',    glyph: '⌗' },
];

function PqSidebar({ view, setView, theme, setTheme }) {
  return (
    <aside className="pq-side">
      <div className="pq-side__brand">
        <Lockup brand="iesdesk" size={19} />
      </div>

      <nav className="pq-nav" aria-label="Primary">
        {NAV.map((n) => (
          <button
            key={n.id}
            className={'pq-nav__item' + (n.id === view ? ' is-active' : '')}
            onClick={() => setView(n.id)}
            aria-current={n.id === view ? 'page' : undefined}
          >
            <span className="pq-nav__glyph" aria-hidden="true">{n.glyph}</span>
            <span className="pq-nav__label">{n.label}</span>
            {n.count != null && <span className="pq-nav__count">{n.count}</span>}
          </button>
        ))}
      </nav>

      <div className="pq-side__foot">
        <div className="pq-meter" aria-label="Local cache">
          <div className="pq-meter__head">
            <span>Local cache</span>
            <span className="pq-num">1.8 / 4 GB</span>
          </div>
          <div className="pq-meter__track"><div className="pq-meter__fill" style={{ width: '45%' }}></div></div>
          <p className="pq-side__note">Files never leave this machine.</p>
        </div>

        <button
          className="pq-theme"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          aria-pressed={theme === 'dark'}
        >
          <span aria-hidden="true">{theme === 'dark' ? '☾' : '☀'}</span>
          {theme === 'dark' ? 'Dark' : 'Light'}
        </button>
      </div>
    </aside>
  );
}
window.PqSidebar = PqSidebar;
