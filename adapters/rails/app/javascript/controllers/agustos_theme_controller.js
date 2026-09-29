import { Controller } from "@hotwired/stimulus"

// Product UI only. Websites ship light and carry no theme control.
export default class extends Controller {
  connect() {
    this.sync(document.documentElement.getAttribute("data-theme") === "dark")
  }

  toggle() {
    const root = document.documentElement
    const dark = root.getAttribute("data-theme") !== "dark"
    if (dark) root.setAttribute("data-theme", "dark")
    else root.removeAttribute("data-theme")
    this.sync(dark)

    try {
      localStorage.setItem("agustos:theme", dark ? "dark" : "light")
    } catch (_) {
      // Storage may be unavailable in private browsing contexts.
    }
  }

  sync(dark) {
    this.element
      .querySelectorAll('[data-action~="agustos-theme#toggle"][aria-pressed]')
      .forEach((button) => button.setAttribute("aria-pressed", String(dark)))
  }
}
