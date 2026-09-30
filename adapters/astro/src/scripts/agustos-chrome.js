/* AĞUSTOS DESIGN SYSTEM v7.4.1 · CHROME BEHAVIOUR
   GENERATED. Do not hand-edit. Run: python3 scripts/build_design_system.py

   It adds what native HTML does not give the chrome. The More menu of the top
   menu (a <details class="site-header__more">) closes on Escape, on a click
   outside it, and when keyboard focus leaves it. An open drawer (a native
   popover: site-header__panel or site-sidebar) closes when keyboard focus
   leaves it, so focus never moves to the page behind the drawer. Without this
   file More still opens and closes on click, and a drawer still closes on
   Escape, an outside click and its close button. Load it once on every page
   with the chrome, with defer. */
(() => {
  if (document.agustosChrome) return;
  document.agustosChrome = true;

  const OPEN = 'details.site-header__more[open]';
  const DRAWER = '.site-header__panel[popover], .site-sidebar[popover]';

  function close(menu, returnFocus) {
    menu.open = false;
    if (returnFocus) menu.querySelector('summary')?.focus();
  }

  // A browser without popovers throws on the selector; its drawers never open.
  function isOpen(drawer) {
    try { return drawer.matches(':popover-open'); } catch { return false; }
  }

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;
    document.querySelectorAll(OPEN).forEach((menu) => close(menu, menu.contains(document.activeElement)));
  });

  document.addEventListener('click', (event) => {
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
