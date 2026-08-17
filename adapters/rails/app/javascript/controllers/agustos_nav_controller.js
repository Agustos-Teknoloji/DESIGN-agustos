import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["panel", "toggle", "backdrop"]

  toggle() {
    this.setOpen(!this.element.hasAttribute("data-nav-open"))
  }

  close() {
    this.setOpen(false)
  }

  follow() {
    if (window.matchMedia("(max-width: 1023px), (max-width: 1366px) and (hover: none) and (pointer: coarse)").matches) {
      this.close()
    }
  }

  disconnect() {
    document.body.style.overflow = ""
  }

  setOpen(open) {
    this.element.toggleAttribute("data-nav-open", open)
    this.toggleTargets.forEach((button) => button.setAttribute("aria-expanded", String(open)))
    document.body.style.overflow = open ? "hidden" : ""
  }
}
