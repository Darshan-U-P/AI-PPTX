export type Element = { id: string; type: "text" | "image" | "shape" | "line" | "group"; x: number; y: number; width: number; height: number; z_index: number; [key: string]: unknown };
export type Slide = { id: string; layout: string; background: string; elements: Element[]; speaker_notes: string };
export type Presentation = { id: string; metadata: { title: string; description: string }; dimensions: { width: number; height: number; unit: "in" }; theme: { colors: { background: string; foreground: string; primary: string; secondary: string } }; slides: Slide[]; version: number };

