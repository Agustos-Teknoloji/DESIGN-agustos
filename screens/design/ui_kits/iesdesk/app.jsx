/* app.jsx — composes IESDesk. White substrate always (product UI never uses
   the cream band — that's a marketing-site-only surface), opt-in warm dark
   via data-theme on <html>. Brand scope is iesdesk — off-black, like every
   secondary brand; accents below use ink/surface, never colour. */

function PqApp() {
  const [view, setView] = React.useState('validation');
  const [theme, setTheme] = React.useState('light');

  React.useEffect(() => {
    if (theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
  }, [theme]);

  return (
    <div className="pq brand-iesdesk">
      <a className="skip-link" href="#pq-main">Skip to content</a>
      <window.PqSidebar view={view} setView={setView} theme={theme} setTheme={setTheme} />
      <div id="pq-main" className="pq-stage">
        <window.PqDashboard view={view} />
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<PqApp />);
