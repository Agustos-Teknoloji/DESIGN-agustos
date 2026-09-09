import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  toggle(event) {
    const root = document.documentElement
    const dark = root.getAttribute("data-theme") !== "dark"
    if (dark) root.setAttribute("data-theme", "dark")
    else root.removeAttribute("data-theme")

    const button = event?.currentTarget
    if (button?.classList?.contains("pq-theme")) {
      button.setAttribute("aria-pressed", String(dark))
      button.innerHTML = dark
        ? '<span aria-hidden="true">☾</span> Dark'
        : '<span aria-hidden="true">☀</span> Light'
    }

    try {
      localStorage.setItem("agustos:theme", dark ? "dark" : "light")
    } catch (_) {
      // Storage may be unavailable in private browsing contexts.
    }
  }
}
