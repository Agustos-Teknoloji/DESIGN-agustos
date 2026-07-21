module AgustosThemeHelper
  UNSET = Object.new.freeze
  BRAND_CLASSES = {
    agustos: "brand-agustos",
    pataraz: "brand-pataraz",
    pld: "brand-pld",
    photo: "brand-photo",
    specquick: "brand-specquick"
  }.freeze

  BRAND_WORDMARKS = {
    agustos: "ağustos",
    pataraz: "pataraz",
    pld: "pld türkiye",
    photo: "photometric",
    specquick: "specquick"
  }.freeze

  DEFAULT_NAV = [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
    { label: "Writing", href: "/blog" },
    { label: "Typography", href: "/typography" }
  ].freeze

  DEFAULT_FOOTER_COLUMNS = [
    { heading: "Explore", links: [{ label: "Home", href: "/" }, { label: "About", href: "/about" }] },
    { heading: "Content", links: [{ label: "Writing", href: "/blog" }, { label: "Typography", href: "/typography" }] },
    {
      heading: "Repository",
      links: [
        { label: "Source", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos", external: true },
        { label: "Design spec", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos/blob/main/DESIGN.md", external: true },
        { label: "Asset index", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos/blob/main/ASSETS.md", external: true }
      ]
    }
  ].freeze

  SEARCH_LABELS = {
    en: { placeholder: "Search", aria: "Search this site", loading: "Searching...", submit: "Search" },
    tr: { placeholder: "Ara", aria: "Sitede ara", loading: "Aranıyor...", submit: "Ara" }
  }.freeze

  def agustos_theme(
    brand: :agustos,
    lang: :tr,
    substrate: :white,
    title: nil,
    description: nil,
    home_href: nil,
    nav: nil,
    cta: UNSET,
    language_switch: nil,
    theme: true,
    search: nil,
    footer: nil
  )
    @agustos_theme = {
      brand: brand.to_sym,
      lang: lang.to_s,
      substrate: substrate.to_sym,
      title: title,
      description: description,
      home_href: home_href,
      nav: nav,
      language_switch: language_switch,
      theme: theme,
      search: search,
      footer: footer
    }.compact
    @agustos_theme[:cta] = cta unless cta.equal?(UNSET)
    @agustos_theme
  end

  def agustos_theme_config
    {
      brand: :agustos,
      lang: "tr",
      substrate: :white,
      title: "Ağustos",
      description: "Typography-first design system.",
      home_href: "/",
      nav: DEFAULT_NAV,
      cta: { label: "View source", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos", external: true },
      language_switch: nil,
      theme: true,
      search: nil,
      footer: {
        description: "Ağustos Design System · multi-brand typography and chrome",
        columns: DEFAULT_FOOTER_COLUMNS
      }
    }.merge(@agustos_theme || {})
  end

  def agustos_body_class
    config = agustos_theme_config
    classes = ["agustos-layout", BRAND_CLASSES.fetch(config[:brand], BRAND_CLASSES[:agustos])]
    classes << "paper-white" if config[:substrate] == :white
    classes.join(" ")
  end

  def agustos_wordmark
    BRAND_WORDMARKS.fetch(agustos_theme_config[:brand], BRAND_WORDMARKS[:agustos])
  end

  def agustos_page_title = agustos_theme_config[:title]
  def agustos_meta_description = agustos_theme_config[:description]
  def agustos_nav_items = agustos_theme_config[:nav] || []
  def agustos_header_cta = agustos_theme_config[:cta]
  def agustos_language_switch = agustos_theme_config[:language_switch]
  def agustos_search_config = agustos_theme_config[:search]
  def agustos_footer_config = agustos_theme_config[:footer] || {}

  def agustos_value(value, key, default = nil)
    value&.fetch(key, value&.fetch(key.to_s, default))
  end

  def agustos_nav_active?(href)
    path = request.path
    href == "/" ? path == "/" : path == href || path.start_with?("#{href}/")
  end

  def agustos_link_html_options(link, class_name:)
    options = { class: class_name }
    options[:aria] = { label: agustos_value(link, :aria_label) } if agustos_value(link, :aria_label)
    if agustos_value(link, :external, false)
      options[:target] = "_blank"
      options[:rel] = "noopener noreferrer"
    end
    options
  end

  def agustos_search_labels
    locale = agustos_theme_config[:lang] == "tr" ? :tr : :en
    SEARCH_LABELS.fetch(locale).merge(agustos_value(agustos_search_config, :labels, {}) || {})
  end
end
