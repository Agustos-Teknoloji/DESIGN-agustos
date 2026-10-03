/* AĞUSTOS DESIGN SYSTEM v7.7.0 · CHROME BEHAVIOUR
   GENERATED. Do not hand-edit. Run: python3 scripts/build_design_system.py

   It adds what native HTML does not give the chrome. The More menu of the top
   menu (a <details class="site-header__more">) closes on Escape, on a click
   outside it, and when keyboard focus leaves it. An open drawer (a native
   popover: site-header__panel or site-sidebar) closes when keyboard focus
   leaves it, so focus never moves to the page behind the drawer. Without this
   file More still opens and closes on click, and a drawer still closes on
   Escape, an outside click and its close button. Below 1024px it opens every
   More of an open drawer, so each group shows; without this file each More
   folds and opens on a tap. Load it once on every page
   with the chrome, with defer. A theme switch (a button with
   data-agustos-theme) flips data-theme on <html> and keeps the choice in
   localStorage under agustos:theme. The inline head script in UI-KIT.md
   applies a stored dark choice before the first paint. The device setting is
   never read. */
(() => {
  if (document.agustosChrome) return;
  document.agustosChrome = true;

  // An unfolded More (inside an open drawer) never closes on Escape, a click or focus.
  const OPEN = 'details.site-header__more[open]:not([data-agustos-unfold])';
  const DRAWER_MODE = window.matchMedia('(max-width: 1023px)');
  const PANEL_MORE = '.site-header__panel details.site-header__more';
  const DRAWER = '.site-header__panel[popover], .site-sidebar[popover]';
  const SWITCH = '[data-agustos-theme]';
  const THEME_KEY = 'agustos:theme';

  // Light is the default: no attribute. Dark is the user's choice alone.
  function flipTheme() {
    const root = document.documentElement;
    const dark = root.getAttribute('data-theme') !== 'dark';
    if (dark) root.setAttribute('data-theme', 'dark');
    else root.removeAttribute('data-theme');
    // Blocked storage (a private window) still flips the page in view.
    try { localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light'); } catch { /* not kept */ }
  }

  function close(menu, returnFocus) {
    menu.open = false;
    if (returnFocus) menu.querySelector('summary')?.focus();
  }

  // A browser without popovers throws on the selector; its drawers never open.
  function isOpen(drawer) {
    try { return drawer.matches(':popover-open'); } catch { return false; }
  }

  // Below 1024px the drawer shows every More open, its summary as a small title
  // (v7.7.0). It runs on each drawer open, so a swapped page body is covered.
  function unfold(on) {
    document.querySelectorAll(PANEL_MORE).forEach((menu) => {
      const summary = menu.querySelector('summary');
      if (on) {
        menu.dataset.agustosUnfold = '';
        menu.open = true;
        summary?.setAttribute('tabindex', '-1');
      } else if ('agustosUnfold' in menu.dataset) {
        delete menu.dataset.agustosUnfold;
        menu.open = false;
        summary?.removeAttribute('tabindex');
      }
    });
  }

  // toggle does not bubble, so listen in the capture phase.
  document.addEventListener('toggle', (event) => {
    const target = event.target;
    if (target.matches?.('.site-header__panel[popover]') && isOpen(target)) unfold(DRAWER_MODE.matches);
    // A screen reader can still activate the summary: keep the menu open.
    if (target.matches?.('details[data-agustos-unfold]') && !target.open && DRAWER_MODE.matches) target.open = true;
  }, true);

  DRAWER_MODE.addEventListener('change', (event) => { if (!event.matches) unfold(false); });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll(OPEN).forEach((menu) => close(menu, menu.contains(document.activeElement)));
  });

  document.addEventListener('click', (event) => {
    if (event.target.closest?.(SWITCH)) flipTheme();
    document.querySelectorAll(OPEN).forEach((menu) => {
      if (!menu.contains(event.target)) close(menu, false);
    });
  });

  document.addEventListener('focusout', (event) => {
    const leaving = event.relatedTarget;
    if (!leaving) return;
    const menu = event.target.closest?.(OPEN);
    if (menu && !menu.contains(leaving)) close(menu, false);
    const drawer = event.target.closest?.(DRAWER);
    if (drawer && isOpen(drawer) && !drawer.contains(leaving)) drawer.hidePopover();
  });
})();
