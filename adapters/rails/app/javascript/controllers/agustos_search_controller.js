import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["form", "input", "panel", "toggle"]
  static values = { threshold: { type: Number, default: 2 }, delay: { type: Number, default: 180 } }

  disconnect() {
    window.clearTimeout(this.timer)
  }

  toggle() {
    this.panelTarget.hidden ? this.open(true) : this.close()
  }

  focus() {
    if (this.inputTarget.value.trim().length >= this.thresholdValue) this.open(false)
  }

  queue() {
    window.clearTimeout(this.timer)
    const query = this.inputTarget.value.trim()

    if (query.length < this.thresholdValue) {
      this.close()
      return
    }

    this.open(false)
    this.timer = window.setTimeout(() => this.formTarget.requestSubmit(), this.delayValue)
  }

  navigate(event) {
    const links = Array.from(this.element.querySelectorAll(".agustos-header__search-result a"))
    const activeIndex = links.indexOf(document.activeElement)

    if (event.key === "Escape") {
      event.preventDefault()
      this.close()
      if (this.hasToggleTarget) this.toggleTarget.focus()
      else this.inputTarget.focus()
      return
    }

    if (document.activeElement === this.inputTarget) {
      if (event.key === "ArrowDown" && links.length > 0) {
        event.preventDefault()
        links[0].focus()
      } else if (event.key === "Enter" && links.length > 0) {
        event.preventDefault()
        links[0].click()
      }
      return
    }

    if (activeIndex >= 0 && event.key === "ArrowDown") {
      event.preventDefault()
      links[Math.min(activeIndex + 1, links.length - 1)].focus()
    } else if (activeIndex >= 0 && event.key === "ArrowUp") {
      event.preventDefault()
      if (activeIndex === 0) this.inputTarget.focus()
      else links[activeIndex - 1].focus()
    }
  }

  outside(event) {
    if (!this.element.contains(event.target)) this.close()
  }

  open(focusInput) {
    this.panelTarget.hidden = false
    if (this.hasToggleTarget) this.toggleTarget.setAttribute("aria-expanded", "true")
    this.inputTarget.setAttribute("aria-expanded", "true")
    if (focusInput) this.inputTarget.focus()
  }

  close() {
    this.panelTarget.hidden = true
    if (this.hasToggleTarget) this.toggleTarget.setAttribute("aria-expanded", "false")
    this.inputTarget.setAttribute("aria-expanded", "false")
  }
}
