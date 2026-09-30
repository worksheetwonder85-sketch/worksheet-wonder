# Worksheet Wonder: Dependency Graph

This graph illustrates how the decoupled publishing platform currently operates.

```mermaid
graph TD
    subgraph Data Layer
        A[04_Content_Database] -->|JSON Payloads| B[05_JSON_Schemas]
        B -->|Validates| A
    end

    subgraph Asset Layer
        C[03_Illustration_Library] -->|SVG/Metadata| A
    end

    subgraph Presentation Layer
        D[06_HTML_Framework] -->|Requires| A
        D -->|Requires| C
        E[07_CSS_Framework] -->|Styles| D
    end

    subgraph Output Engine (Missing)
        F[Template Compiler e.g., Handlebars] -->|Ingests| A
        F -->|Ingests| D
        G[PDF Generator e.g., Puppeteer] -->|Renders| F
        G -->|Applies| E
    end
```

### Dependency Flow Analysis
1.  **Content Database** is entirely dependent on the **JSON Schemas** for structural integrity.
2.  **HTML Framework** is dependent on the exact key names generated in the **Content Database**.
3.  **HTML Framework** relies on the grid physics enforced by the **CSS Framework**.
4.  The entire pipeline is currently halted because the **Output Engine** and **JSON Schemas** are missing from the workflow.
