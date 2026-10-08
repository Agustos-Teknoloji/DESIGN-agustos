# Ağustos WordPress Adapter

This adapter translates the Ağustos Design System (kit v7.12.0) into WordPress Global Styles. It is an adapter, not a complete theme.

Copy `theme.json` to a block theme root and `assets/css/agustos.css` to the theme assets directory. Merge `functions.php.example` into the theme bootstrap to enqueue the generated behavior and recipe layer.

Both generated files come from `tokens/design-tokens.json`; never edit them directly:

```bash
python3 scripts/build_design_system.py
python3 scripts/build_design_system.py --check
```

Use WordPress blocks for native authoring. Apply the shared recipe classes (`agustos-section`, `agustos-card-grid`, `agustos-card`, `agustos-chrome-link`) only where Global Styles cannot express the intended composition.

Set the site brand on the body or a wrapping block with `brand-agustos`, `brand-pataraz`, `brand-pld`, `brand-iesdesk`, or `brand-specquick`. Add `paper-white` for the white working substrate. The brand sets the identity ink only; it never picks the chrome.

## Chrome

A WordPress site is a website, so it uses the top menu and the footer, whatever the brand. The sidebar (`site-sidebar*`) is for product UI. A theme may add the kit theme switch; without it the site stays light.

**Header template part.** At most five menu items. With more than five, keep the first four and put the rest in one More menu, as the last child of `site-header__nav`:

```html
<nav class="site-header__nav" aria-label="Ana menü">
  <a class="site-header__link" href="/aydinlatma" aria-current="page">Aydınlatma</a>
  <a class="site-header__link" href="/danismanlik">Danışmanlık</a>
  <a class="site-header__link" href="/blog">Yazılar</a>
  <a class="site-header__link" href="/biz-kimiz">Biz kimiz</a>
  <details class="site-header__more">
    <summary class="site-header__link">Daha fazla</summary>
    <div class="site-header__more-menu">
      <a class="site-header__more-link" href="/gecmis-markalar">Geçmiş markalar</a>
      <a class="site-header__more-link" href="/kariyer">Kariyer</a>
    </div>
  </details>
</nav>
```

Label the More menu "Daha fazla" on Turkish sites and "More" on English ones. The current page carries `aria-current="page"`, on a `site-header__more-link` too. On a nested page, the parent section carries `aria-current="true"`, never `page`, so a screen reader does not announce the parent as the current page; the kit gives both the red rule. `wp_nav_menu` already sets `page` on the current item; the filter in `functions.php.example` adds `true` to its ancestors. A custom nav walker that renders `wp_nav_menu` items should apply the same split.

**Footer template part.** One note line and one row of links for social, legal, and language, and no button. The optional site map (`site-footer__map`, v7.1.0) goes above this row; copy it from `ui/starter.html`. WordPress publishes `wp-sitemap.xml` by itself since 5.5; register it in Google Search Console:

```html
<footer class="site-footer">
  <div class="site-footer__inner site-frame">
    <div class="site-footer__brand">
      <!-- the site-lockup markup from ui/starter.html -->
      <p class="type-footnote">© Ağustos Teknoloji, 1996–2026</p>
    </div>
    <nav aria-label="Alt menü">
      <ul class="site-footer__links">
        <li><a class="site-footer__link" href="https://www.linkedin.com/company/agustostek/" rel="noopener">LinkedIn</a></li>
        <li><a class="site-footer__link" href="/gizlilik-politikasi">Gizlilik ve KVKK</a></li>
        <li><a class="site-footer__link" href="/en" hreflang="en">English</a></li>
      </ul>
    </nav>
  </div>
</footer>
```

**Hero.** Open a page with a `type-hero` headline, a `type-hero-deck`, and a `<div class="hero-actions">` holding one `agustos-button agustos-button--primary` and one `agustos-button agustos-button--secondary`. Wrap one to four words of the headline in `<mark class="type-highlight">`, once per page. Close with one `band band--cream`.

> Building a UI in a repository that is not one of these adapters? Use the distribution kit
> at [`ui/UI-KIT.md`](../../ui/UI-KIT.md) instead — it needs no framework integration.
