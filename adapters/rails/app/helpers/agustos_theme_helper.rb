module AgustosThemeHelper
  UNSET = Object.new.freeze
  BRAND_CLASSES = {
    agustos: "brand-agustos",
    pataraz: "brand-pataraz",
    pld: "brand-pld",
    iesdesk: "brand-iesdesk",
    specquick: "brand-specquick"
  }.freeze

  BRAND_WORDMARKS = {
    agustos: "ağustos",
    pataraz: "pataraz",
    pld: "pld türkiye",
    iesdesk: "iesdesk",
    specquick: "specquick"
  }.freeze

  DEFAULT_NAV = [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
    { label: "Writing", href: "/blog" },
    { label: "Typography", href: "/typography" }
  ].freeze

  # The footer's bottom row of links for social, legal and language. It never
  # holds a button. footer: { address:, groups: } adds the optional site map.
  DEFAULT_FOOTER_LINKS = [
    { label: "Source", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos", external: true },
    { label: "Design spec", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos/blob/main/DESIGN.md", external: true },
    { label: "Asset index", href: "https://github.com/Agustos-Teknoloji/DESIGN-agustos/blob/main/ASSETS.md", external: true }
  ].freeze

  # The top menu shows at most five items. A longer nav keeps its first four
  # and puts the rest under one More menu.
  NAV_LIMIT = 5

  # The exact themeScript of kit.json. The layout puts it in <head>, before the
  # stylesheets, so a stored dark choice applies before the first paint.
  THEME_SCRIPT = 'try{if(localStorage.getItem("agustos:theme")==="dark")document.documentElement.setAttribute("data-theme","dark")}catch(e){}'

  CHROME_LABELS = {
    en: { more: "More", skip: "Skip to content", nav: "Main menu", footer: "Footer", sidebar: "Application menu", sections: "Sections", open_menu: "Open menu", close_menu: "Close menu", site_map: "Site map", theme_to_dark: "Dark theme", theme_to_light: "Light theme" },
    tr: { more: "Daha fazla", skip: "İçeriğe geç", nav: "Ana menü", footer: "Alt menü", sidebar: "Uygulama menüsü", sections: "Bölümler", open_menu: "Menüyü aç", close_menu: "Menüyü kapat", site_map: "Site haritası", theme_to_dark: "Koyu tema", theme_to_light: "Açık tema" }
  }.freeze

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
    more_label: nil,
    cta: UNSET,
    language_switch: nil,
    theme: false,
    shell: :marketing,
    screen: nil,
    search: nil,
    footer: nil,
    sidebar: nil
  )
    @agustos_theme = {
      brand: brand.to_sym,
      lang: lang.to_s,
      substrate: substrate.to_sym,
      title: title,
      description: description,
      home_href: home_href,
      nav: nav,
      more_label: more_label,
      language_switch: language_switch,
      theme: theme,
      shell: shell&.to_sym,
      screen: screen&.to_s&.tr("_", "-"),
      search: search,
      footer: footer,
      sidebar: sidebar
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
      cta: { label: "Start a project", href: "/about" },
      language_switch: nil,
      theme: false,
      shell: :marketing,
      screen: nil,
      search: nil,
      footer: {
        note: "Ağustos Design System · © #{Time.now.year}",
        links: DEFAULT_FOOTER_LINKS
      },
      sidebar: nil
    }.merge(@agustos_theme || {})
  end

  def agustos_body_class
    config = agustos_theme_config
    classes = [BRAND_CLASSES.fetch(config[:brand], BRAND_CLASSES[:agustos])]
    classes << "paper-white" if config[:substrate] == :white
    # Chrome follows the screen family, not the brand: websites get the top
    # menu and footer; product UI alone gets the sidebar.
    classes << (agustos_product_shell? ? "site-sidebar-layout" : "agustos-layout")
    classes.join(" ")
  end

  # The kit screen this page is, rendered as data-screen on <body>. The kit
  # checker holds the page to that screen's row (primary CTA limit, quotes,
  # theme). Product UI defaults to the app shell; a marketing page names its own
  # (home, static, content, content-index, products, product-finder, product,
  # spec-sheet) or the checker reports the page.
  def agustos_screen
    agustos_theme_config[:screen] || (agustos_product_shell? ? "app-shell" : nil)
  end

  def agustos_wordmark
    BRAND_WORDMARKS.fetch(agustos_theme_config[:brand], BRAND_WORDMARKS[:agustos])
  end

  def agustos_page_title = agustos_theme_config[:title]
  def agustos_meta_description = agustos_theme_config[:description]
  def agustos_nav_items = agustos_theme_config[:nav] || []
  def agustos_header_cta = agustos_theme_config[:cta]
  def agustos_language_switch = agustos_theme_config[:language_switch]
  def agustos_theme_toggle? = agustos_theme_config[:theme] == true
  def agustos_product_shell? = agustos_theme_config[:shell] == :product
  def agustos_header_utility? = agustos_language_switch || agustos_theme_toggle?

  # The Stimulus controllers on <body>: none. The kit script agustos/chrome.js
  # handles the theme switch, so the adapter ships no theme controller.
  def agustos_body_controller = ""
  def agustos_search_config = agustos_theme_config[:search]
  def agustos_footer_config = agustos_theme_config[:footer] || {}
  def agustos_footer_note = agustos_value(agustos_footer_config, :note)
  def agustos_footer_links = agustos_value(agustos_footer_config, :links, []) || []
  # The optional site map: address lines, and at most three groups of
  # { title:, links: [] } with at most five links each.
  def agustos_footer_address = agustos_value(agustos_footer_config, :address, []) || []
  def agustos_footer_contact = agustos_value(agustos_footer_config, :contact, []) || []
  def agustos_footer_groups = agustos_value(agustos_footer_config, :groups, []) || []
  def agustos_footer_map? = agustos_footer_address.any? || agustos_footer_contact.any? || agustos_footer_groups.any?
  def agustos_footer_aria_label = agustos_value(agustos_footer_config, :aria_label) || agustos_chrome_labels[:footer]
  def agustos_sidebar_config = agustos_theme_config[:sidebar] || {}
  def agustos_sidebar_items = agustos_value(agustos_sidebar_config, :nav, []) || []
  def agustos_sidebar_note = agustos_value(agustos_sidebar_config, :note)

  def agustos_chrome_labels
    CHROME_LABELS.fetch(agustos_theme_config[:lang] == "tr" ? :tr : :en)
  end

  def agustos_more_label = agustos_theme_config[:more_label] || agustos_chrome_labels[:more]

  # [menu items, More items]. Five or fewer render as they are; more than five
  # keep the first four in the menu and move the rest under More.
  def agustos_nav_split
    items = agustos_nav_items
    return [items, []] if items.size <= NAV_LIMIT

    [items.first(NAV_LIMIT - 1), items.drop(NAV_LIMIT - 1)]
  end

  def agustos_value(value, key, default = nil)
    value&.fetch(key, value&.fetch(key.to_s, default))
  end

  # "page" when the request path is the item's own URL; "true" when the item
  # is a section that holds the page, such as /haberler/ on /haberler/guncel/;
  # nil otherwise. Trailing slashes do not count, and "/" is only ever exact.
  # A link with a query or a fragment (/about#team) is a place on a page, never
  # the page itself; an item that needs it passes current: true.
  def agustos_nav_current(href)
    href = href.to_s
    return nil unless href.start_with?("/") && !href.start_with?("//") && !href.match?(/[?#]/)

    trim = ->(path) { path.sub(/[?#].*\z/, "").sub(%r{/+\z}, "").then { |p| p.empty? ? "/" : p } }
    item = trim.call(href)
    page = trim.call(request.path.to_s)
    return "page" if item == page
    return "true" if item != "/" && page.start_with?("#{item}/")

    nil
  end

  def agustos_nav_active?(href) = !agustos_nav_current(href).nil?

  def agustos_link_html_options(link, class_name:)
    options = { class: class_name }
    options[:aria] = { label: agustos_value(link, :aria_label) } if agustos_value(link, :aria_label)
    options[:hreflang] = agustos_value(link, :hreflang) if agustos_value(link, :hreflang)
    # A language link names its language (WCAG 3.1.2), so a screen reader pronounces it.
    link_lang = agustos_value(link, :hreflang) || agustos_value(link, :code)
    options[:lang] = link_lang.to_s.downcase if link_lang
    if agustos_value(link, :external, false)
      options[:target] = "_blank"
      options[:rel] = "noopener noreferrer"
    end
    options
  end

  # Link options plus aria-current: "page" for the current page, "true" for the
  # section that holds it. An item may force "page" with current: true (for
  # example an in-page #anchor).
  def agustos_nav_link_options(item, class_name:)
    options = agustos_link_html_options(item, class_name: class_name)
    current = agustos_value(item, :current, false) ? "page" : agustos_nav_current(agustos_value(item, :href))
    options[:aria] = (options[:aria] || {}).merge(current: current) if current
    options
  end

  def agustos_search_labels
    locale = agustos_theme_config[:lang] == "tr" ? :tr : :en
    SEARCH_LABELS.fetch(locale).merge(agustos_value(agustos_search_config, :labels, {}) || {})
  end
end
