name: benchmark-or-eval-graph
description: Use when user wants any graph from local or remote data using a scripted workflow, including bars, lines, scatters, and faceted layouts.
disable-model-invocation: true
---

Build, run, and export requested graphs from user-provided data and instructions.

## Branch

- Use when the user gives a graph type and input data source.
- Use when the user asks for reproducible re-runs as source data changes.

## In-skill Steps

1. Resolve intent and constraints

- Extract graph intent:
  - chart type (bar, line, scatter, histogram, heatmap, or faceted layout)
  - grouping and faceting rules
  - formatting preferences (labels, fonts, logos, colors, legends, axis style)
- Confirm output requirements:
  - one or more files, and file formats (`png`, `svg`, `pdf`)
  - image size, DPI, and optional tight bounding box
- Define source:
  - local CSV path, or
  - published Google Sheet export URL

Completion criterion:
- User request is mapped to a concrete graph specification and output contract.

2. Prepare data source

- Load the source with pandas.
- Validate required columns for the requested graph.
- Normalize types:
  - numeric columns as numbers
  - categories as strings
- Keep deterministic ordering (sort by benchmark/model/date if available).

Completion criterion:
- Data loads without errors and matches the required schema for the requested graph.

3. Construct the figure

- Create the figure and axes for the requested layout:
  - single axis or grid/axes array for faceting
- Draw the chart using the requested matplotlib path:
  - bar plot
  - line plot
  - scatter
  - histogram
  - heatmap
  - custom composition if requested
- Apply consistent styling:
  - axis labels and tick labels
  - title text per panel
  - color mapping and legend
  - grid settings
- If a logo is requested and provided, overlay it after bars/markers.

Completion criterion:
- All requested panels render and follow the requested style and data mapping.

4. Export outputs and validate existence

- Save every requested file with explicit parameters:
  - PNG: configured `dpi`
  - SVG/PDF/vector outputs if requested
- Verify each target file exists and is non-zero bytes.

Completion criterion:
- All declared output files are generated and non-empty.

5. Optional publish step

- If upload is requested, send the selected file(s) to the chosen host and return returned URLs.
- If no host is provided, stop after local artifact creation.

Completion criterion:
- User receives upload URLs or a clear local-path-only result.

## In-skill Reference

- Required packages: `pandas`, `matplotlib`, `numpy`.
- Keep runs deterministic:
  - fixed sort order
  - fixed figure size and scale
  - fixed color and marker choices unless user changes them
- Axis scale strategy:
  - shared scale for direct cross-panel comparison
  - per-axis scale for local readability
- If input data and request mismatch, ask one concise clarification and do not guess defaults that change semantics.
