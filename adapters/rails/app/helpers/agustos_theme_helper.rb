module AgustosThemeHelper
  BRAND_CLASSES = {
    agustos: "brand-agustos",
    pataraz: "brand-pataraz",
    pld: "brand-pld",
    photo: "brand-photo"
  }.freeze

  BRAND_WORDMARKS = {
    agustos: "ağustos",
    pataraz: "pataraz",
    pld: "pld türkiye",
    photo: "photometric"
  }.freeze

  def agustos_theme(brand: :agustos, lang: :tr, substrate: :cream, title: nil, description: nil, nav: nil)
    @agustos_theme = {
      brand: brand.to_sym,
      lang: lang.to_s,
      substrate: substrate.to_sym,
      title: title,
      description: description,
      nav: nav
    }.compact
  end

  def agustos_theme_config
    {
      brand: :agustos,
      lang: "tr",
      substrate: :cream,
      title: "Ağustos",
      description: "Typography-first design system.",
      nav: [
        { label: "Home", href: "/" },
        { label: "Writing", href: "/yazilar" },
        { label: "Typography", href: "/typography" }
      ]
    }.merge(@agustos_theme || {})
  end

  def agustos_body_class
    config = agustos_theme_config
    classes = [BRAND_CLASSES.fetch(config[:brand], BRAND_CLASSES[:agustos])]
    classes << "paper-white" if config[:substrate] == :white
    classes.join(" ")
  end

  def agustos_wordmark
    BRAND_WORDMARKS.fetch(agustos_theme_config[:brand], BRAND_WORDMARKS[:agustos])
  end

  def agustos_page_title
    agustos_theme_config[:title]
  end

  def agustos_meta_description
    agustos_theme_config[:description]
  end

  def agustos_nav_items
    agustos_theme_config[:nav]
  end
end

