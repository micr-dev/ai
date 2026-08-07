---
name: data-visualization
description: Choose and create truthful, distinctive data visualizations instead of defaulting to bar charts. Use when analyzing a dataset, selecting a chart or diagram, designing dashboards, building interactive visualizations, creating infographics, or explaining trends, distributions, relationships, flows, rankings, spatial patterns, or uncertainty.
---

# Data Visualization

Choose the visual form from the question and data structure. Do not default to bars, pie charts, or radial charts because they are familiar.

## Core rule

Start with the viewer's question:

- **Compare values**: Which is larger, and by how much?
- **Show change**: How did values move over time or between conditions?
- **Show distribution**: How are observations spread, clustered, or skewed?
- **Show relationships**: Which variables move together or which entities connect?
- **Show composition**: What parts make up a whole, and how does that change?
- **Show flow**: How do things move between stages, places, or categories?
- **Show rank**: How do positions change?
- **Show location**: Where does something happen?
- **Show uncertainty**: How reliable, variable, or incomplete is the estimate?
- **Tell a process**: What happens first, next, and why?

State the chosen question and the visual encoding before implementation.

## Workflow

1. **Inspect the data**
   - Identify row meaning, entity keys, measures, dimensions, time fields, geography, categories, missing values, and uncertainty.
   - Check units, denominators, aggregation level, outliers, and whether values are comparable.
   - Use a small exploratory analysis or notebook when the data is unfamiliar.

2. **Define the task**
   - Write one sentence: "The viewer needs to understand X about Y."
   - Pick the primary task: compare, change, distribution, relationship, composition, flow, rank, location, uncertainty, or process.
   - Identify the audience and the decision the visualization should support.

3. **Select candidates**
   - Choose 2-4 plausible forms from the decision guide below.
   - Prefer the simplest form that exposes the intended pattern.
   - Use a distinctive form only when it improves the question being answered, not as decoration.

4. **Test the choice**
   - Sketch or render a rough version.
   - Check whether the intended pattern is visible without a legend hunt.
   - Compare it against a boring baseline when the choice is debatable.
   - Reject forms that hide scale, overplot points, imply false precision, or require excessive interaction.

5. **Build the final artifact**
   - Use a suitable tool: notebook for analysis, a conventional chart library for precise static charts, p5.js/SVG for custom interactive work, infographic layouts for designed summaries, or animation when movement is itself meaningful.
   - Preserve the raw data and document transformations.
   - Add direct labels, units, source, time range, and a short takeaway.

6. **Verify**
   - Check values against the source data.
   - Check axes, sort order, color meaning, missing values, and responsive behavior.
   - Test grayscale or low-saturation viewing when color carries meaning.
   - Test keyboard access and a text alternative for interactive output.
   - Report the chosen form, rejected alternatives, and the reason for the decision.

## Decision guide

### Comparison

- Few categories, exact magnitude: dot plot or lollipop chart.
- Many categories: sorted dot plot, interval plot, or horizontal bars.
- Before versus after: slopegraph or dumbbell plot.
- Several groups across the same measures: small multiples or a connected dot plot.
- Values with confidence intervals: interval plot or forest plot.
- Use bars when a zero baseline and magnitude comparison are central.

### Change over time

- Continuous trend: line chart with meaningful annotations.
- Many series: small multiples, horizon chart, or indexed line chart.
- Rank changes: bump chart.
- Change between two points: slopegraph.
- Cumulative contribution: stacked area or streamgraph, only when total and composition both matter.
- Periodic intensity: calendar heatmap or radial calendar.
- Event sequence: annotated timeline.
- Use animation only when temporal transition helps comprehension and a static fallback exists.

### Distribution

- Small sample with individual observations: beeswarm or strip plot.
- Several distributions: ridgeline, violin, boxen, or small-multiple density plots.
- Distribution over time: ridgeline, calendar heatmap, or animated density.
- Skew and outliers: box plot plus raw points or a log-scale distribution view.
- Avoid hiding the observations behind a single summary mark when sample size and spread matter.

### Relationships

- Two numeric variables: scatterplot with trend, marginal distributions, and outlier annotation.
- Relationship changes over time: connected scatterplot or small multiples.
- Many variables: correlation matrix, parallel coordinates, or carefully selected small multiples.
- Entities connected to one another: network graph, adjacency matrix, or chord diagram.
- Prefer an adjacency matrix when a network becomes dense or labels must remain readable.

### Composition and hierarchy

- Parts of a whole at one point: 100% stacked bar or treemap when spatial packing helps.
- Composition across time: stacked area, stacked bars, or small multiples.
- Nested hierarchy: treemap, sunburst, icicle, or indented tree.
- Overlap between a few sets: Venn or Euler diagram.
- Do not use pie or donut charts for many slices or close values.

### Flow and movement

- Stage-to-stage quantities: Sankey or alluvial diagram.
- Spatial movement: flow map, origin-destination matrix, or animated path map.
- Routes through a process: directed graph or process map.
- Use proportional links only when widths remain comparable and readable.

### Rank and prioritization

- Ordered list: sorted dot plot or bar chart.
- Rank over time: bump chart.
- Multi-criteria prioritization: scatterplot with quadrants, comparison matrix, or slopegraph.
- Use a Pareto chart only when cumulative threshold decisions matter.

### Space and location

- Geographic rate or intensity: choropleth with a valid denominator.
- Geographic counts: proportional symbols or dot density, not an unnormalized choropleth.
- Routes and proximity: map, flow map, or Voronoi-style partition.
- Non-geographic spatial relationships: matrix, network, or custom spatial layout.

### Uncertainty

- Estimate plus interval: dot-and-whisker or forest plot.
- Probability over outcomes: fan chart, interval bands, or discrete outcome dots.
- Measurement variability: raw points plus summary and interval.
- Missingness: explicit missing-data encoding; never silently convert missing to zero.

## Distinctiveness without gimmicks

Use one unusual technique only when it improves the message:

- Convert a dense time series into small multiples before adding animation.
- Use annotations and direct labels before adding interaction.
- Use a custom p5.js visualization for networks, particles, spatial fields, or high-dimensional exploration.
- Use an infographic layout for a narrative, taxonomy, process, or comparison rather than forcing the content into axes.
- Use animation to reveal causality, sequence, or transformation, not merely to make a static chart move.
- Use radial forms for cycles, direction, or periodicity, not because they look novel.

## Visual integrity

- Use a zero baseline when bar length encodes magnitude; otherwise make the scale explicit.
- Keep scales comparable across small multiples.
- Do not use 3D perspective, gradients, shadows, or decorative texture that changes perceived value.
- Reserve color for grouping, emphasis, or a meaningful numeric scale.
- Use colorblind-safe palettes and a non-color distinction when categories matter.
- Sort categories by the question, not alphabetically by habit.
- Label the data directly where practical.
- Show denominators, units, and normalization choices.
- Annotate important events, thresholds, and outliers.
- Keep grid lines quiet and data marks prominent.
- Include a source and date for external data.

## Tool selection

- **Python/Jupyter**: inspect, clean, aggregate, compare candidate encodings, and validate values.
- **Standard chart libraries**: produce precise static charts when the visual form is conventional and the data is the focus.
- **p5.js**: create custom interactive, generative, animated, spatial, network, or high-dimensional visualizations.
- **SVG/HTML**: create responsive diagrams, annotated visual summaries, and publication-ready standalone artifacts.
- **Infographic workflows**: use for narrative summaries, taxonomies, timelines, process maps, and multi-panel explanations.
- **Manim or another animation tool**: use for data stories where the transition or derivation is central.

## Output contract

For every non-trivial visualization, provide:

1. The viewer question.
2. The data fields and transformations used.
3. The selected visual form and why it fits.
4. At least one plausible alternative and why it was rejected.
5. The final artifact or a runnable source file.
6. Verification results, including any limitations or unresolved ambiguity.

If the data is insufficient for a trustworthy visual, say what is missing and do not manufacture precision.
