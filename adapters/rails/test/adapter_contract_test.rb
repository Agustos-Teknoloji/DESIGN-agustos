require "erb"
require "minitest/autorun"
require_relative "../app/helpers/agustos_theme_helper"

class AdapterContractTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)

  def read(relative_path)
    File.read(File.join(ROOT, relative_path), encoding: "UTF-8")
  end

  def test_helper_exposes_v7_chrome_configuration
    helper = read("app/helpers/agustos_theme_helper.rb")
    %w[home_href nav more_label cta language_switch theme color_scheme shell screen search footer sidebar].each do |key|
      assert_includes helper, "#{key}:"
    end
    assert_includes helper, "theme: false"
    assert_includes helper, "path.start_with?"
    assert_includes helper, "NAV_LIMIT = 5"
    refute_match(/columns|DEFAULT_FOOTER_COLUMNS|footer_cta/, helper)
    refute_match(/BRAND_CHROME|chrome_for|brand_chrome/, helper, "brands no longer register chrome")
  end

  def harness
    Class.new do
      include AgustosThemeHelper
      attr_accessor :request
    end.new.tap { |h| h.request = Struct.new(:path).new("/blog/post") }
  end

  def test_helper_defaults_and_active_matching_execute
    harness = self.harness

    assert_equal :white, harness.agustos_theme_config[:substrate]
    assert_equal :light, harness.agustos_theme_config[:color_scheme]
    refute harness.agustos_theme_toggle?
    refute harness.agustos_dark?
    refute harness.agustos_product_shell?
    assert_nil harness.agustos_screen, "a marketing page names its own screen; the checker reports one that does not"
    assert_equal "", harness.agustos_body_controller
    assert_includes harness.agustos_body_class, "agustos-layout"
    refute_includes harness.agustos_body_class, "site-sidebar-layout"
    assert_equal %w[Home About Writing Typography], harness.agustos_nav_items.map { |item| item[:label] }
    assert_equal "Start a project", harness.agustos_value(harness.agustos_header_cta, :label)
    refute_respond_to harness, :agustos_footer_cta
    assert harness.agustos_footer_note.include?("©")
    assert harness.agustos_footer_links.any?
    assert harness.agustos_nav_active?("/blog")
    refute harness.agustos_nav_active?("/about")
    refute harness.agustos_nav_active?("/")
    refute harness.agustos_nav_active?("#top")
    assert_equal "Daha fazla", harness.agustos_more_label
    assert_equal "Alt menü", harness.agustos_footer_aria_label

    harness.agustos_theme(cta: nil, language_switch: { "code" => "TR", "href" => "/tr" })
    assert_nil harness.agustos_header_cta
    assert harness.agustos_header_utility?
    assert_equal "TR", harness.agustos_value(harness.agustos_language_switch, :code)
    assert_equal "Ara", harness.agustos_search_labels[:submit]

    harness.agustos_theme(brand: :iesdesk, shell: :product, theme: true)
    assert harness.agustos_theme_toggle?
    refute harness.agustos_dark?
    assert harness.agustos_product_shell?
    assert_equal :iesdesk, harness.agustos_theme_config[:brand]
    assert_includes harness.agustos_body_class, "site-sidebar-layout"
    assert_includes harness.agustos_body_class, "brand-iesdesk"
    assert_equal "agustos-theme", harness.agustos_body_controller
    assert_equal "app-shell", harness.agustos_screen

    # Chrome follows the screen family, not the brand: a house brand with a
    # website gets the top menu.
    harness.agustos_theme(brand: :iesdesk, screen: :home)
    refute harness.agustos_product_shell?
    refute_includes harness.agustos_body_class, "site-sidebar-layout"

    harness.agustos_theme(screen: :static)
    assert_equal "static", harness.agustos_screen

    options = harness.agustos_link_html_options({ external: true, aria_label: "Source", hreflang: "tr" }, class_name: "link")
    assert_equal "_blank", options[:target]
    assert_equal "noopener noreferrer", options[:rel]
    assert_equal "tr", options[:hreflang]
    assert_equal({ label: "Source" }, options[:aria])

    current = harness.agustos_nav_link_options({ href: "/blog" }, class_name: "site-header__link")
    assert_equal "page", current[:aria][:current]
    forced = harness.agustos_nav_link_options({ href: "#validation", current: true }, class_name: "site-sidebar__link")
    assert_equal "page", forced[:aria][:current]
    assert_nil harness.agustos_nav_link_options({ href: "/about" }, class_name: "x")[:aria]
  end

  def test_nav_over_five_items_keeps_four_and_moves_the_rest_under_more
    harness = self.harness
    five = (1..5).map { |n| { label: "Item #{n}", href: "/i#{n}" } }
    harness.agustos_theme(nav: five)
    menu, more = harness.agustos_nav_split
    assert_equal 5, menu.size
    assert_empty more

    six = (1..7).map { |n| { label: "Item #{n}", href: "/i#{n}" } }
    harness.agustos_theme(nav: six, lang: :en)
    menu, more = harness.agustos_nav_split
    assert_equal ["Item 1", "Item 2", "Item 3", "Item 4"], menu.map { |item| item[:label] }
    assert_equal ["Item 5", "Item 6", "Item 7"], more.map { |item| item[:label] }
    assert_equal "More", harness.agustos_more_label
    assert_equal "Footer", harness.agustos_footer_aria_label

    harness.agustos_theme(nav: six, more_label: "Other")
    assert_equal "Other", harness.agustos_more_label
  end

  def test_layout_picks_chrome_by_screen_family
    layout = read("app/views/layouts/agustos.html.erb")
    assert_includes layout, 'render "agustos/shared/header"'
    assert_includes layout, 'render "agustos/shared/footer"'
    assert_includes layout, 'render "agustos/shared/sidebar"'
    assert_includes layout, "agustos_theme_toggle?"
    assert_includes layout, "agustos_product_shell?"
    assert_match(/<body\s+data-screen="<%= agustos_screen %>"/, layout, "data-screen must precede any ERB tag on <body>")
    product_branch, website_branch = layout.split("<% else %>", 2)
    assert_includes product_branch, "agustos/shared/sidebar"
    refute_includes product_branch, "agustos/shared/header"
    refute_includes website_branch, "sidebar", "websites never render the sidebar"
    refute_includes layout, "agustos/product"
    refute File.exist?(File.join(ROOT, "app/assets/stylesheets/agustos/product.css"))
    refute_includes read("app/assets/stylesheets/agustos/components.css"), "margin-left: 280px"
  end

  def test_header_renders_more_menu_and_footer_is_simple
    header = read("app/views/agustos/shared/_header.html.erb")
    footer = read("app/views/agustos/shared/_footer.html.erb")
    utility = read("app/views/agustos/shared/_header_utility.html.erb")
    assert_includes header, "agustos-button agustos-button--primary site-header__cta"
    assert_includes header, "agustos_header_utility?"
    assert_includes header, "agustos_nav_split"
    assert_includes header, '<details class="site-header__more">'
    assert_includes header, '<summary class="site-header__link"><%= agustos_more_label %></summary>'
    assert_includes header, '<div class="site-header__more-menu">'
    assert_includes header, 'class_name: "site-header__more-link"'
    assert_includes footer, '<footer class="site-footer">'
    assert_includes footer, '<div class="site-footer__inner site-frame">'
    assert_includes footer, '<div class="site-footer__brand">'
    assert_includes footer, '<p class="type-footnote"><%= agustos_footer_note %></p>'
    assert_includes footer, '<ul class="site-footer__links">'
    assert_includes footer, 'class_name: "site-footer__link"'
    refute_match(/site-footer__(cols|col|col-heading|list|cta)\b|agustos-button/, footer)
    assert_includes utility, "agustos_theme_toggle?"
    css = read("app/assets/stylesheets/agustos/components.css")
    refute_includes css, "agustos-lockup"
    refute_includes css, ".site-header {"
    refute_includes css, ".site-footer"
    refute_includes css, "agustos-cta-band"
    lockup = read("app/views/agustos/shared/_brand_lockup.html.erb")
    assert_includes lockup, "site-lockup"
    refute_includes lockup, "agustos-lockup"
  end

  def test_sidebar_uses_kit_classes_for_product_ui
    sidebar = read("app/views/agustos/shared/_sidebar.html.erb")
    %w[site-sidebar-bar site-sidebar-burger site-sidebar__nav site-sidebar__link site-sidebar__utility site-sidebar__note].each do |name|
      assert_includes sidebar, name
    end
    assert_includes sidebar, 'id="site-sidebar" class="site-sidebar" popover'
    assert_includes sidebar, 'popovertarget="site-sidebar"'
    assert_includes sidebar, "agustos-theme#toggle"
  end

  def test_search_is_turbo_frame_and_server_partial_driven
    search = read("app/views/agustos/shared/_header_search.html.erb")
    results = read("app/views/agustos/shared/_search_results.html.erb")
    assert_includes search, "turbo_frame_tag"
    assert_includes search, "method: :get"
    header = read("app/views/agustos/shared/_header.html.erb")
    assert_includes header, "<noscript>"
    assert_includes header, "local: true"
    %w[frame_id query status groups].each { |local| assert_includes results, local }
    refute_match(/fetch\(|XMLHttpRequest|ActionCable/, read("app/javascript/controllers/agustos_search_controller.js"))
  end

  def test_stimulus_search_cleans_up_its_timer
    controller = read("app/javascript/controllers/agustos_search_controller.js")
    assert_match(/disconnect\(\).*window\.clearTimeout/m, controller)
    assert_includes controller, "default: 2"
    assert_includes controller, "default: 180"
    assert_match(/query\.length < this\.thresholdValue.*this\.close\(\)/m, controller)
    assert_includes controller, 'event.key === "ArrowDown"'
    assert_includes controller, 'event.key === "Enter"'
    assert_includes controller, 'event.key === "Escape"'
    theme = read("app/javascript/controllers/agustos_theme_controller.js")
    assert_includes theme, 'setAttribute("data-theme", "dark")'
    assert_includes theme, "aria-pressed"
    refute_includes theme, "pq-theme"
  end

  def test_responsive_contract_matches_kit_breakpoint_and_ios_safe_input
    css = read("app/assets/stylesheets/agustos/components.css")
    refute_includes css, "1366"
    assert_includes css, "@media (max-width: 1023px)"
    assert_includes css, "@media (max-width: 480px)"
    assert_match(/search--responsive .*input \{ font-size: 16px; \}/, css)
    assert_includes css, "outline: 2px solid var(--signal)"
  end

  def test_marketing_example_follows_locked_composition
    [read("app/views/agustos/examples/show.html.erb"), read("preview/marketing.html")].each do |page|
      assert_includes page, "hero-trust"
      assert_includes page, '<div class="hero-actions">'
      assert_includes page, "agustos-button agustos-button--primary"
      assert_includes page, "agustos-button agustos-button--secondary"
      assert_equal 1, page.scan('<mark class="type-highlight">').size, "one highlighter per page"
      assert_includes page, "band band--cream"
      assert_includes page, "Start a project"
      refute_match(/hero-links?\b|hero-link--|hero-action\b|hero-action--|agustos-cta-band|site-sidebar/, page)
      refute_match(/type-blockquote|type-pullquote/, page)
    end
    preview = read("preview/marketing.html")
    assert_includes preview, '<details class="site-header__more">'
    assert_includes preview, '<ul class="site-footer__links">'
    refute_match(/site-footer__(cols|col|col-heading|list|cta)\b/, preview)
  end

  def test_product_ui_example_uses_the_kit_sidebar
    page = read("app/views/agustos/examples/product.html.erb")
    preview = read("preview/product-ui.html")
    assert_includes page, "shell: :product"
    assert_includes page, "theme: true"
    assert_includes page, "brand: :iesdesk"
    assert_includes page, "sidebar: {"
    assert_includes page, "Validation run"
    assert_includes page, "Export dataset"
    assert_includes page, "Local cache"
    refute_match(/pq-|type-blockquote|type-pullquote/, page)
    assert_includes preview, "brand-iesdesk paper-white site-sidebar-layout"
    assert_includes preview, 'data-screen="app-shell"'
    assert_includes preview, "site-sidebar__nav"
    assert_includes preview, "Validation run"
    refute_includes preview, 'data-theme="dark"'
    refute_includes preview, "pq-"
    refute_includes preview, "site-header"
  end

  def test_all_erb_templates_parse
    Dir[File.join(ROOT, "app/views/**/*.erb")].each do |path|
      source = File.read(path, encoding: "UTF-8")
      template = ERB.new(source)
      RubyVM::InstructionSequence.compile("def render_template; #{template.src}; end") unless source.match?(/<%=.*\bdo\b/m)
    rescue SyntaxError => error
      flunk "#{path} does not parse: #{error.message}"
    end
  end
end
