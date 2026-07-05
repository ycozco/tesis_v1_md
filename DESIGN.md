---
name: Agro-Intelligence Design System
version: 1.0.0
colors:
  primary: "#76db8f"
  primary-container: "#3da35d"
  primary-fixed: "#92f8a9"
  secondary: "#9dd3a7"
  secondary-container: "#205331"
  tertiary: "#89ceff"
  tertiary-container: "#009ada"
  background: "#0f150f"
  surface: "#0f150f"
  surface-container: "#1b211b"
  surface-container-low: "#171d17"
  surface-container-lowest: "#0a100a"
  surface-variant: "#30362f"
  on-surface: "#dee4da"
  on-surface-variant: "#becabc"
  outline: "#889487"
  outline-variant: "#3f4a3f"
  error: "#ffb4ab"
  error-container: "#93000a"
  on-error-container: "#ffdad6"
typography:
  display-lg:
    fontFamily: Outfit, sans-serif
  headline-lg:
    fontFamily: Outfit, sans-serif
  headline-md:
    fontFamily: Outfit, sans-serif
  headline-sm:
    fontFamily: Outfit, sans-serif
  body-lg:
    fontFamily: Inter, sans-serif
  body-md:
    fontFamily: Inter, sans-serif
  body-sm:
    fontFamily: Inter, sans-serif
  label-md:
    fontFamily: Inter, sans-serif
  mono-data:
    fontFamily: monospace
spacing:
  unit: 4px
  gutter: 16px
  card-gap: 20px
  container-padding: 24px
borderRadius:
  default: 0.125rem
  lg: 0.25rem
  xl: 0.5rem
  full: 0.75rem
---

## Overview
The Agro-Intelligence Design System is designed specifically for dark-themed, data-heavy agricultural auditing and AI oversight dashboards. It features a forest-green color palette combined with high-contrast indicator highlights (cyan/blue for telemetry, orange/red for alerts) and clean glassmorphism patterns.

---

## Color System
* **Brand Colors (Greens):** 
  * `primary` (`#76db8f`) is the core accent brand green, used for branding, active states, and successful actions.
  * `secondary` (`#9dd3a7`) and `secondary-container` are used for secondary UI elements.
  * `background` (`#0f150f`) is a deep, dark forest green that serves as the root canvas.
* **Functional Highlight Colors:**
  * `tertiary` (`#89ceff`) is cyan-blue, used for AI models, logs, metrics, and SHAP data.
  * `error` (`#ffb4ab`) and `error-container` (`#93000a`) are reserved for critical risk scores, anomalous flags, and action warnings.

---

## Spacing & Grid System
* **`unit` (4px):** The base scale multiplier.
* **`gutter` (16px) / `card-gap` (20px):** Spacing between panels and cards.
* **`container-padding` (24px):** Padding applied to main layouts and view roots.

---

## Typography
* **Headings:** Use `Outfit` (sans-serif) for titles, section headers, and scores to give a premium, geometric vibe.
* **Body & Labels:** Use `Inter` (sans-serif) for body texts, form descriptions, buttons, and legends.
* **Telemetry & Logs:** Use `monospace` (System monospace) for RUC numbers, DAM codes, timestamp sequences, and pipeline logs.

---

## Component Specifications & Constraints

### 1. Glassmorphism Panels
Always use the following Tailwind-compatible style classes to render UI cards instead of flat backgrounds:
* `.glass-card`: `bg-white/5 backdrop-blur-[20px] border border-white/10`
* `.glass-panel`: `bg-white/3 backdrop-blur-[10px] border border-white/5`
* `.glass-modal`: `bg-[#0f190f]/85 backdrop-blur-[20px] border border-[#76db8f]/15`
* `.glass-input`: `bg-transparent border border-white/30` transitioning to `border-[#76db8f]` on focus.

### 2. Layout Grid Constraints (CRITICAL)
> [!IMPORTANT]
> **Always close container tags properly.** Never use unclosed layout tags (like missing `</div>` on main banners) as this breaks grid columns and squishes panels.
> Avoid nested absolute height limits inside responsive grids. Use dynamic spacing utilities (`gap-6`, `flex flex-col`) to allow charts and tables to expand without overlapping.
