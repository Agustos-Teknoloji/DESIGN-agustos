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

/**
 * The footer is light and small: the lockup, one footnote line, and one row of
 * links for social, legal, and language. No column headings, no repeat of the
 * top menu, no button.
 */
export interface FooterConfig {
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

export const CHROME_LABELS: Record<'en' | 'tr', { more: string; skip: string; nav: string; footer: string; openMenu: string; closeMenu: string }> = {
  en: { more: 'More', skip: 'Skip to content', nav: 'Main menu', footer: 'Footer', openMenu: 'Open menu', closeMenu: 'Close menu' },
  tr: { more: 'Daha fazla', skip: 'İçeriğe geç', nav: 'Ana menü', footer: 'Alt menü', openMenu: 'Menüyü aç', closeMenu: 'Menüyü kapat' },
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
