require "erb"
require "minitest/autorun"
require_relative "../app/helpers/agustos_theme_helper"

class AdapterContractTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)

  def read(relative_path)
    File.read(File.join(ROOT, relative_path), encoding: "UTF-8")
  end

  def test_helper_exposes_v5_chrome_configuration
    helper = read("app/helpers/agustos_theme_helper.rb")
    %w[home_href nav cta language_switch theme color_scheme shell search footer].each do |key|
      assert_includes helper, "#{key}:"
    end
    assert_includes helper, "theme: false"
    assert_includes helper, "path.start_with?"
  end

  def test_helper_defaults_and_active_matching_execute
    harness = Class.new do
      include AgustosThemeHelper
      attr_accessor :request
    end.new
    harness.request = Struct.new(:path).new("/blog/post")

    assert_equal :white, harness.agustos_theme_config[:substrate]
    assert_equal :light, harness.agustos_theme_config[:color_scheme]
    refute harness.agustos_theme_toggle?
    refute harness.agustos_dark?
    refute harness.agustos_product_shell?
    assert_equal "agustos-nav", harness.agustos_body_controller
    assert_equal %w[Home About Writing Typography], harness.agustos_nav_items.map { |item| item[:label] }
    assert_equal "Start a project", harness.agustos_value(harness.agustos_header_cta, :label)
    assert_equal "Contact", harness.agustos_value(harness.agustos_footer_cta, :label)
    assert harness.agustos_nav_active?("/blog")
    refute harness.agustos_nav_active?("/about")
    refute harness.agustos_nav_active?("/")

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
    assert_includes harness.agustos_body_class, "pq"
    assert_equal "agustos-theme", harness.agustos_body_controller

    options = harness.agustos_link_html_options({ external: true, aria_label: "Source" }, class_name: "link")
    assert_equal "_blank", options[:target]
    assert_equal "noopener noreferrer", options[:rel]
    assert_equal({ label: "Source" }, options[:aria])
  end

  def test_layout_uses_header_and_footer_without_sidebar_offset
    layout = read("app/views/layouts/agustos.html.erb")
    assert_includes layout, 'render "agustos/shared/header"'
    assert_includes layout, 'render "agustos/shared/footer"'
    assert_includes layout, "agustos_theme_toggle?"
    assert_includes layout, "agustos_product_shell?"
    refute_includes layout, "sidebar"
    refute_includes read("app/assets/stylesheets/agustos/components.css"), "margin-left: 280px"
  end

  def test_header_and_footer_use_kit_buttons
    header = read("app/views/agustos/shared/_header.html.erb")
    footer = read("app/views/agustos/shared/_footer.html.erb")
    utility = read("app/views/agustos/shared/_header_utility.html.erb")
    assert_includes header, "agustos-button agustos-button--primary agustos-header__cta"
    assert_includes header, "agustos_header_utility?"
    assert_includes footer, "agustos-button agustos-button--primary agustos-footer__cta"
    assert_includes utility, "agustos_theme_toggle?"
    css = read("app/assets/stylesheets/agustos/components.css")
    assert_includes css, "var(--footer-paper)"
    assert_includes css, "var(--lockup-color, var(--brand))"
    assert_includes css, 'html[data-theme="dark"] .agustos-header'
    assert_includes css, 'html[data-theme="dark"] .agustos-footer .agustos-button--primary'
    refute_match(/\.agustos-header__cta \{[^}]*background: var\(--ink\)/, css)
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
    assert_includes theme, "pq-theme"
  end

  def test_responsive_contract_includes_touch_tablets_and_ios_safe_input
    css = read("app/assets/stylesheets/agustos/components.css")
    assert_includes css, "(max-width: 1366px) and (hover: none) and (pointer: coarse)"
    assert_includes css, "@media (max-width: 1023px)"
    assert_includes css, "@media (max-width: 480px)"
    assert_match(/search--responsive .*input \{ font-size: 16px; \}/, css)
    assert_includes css, "outline: 2px solid var(--signal)"
  end

  def test_marketing_example_follows_locked_composition
    page = read("app/views/agustos/examples/show.html.erb")
    assert_includes page, "hero-trust"
    assert_includes page, "agustos-cta-band"
    assert_includes page, "Start a project"
    refute_match(/type-blockquote|type-pullquote/, page)
  end

  def test_product_ui_example_ports_iesdesk_validation_run
    page = read("app/views/agustos/examples/product.html.erb")
    preview = read("preview/product-ui.html")
    css = read("app/assets/stylesheets/agustos/product.css")
    assert_includes page, "shell: :product"
    assert_includes page, "theme: true"
    assert_includes page, "brand: :iesdesk"
    assert_includes page, "pq-side"
    assert_includes page, "Validation run"
    assert_includes page, "Export dataset"
    assert_includes page, "Local cache"
    refute_match(/type-blockquote|type-pullquote/, page)
    assert_includes preview, "brand-iesdesk"
    assert_includes preview, "Validation run"
    assert_includes preview, "pq-stat--featured"
    refute_includes preview, 'data-theme="dark"'
    assert_includes css, ".pq-side"
    refute_includes css, "999px"
    refute_includes css, "agustos-header"
    assert_includes css, 'html[data-theme="dark"] .pq-file code'
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
