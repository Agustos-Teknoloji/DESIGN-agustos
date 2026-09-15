/* dashboard.jsx — IESDesk main views: topbar, stat tiles, and the validation
   table. Numbers use the display family + tabular figures (the "dashboard
   numerals" role). Status is carried by text + glyph, never colour alone —
   there is no brand hue to lean on here, so "Valid" is a solid ink pill;
   everything else is ink on white. */
const { Button, Badge, Link } = window.AUstosDesignSystem_7fee69;

function Status({ kind }) {
  if (kind === 'valid')   return <Badge variant="solid">✓ Valid</Badge>;
  if (kind === 'flagged') return <span className="pq-status pq-status--flag">⚠ Flagged</span>;
  if (kind === 'error')   return <span className="pq-status pq-status--err">✕ Error</span>;
  return <span className="pq-status pq-status--skip">– Skipped</span>;
}

const STATS = [
  { label: 'Files in batch', value: '4,218', sub: 'IES · LDT' },
  { label: 'Valid', value: '4,061', sub: '96.3% pass', featured: true },
  { label: 'Flagged', value: '157', sub: '142 fixable' },
  { label: 'Median efficacy', value: '118', sub: 'lm / W' },
];

const ROWS = [
  { file: 'osram-kreios-g3-840.ies',     fmt: 'IES',  flux: '3,240', eff: '129', beam: '38°', status: 'valid' },
  { file: 'pataraz-linea-spot-927.ldt',  fmt: 'LDT',  flux: '1,180', eff: '112', beam: '24°', status: 'valid' },
  { file: 'pataraz-run-2700k.ldt',       fmt: 'LDT',  flux: '4,860', eff: '121', beam: '—',   status: 'valid' },
  { file: 'erco-optec-spot-30.ies',      fmt: 'IES',  flux: '2,010', eff: '—',   beam: '30°', status: 'flagged' },
  { file: 'generic-panel-600x600.ies',   fmt: 'IES',  flux: '3,600', eff: '108', beam: '—',   status: 'valid' },
  { file: 'unnamed-export-0042.ldt',     fmt: 'LDT',  flux: '—',     eff: '—',   beam: '—',   status: 'error' },
  { file: 'pataraz-qu0-fixed-930.ies',   fmt: 'IES',  flux: '1,540', eff: '124', beam: '15°', status: 'valid' },
  { file: 'tracklight-batch-legacy.ldt', fmt: 'LDT',  flux: '2,720', eff: '96',  beam: '40°', status: 'flagged' },
];

function StatTile({ s }) {
  return (
    <div className={'pq-stat' + (s.featured ? ' pq-stat--featured' : '')}>
      <div className="type-h4 pq-stat__label">{s.label}</div>
      <div className="pq-stat__value pq-num">{s.value}</div>
      <div className="pq-stat__sub">{s.sub}</div>
    </div>
  );
}

function PqDashboard({ view }) {
  return (
    <section className="pq-main">
      <header className="pq-topbar">
        <div className="pq-topbar__lead">
          <div className="pq-crumb">
            <span>Batches</span>
            <span aria-hidden="true" className="pq-crumb__sep">/</span>
            <span className="pq-crumb__here">catalogue-2026-q2</span>
          </div>
          <h1 className="type-h1 pq-topbar__title">Validation run</h1>
        </div>
        <div className="pq-topbar__actions">
          <Button variant="ghost">Re-run</Button>
          <Button variant="primary">Export dataset</Button>
        </div>
      </header>

      <div className="pq-scroll">
        <div className="pq-progress">
          <div className="pq-progress__head">
            <span className="type-h4">Processing complete</span>
            <span className="pq-num pq-progress__pct">4,218 / 4,218</span>
          </div>
          <div className="pq-progress__track"><div className="pq-progress__fill" style={{ width: '100%' }}></div></div>
          <p className="pq-progress__note">Parsed locally in 11.4s · LM-63 + EULUMDAT · units normalized to SI.</p>
        </div>

        <div className="pq-stats">
          {STATS.map((s) => <StatTile key={s.label} s={s} />)}
        </div>

        <div className="pq-table-head">
          <h2 className="type-h2 pq-table-title">Files</h2>
          <div className="pq-table-tools">
            <span className="pq-filter is-active">All</span>
            <span className="pq-filter">Flagged</span>
            <span className="pq-filter">Errors</span>
            <Link href="#" variant="secondary">Download report</Link>
          </div>
        </div>

        <div className="pq-table" role="table" aria-label="Validation results">
          <div className="pq-tr pq-tr--head" role="row">
            <span role="columnheader">File</span>
            <span role="columnheader">Format</span>
            <span role="columnheader" className="pq-r">Flux (lm)</span>
            <span role="columnheader" className="pq-r">Efficacy (lm/W)</span>
            <span role="columnheader" className="pq-r">Beam</span>
            <span role="columnheader">Status</span>
          </div>
          {ROWS.map((r) => (
            <div className="pq-tr" role="row" key={r.file}>
              <span role="cell" className="pq-file"><code>{r.file}</code></span>
              <span role="cell" className="pq-fmt">{r.fmt}</span>
              <span role="cell" className="pq-r pq-num">{r.flux}</span>
              <span role="cell" className="pq-r pq-num">{r.eff}</span>
              <span role="cell" className="pq-r pq-num">{r.beam}</span>
              <span role="cell"><Status kind={r.status} /></span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
window.PqDashboard = PqDashboard;
