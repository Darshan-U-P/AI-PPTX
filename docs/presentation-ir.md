# Presentation IR v1

Presentation IR is the canonical source of truth. A presentation contains metadata, inch-based dimensions, a tokenized theme, separate asset records, ordered slides, and a positive version number. Slides contain a stable UUID, layout/background metadata, elements, and speaker notes.

Supported v1 elements are `text`, `image`, `shape`, `line`, and `group`. Every element has a stable UUID and absolute geometry (`x`, `y`, `width`, `height`) in inches. Pydantic validates the server boundary and the JSON Schema provides an interoperable contract. The schema is designed for later chart, table, diagram, media, and embed extensions.

