export interface ChromeLink {
  href: string;
  label: string;
  ariaLabel?: string;
  external?: boolean;
  /** Language of the destination, for a language link (for example 'en'). */
  hreflang?: string;
}

export interface LanguageSwitch extends ChromeLink {
  code: string;
}

export interface SearchLabels {
  placeholder: string;
  aria: string;
  loading: string;
  empty: string;
  unavailable: string;
  result: string;
  results: string;
  pages: string;
  posts: string;
}

export interface HeaderConfig {
  homeHref?: string;
  /**
   * Top-menu items. The menu shows at most five: a longer list keeps its first
   * four and puts the rest under one More menu (site-header__more).
   */
  nav?: ChromeLink[];
  /** Label of the More menu. Default 'Daha fazla' for tr, 'More' otherwise. */
  moreLabel?: string;
  cta?: ChromeLink | null;
  languageSwitch?: LanguageSwitch | null;
  /** Product UI only. Marketing chrome omits the theme toggle. */
  theme?: boolean;
  search?: boolean | { labels?: Partial<SearchLabels> };
}

/** One group of the optional footer site map: a sentence-case title over at most five links. */
export interface FooterGroup {
  title: string;
  links: ChromeLink[];
}

/**
 * The footer is light: the lockup, one footnote line, and one row of links for
 * social, legal, and language. No button. An optional site map sits above that
 * row: the lockup with an address block, and at most three short groups.
 */
export interface FooterConfig {
  /** Lines of the contact block, for example the legal name and the address. */
  address?: string[];
  /** Phone and email under the address, for example { href: 'tel:+908508851996', label: '+90 850 885 1996' }. */
  contact?: ChromeLink[];
  /** At most three groups of at most five links: the pages people look for, not every page. */
  groups?: FooterGroup[];
  /** The one footnote line under the lockup, for example '© Ağustos Teknoloji, 1996–2026'. */
  note?: string;
  links?: ChromeLink[];
  /** Accessible name of the footer nav. Default 'Alt menü' for tr, 'Footer' otherwise. */
  ariaLabel?: string;
}

/** The top menu shows at most this many items; the rest go under More. */
export const NAV_LIMIT = 5;

/** [menu items, More items]. More than five keeps four and moves the rest. */
export function splitNav<T>(items: T[]): [T[], T[]] {
  if (items.length <= NAV_LIMIT) return [items, []];
  return [items.slice(0, NAV_LIMIT - 1), items.slice(NAV_LIMIT - 1)];
}

/**
 * aria-current for a menu item. 'page' when the pathname is the item's own
 * URL; 'true' when the item is a section that holds the page, such as
 * '/haberler/' on '/haberler/guncel/'; undefined otherwise. Trailing slashes
 * do not count, and the home item '/' is only ever exact. A link with a query
 * or a fragment ('/about#team') is a place on a page, never the page itself.
 */
export function currentState(href: string, pathname: string): 'page' | 'true' | undefined {
  if (!href.startsWith('/') || href.startsWith('//') || /[?#]/.test(href)) return undefined;
  const trim = (path = '') => path.replace(/[?#].*$/, '').replace(/\/+$/, '') || '/';
  const item = trim(href);
  const page = trim(pathname);
  if (item === page) return 'page';
  if (item !== '/' && page.startsWith(`${item}/`)) return 'true';
  return undefined;
}

export const CHROME_LABELS: Record<'en' | 'tr', { more: string; skip: string; nav: string; footer: string; openMenu: string; closeMenu: string; siteMap: string }> = {
  en: { more: 'More', skip: 'Skip to content', nav: 'Main menu', footer: 'Footer', openMenu: 'Open menu', closeMenu: 'Close menu', siteMap: 'Site map' },
  tr: { more: 'Daha fazla', skip: 'İçeriğe geç', nav: 'Ana menü', footer: 'Alt menü', openMenu: 'Menüyü aç', closeMenu: 'Menüyü kapat', siteMap: 'Site haritası' },
};

export const SEARCH_LABELS: Record<'en' | 'tr', SearchLabels> = {
  en: {
    placeholder: 'Search',
    aria: 'Search this site',
    loading: 'Searching...',
    empty: 'No results',
    unavailable: 'Search is unavailable',
    result: 'result',
    results: 'results',
    pages: 'Pages',
    posts: 'Posts',
  },
  tr: {
    placeholder: 'Ara',
    aria: 'Sitede ara',
    loading: 'Aranıyor...',
    empty: 'Sonuç yok',
    unavailable: 'Arama kullanılamıyor',
    result: 'sonuç',
    results: 'sonuç',
    pages: 'Sayfalar',
    posts: 'Yazılar',
  },
};
