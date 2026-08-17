export interface ChromeLink {
  href: string;
  label: string;
  ariaLabel?: string;
  external?: boolean;
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
  nav?: ChromeLink[];
  cta?: ChromeLink | null;
  languageSwitch?: LanguageSwitch | null;
  theme?: boolean;
  search?: boolean | { labels?: Partial<SearchLabels> };
}

export interface FooterColumn {
  heading: string;
  ariaLabel?: string;
  links: ChromeLink[];
}

export interface FooterConfig {
  description?: string;
  columns?: FooterColumn[];
}

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
