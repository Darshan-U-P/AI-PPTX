export type ElementType = "text" | "image" | "shape" | "line" | "group";
export type Element = {
  id: string; type: ElementType; x: number; y: number; width: number; height: number;
  rotation: number; opacity: number; z_index: number; text?: string; font_size?: number;
  color?: string; fill?: string; stroke?: string; stroke_width?: number; shape_type?: "rectangle" | "rounded_rectangle" | "ellipse";
  source?: string; alt?: string;
};
export type Slide = { id: string; order: number; layout: string; background: string; elements: Element[]; speaker_notes: string };
export type Presentation = {
  id: string; metadata: { title: string; description: string }; dimensions: { width: number; height: number; unit: "in" };
  theme: { colors: { background: string; foreground: string; primary: string; secondary: string; accent: string } };
  assets: { id: string; source: string; alt: string }[]; slides: Slide[]; version: number;
};
export type Asset = { id: string; source: string; alt: string; media_type: string };
