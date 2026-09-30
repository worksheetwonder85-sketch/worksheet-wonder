# Master Print Guide

## CSS Print Rules
```css
@page { size: A4 portrait; margin: 0; }
body { -webkit-print-color-adjust: exact; color-adjust: exact; }
@media print { .print-btn { display: none !important; } }
```

## Universal Print Compatibility
- Designed for 100% scale print on A4 paper and US Letter without clipping.
- High contrast borders (#2C3E50) ensure legibility even on low-cost black & white thermal/laser printers.
