---
name: Agro-Intelligence Oversight
colors:
  surface: '#0f150f'
  surface-dim: '#0f150f'
  surface-bright: '#343b34'
  surface-container-lowest: '#0a100a'
  surface-container-low: '#171d17'
  surface-container: '#1b211b'
  surface-container-high: '#252c25'
  surface-container-highest: '#30362f'
  on-surface: '#dee4da'
  on-surface-variant: '#becabc'
  inverse-surface: '#dee4da'
  inverse-on-surface: '#2c322b'
  outline: '#889487'
  outline-variant: '#3f4a3f'
  surface-tint: '#76db8f'
  primary: '#76db8f'
  on-primary: '#003918'
  primary-container: '#3da35d'
  on-primary-container: '#003114'
  inverse-primary: '#006d33'
  secondary: '#9dd3a7'
  on-secondary: '#01391a'
  secondary-container: '#205331'
  on-secondary-container: '#8fc599'
  tertiary: '#89ceff'
  on-tertiary: '#00344d'
  tertiary-container: '#009ada'
  on-tertiary-container: '#002d43'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#92f8a9'
  primary-fixed-dim: '#76db8f'
  on-primary-fixed: '#00210b'
  on-primary-fixed-variant: '#005225'
  secondary-fixed: '#b8f0c2'
  secondary-fixed-dim: '#9dd3a7'
  on-secondary-fixed: '#00210c'
  on-secondary-fixed-variant: '#1e502e'
  tertiary-fixed: '#c9e6ff'
  tertiary-fixed-dim: '#89ceff'
  on-tertiary-fixed: '#001e2f'
  on-tertiary-fixed-variant: '#004c6e'
  background: '#0f150f'
  on-background: '#dee4da'
  surface-variant: '#30362f'
typography:
  display-lg:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: monospace
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  container-padding: 24px
  gutter: 16px
  card-gap: 20px
---

## Brand & Style
This design system is engineered for the high-stakes environment of Peruvian agro-export auditing. The brand personality is **clinical, vigilant, and technologically advanced**. It moves away from traditional agricultural aesthetics toward a "precision-tech" narrative, positioning the auditor as a pilot of complex data streams.

The visual style employs a **Dark-Glassmorphism** approach. By using a deep charcoal-green base and translucent overlays, the interface reduces pupillary fatigue during long supervision shifts. The aesthetic prioritizes data legibility and optical hierarchy, ensuring that high-severity alerts are immediately distinguishable from the systematic flow of industrial telemetry.

## Colors
The palette is rooted in the **Deep Forest (#0c120c)** background to provide a high-contrast foundation for data visualization. 

- **Primary Emerald:** Used exclusively for interactive elements, active states, and "Healthy/Optimal" status indicators.
- **Surface Colors:** Instead of flat grays, surfaces use semi-transparent variants of the primary color to create a sense of depth and environmental harmony.
- **Audit Semantics:** The high-severity red (#d9534f) and suspicious ochre (#f0ad4e) are tuned to be legible against dark backgrounds without causing vibrance blooming, ensuring auditors can differentiate between a critical crop failure and a sensor calibration warning.

## Typography
The system uses a dual-font strategy. **Outfit** is utilized for headlines and primary KPI values to provide a modern, geometric technical feel. **Inter** is used for all functional UI, tables, and long-form data reading due to its exceptional legibility at small sizes.

For data-heavy audit tables, use the `mono-data` role to ensure that numerical values align vertically, facilitating rapid visual comparison of export metrics. All labels should be uppercase with slight letter-spacing to distinguish them from user-generated content.

## Layout & Spacing
The layout follows a **12-column fluid grid** for desktop, optimized for high-density information displays. On the main dashboard, the layout utilizes a "Sidebar-Control" model where navigation is collapsed to icons to maximize the workspace for tables and charts.

- **Data Density:** Use a compact spacing scale (4px increments) to allow for the high volume of parameters required in agro-industrial monitoring.
- **Safe Areas:** Maintain a minimum 24px outer margin on all containers to prevent the UI from feeling claustrophobic.
- **Reflow:** On mobile devices, 12-column grids collapse into a single vertical stack, with horizontal scrolling enabled specifically for data tables to maintain column integrity.

## Elevation & Depth
Depth is communicated through **Glassmorphism and Tonal Layering** rather than traditional drop shadows.

1.  **Level 0 (Background):** Solid #0c120c.
2.  **Level 1 (Cards/Containers):** Background hex `#ffffff` at 4-6% opacity with a `20px` backdrop blur. A `1px` inner border (stroke) using `#ffffff` at 10% opacity creates a "glass edge" effect.
3.  **Level 2 (Modals/Popovers):** Background hex `#ffffff` at 10% opacity, `40px` backdrop blur, and a subtle emerald-tinted outer glow (`#3da35d` at 15% opacity, 30px blur) to indicate focus.

This hierarchy ensures that secondary information stays in the background while active alerts "float" closer to the user.

## Shapes
The shape language is **Soft (0.25rem - 0.75rem)**. This provides a professional, "machined" look that feels more technical and precise than fully rounded pill shapes. 

- **Primary Buttons & Inputs:** 4px (0.25rem) radius for a sharp, industrial feel.
- **Data Cards:** 8px (0.5rem) radius to soften the high-density grid.
- **Status Indicators:** Small 2px radius or circles for categorical dots.
- **Interactive Visualization Nodes:** Use 4px radius to maintain consistency with the input fields.

## Components
- **Audit Tables:** Use zebra-striping with `#ffffff` at 2% opacity. The header row should be semi-transparent with a persistent bottom border in Primary Emerald. 
- **KPI Cards:** Feature a prominent display value in `display-lg` (Outfit), with a small sparkline chart integrated into the background of the glass container.
- **Glass Buttons:** Primary buttons use a solid Emerald fill. Secondary buttons use a glass background with an Emerald border. Use a "glow" micro-interaction on hover.
- **Sophisticated Inputs:** Fields should have no background fill until focused. On focus, the glass background intensifies and the border glows Emerald.
- **Anomaly Badges:** High-severity anomalies should utilize a "pulsing" animation on the border to draw immediate attention without obstructing the data text.
- **Data Visualization:** Line charts should use 2px stroke widths with area fills using gradients from the semantic color to transparent.