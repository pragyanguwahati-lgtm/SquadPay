# UI/UX Design Specification (`design.md`)

## 1. Design Philosophy & Entry Point
The application starts with a slick, high-performance HTML landing page serving as the main entry point. The visual theme is "CO-OP FINANCE / PLAYER ONE READY," blending a dark, cyberpunk-inspired gaming aesthetic with clean fintech interfaces. 

To achieve the requested "slick" feel, the frontend architecture will leverage high-performance animation and rendering libraries:
- **liquidGL:** For fluid, WebGL-powered background gradients and interactive particle effects.
- **unlumen ui & smooth ui:** For accessible, heavily styled, and glassmorphic UI components.
- **animaster lib:** For orchestrating scroll-triggered reveals and timeline animations between the "Assemble", "Analyze", and "Settle Up" levels.

## 2. Typography
The typographic hierarchy relies on a stark contrast between futuristic display fonts and highly legible sans-serif utility fonts:
- **Display / Headers:** Orbitron (Weights: 700, 800, 900). Used for main titles, branding ("SQUADPAY"), and heavy numerical values.
- **Body / UI Elements:** Inter (Weights: 400 to 900). Used for terminal outputs, descriptive text, and data tables.

## 3. Core Color Palette
The interface utilizes a deep, dark-mode foundation accented by vibrant, game-ready neon highlights:
- **Backgrounds:** Deep navy and dark teal tones (`#11264b`, `#071b1a`, `#102e2a`, `#0c2423`).
- **Primary Accent:** Mint green / Cyan (`#48d5a5`).
- **Secondary Accent:** Electric Blue (`#0866ed`).
- **Text & Highlights:** Bright mint text backgrounds (`#effbf5`) and off-white/grey text (`#F1F5FF`, `#99A8C4`).

## 4. UI Components & Data Visualization
The main website guides the user through three distinct "Levels", utilizing specific visual motifs for each:

*   **Level 01: Assemble:** Features player roster cards with unique identity colors.
    *   Nova (The Grinder): Blue (`#236BE2`).
    *   Ghost (Night Owl): Purple (`#7760CC`).
    *   Pixel (The Builder): Orange (`#B86A31`).
    *   Moss (Sunday Main): Green (`#348765`).
*   **Level 02: Analyze:** Replicates a terminal or CLI environment (`$ squadpay analyze october.log`) overlaying fluid data visualizations (like progress bars showing 48 hrs / 40%). 
*   **Level 03: Settle Up:** Transitions to a fintech dashboard displaying the final PayPal API allocations (e.g., Nova: $24, Ghost: $18, Pixel: $12, Moss: $6 from a $60 server).

## 5. Animation & Interaction
- **Backgrounds:** Radial and linear gradients (e.g., `radial-gradient(50% 50% at 75% 35%,#155844 0%,#0a302b 38%,#071b1a 78%)`) will be animated continuously using liquidGL.
- **Scroll Triggers:** Cards will translate along the Y-axis and rotate slightly into place (e.g., `transform:translateY(40px) rotate(2deg)`) using animaster lib as the user scrolls through the levels.