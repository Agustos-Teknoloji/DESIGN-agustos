import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  toggle() {
    const root = document.documentElement
    const dark = root.getAttribute("data-theme") !== "dark"
    if (dark) root.setAttribute("data-theme", "dark")
    else root.removeAttribute("data-theme")

    try {
      localStorage.setItem("agustos:theme", dark ? "dark" : "light")
    } catch (_) {
      // Storage may be unavailable in private browsing contexts.
    }
  }
}
