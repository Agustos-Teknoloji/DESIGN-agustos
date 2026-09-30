/* AĞUSTOS DESIGN SYSTEM v7.3.2 · CHROME BEHAVIOUR
   GENERATED. Do not hand-edit. Run: python3 scripts/build_design_system.py

   Optional. It adds what native HTML does not give the More menu of the top
   menu (a <details class="site-header__more">): it closes on Escape, on a
   click outside it, and when keyboard focus leaves it. Without this file the
   menu still opens and closes on click. Drawers need no script: they are
   native popovers with a close button. Load it once, anywhere, with defer. */
(() => {
  if (document.agustosChrome) return;
  document.agustosChrome = true;

  const OPEN = 'details.site-header__more[open]';

  function close(menu, returnFocus) {
    menu.open = false;
    if (returnFocus) menu.querySelector('summary')?.focus();
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
    const menu = event.target.closest?.(OPEN);
    if (menu && event.relatedTarget && !menu.contains(event.relatedTarget)) close(menu, false);
  });
})();
