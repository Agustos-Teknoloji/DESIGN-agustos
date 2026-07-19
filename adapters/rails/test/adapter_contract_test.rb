require "erb"
require "minitest/autorun"
require_relative "../app/helpers/agustos_theme_helper"

class AdapterContractTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)

  def read(relative_path)
    File.read(File.join(ROOT, relative_path))
  end

  def test_helper_exposes_v3_chrome_configuration
    helper = read("app/helpers/agustos_theme_helper.rb")
    %w[home_href nav cta language_switch theme search footer].each do |key|
      assert_includes helper, "#{key}:"
    end
    assert_includes helper, "path.start_with?"
  end

  def test_helper_defaults_and_active_matching_execute
    harness = Class.new do
      include AgustosThemeHelper
      attr_accessor :request
    end.new
    harness.request = Struct.new(:path).new("/blog/post")

    assert_equal :white, harness.agustos_theme_config[:substrate]
    assert_equal %w[Home About Writing Typography], harness.agustos_nav_items.map { |item| item[:label] }
    assert harness.agustos_nav_active?("/blog")
    refute harness.agustos_nav_active?("/about")
    refute harness.agustos_nav_active?("/")

    harness.agustos_theme(cta: nil, language_switch: { "code" => "TR", "href" => "/tr" })
    assert_nil harness.agustos_header_cta
    assert_equal "TR", harness.agustos_value(harness.agustos_language_switch, :code)
    assert_equal "Ara", harness.agustos_search_labels[:submit]

    options = harness.agustos_link_html_options({ external: true, aria_label: "Source" }, class_name: "link")
    assert_equal "_blank", options[:target]
    assert_equal "noopener noreferrer", options[:rel]
    assert_equal({ label: "Source" }, options[:aria])
  end

  def test_layout_uses_header_and_footer_without_sidebar_offset
    layout = read("app/views/layouts/agustos.html.erb")
    assert_includes layout, 'render "agustos/shared/header"'
    assert_includes layout, 'render "agustos/shared/footer"'
    refute_includes layout, "sidebar"
    refute_includes read("app/assets/stylesheets/agustos/components.css"), "margin-left: 280px"
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
    assert_includes read("app/javascript/controllers/agustos_theme_controller.js"), 'setAttribute("data-theme", "dark")'
  end

  def test_responsive_contract_includes_touch_tablets_and_ios_safe_input
    css = read("app/assets/stylesheets/agustos/components.css")
    assert_includes css, "(max-width: 1366px) and (hover: none) and (pointer: coarse)"
    assert_match(/search--responsive .*input \{ font-size: 16px; \}/, css)
    assert_includes css, "outline: 2px solid var(--signal)"
    assert_includes css, "@media (max-width: 760px)"
  end

  def test_all_erb_templates_parse
    Dir[File.join(ROOT, "app/views/**/*.erb")].each do |path|
      source = File.read(path)
      template = ERB.new(source)
      RubyVM::InstructionSequence.compile("def render_template; #{template.src}; end") unless source.match?(/<%=.*\bdo\b/m)
    rescue SyntaxError => error
      flunk "#{path} does not parse: #{error.message}"
    end
  end
end
