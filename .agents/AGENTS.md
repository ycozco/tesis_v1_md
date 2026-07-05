# Project Rules & Design System Enforcement

All user interface development in this repository must adhere strictly to the visual style guidelines, layout constraints, and design tokens defined in [DESIGN.md](file:///d:/tesis_yoset/DESIGN.md).

## Rules for Coding Agents
1. **Review Design Tokens First:** Always read [DESIGN.md](file:///d:/tesis_yoset/DESIGN.md) before writing or editing frontend files to use the correct color classes, border radii, and spacing tokens.
2. **Prevent Layout Overlaps:** Always close all JSX tag containers properly. Do not leave any unclosed container tags (like layout columns or banners) as they break the responsive grid alignment.
3. **Maintain Visual Consistency:** Always use glassmorphism utilities (`.glass-card`, `.glass-panel`, `.glass-modal`, `.glass-input`) for content panels instead of solid block background colors.
