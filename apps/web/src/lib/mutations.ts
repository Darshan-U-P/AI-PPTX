import type { Element, Slide } from "@/types/presentation";

export const createTextElement = (): Element => ({ id: crypto.randomUUID(), type: "text", x: 1, y: 1, width: 5, height: 0.7, rotation: 0, opacity: 1, z_index: 0, text: "Edit this text", font_size: 24, color: "#172033" });
export const createShapeElement = (): Element => ({ id: crypto.randomUUID(), type: "shape", x: 1, y: 2, width: 3, height: 1.25, rotation: 0, opacity: 1, z_index: 0, shape_type: "rounded_rectangle", fill: "#4F46E5", stroke: "#4F46E5", stroke_width: 0 });
export const createImageElement = (source: string, alt: string): Element => ({ id: crypto.randomUUID(), type: "image", x: 6, y: 1, width: 3, height: 2, rotation: 0, opacity: 1, z_index: 0, source, alt });
export const createElement = (slide: Slide, element: Element): Slide => ({ ...slide, elements: [...slide.elements, { ...element, z_index: slide.elements.length }] });
export const updateElement = (slide: Slide, id: string, patch: Partial<Element>): Slide => ({ ...slide, elements: slide.elements.map((item) => item.id === id ? { ...item, ...patch } : item) });
export const deleteElement = (slide: Slide, id: string): Slide => ({ ...slide, elements: slide.elements.filter((item) => item.id !== id) });
export const moveElement = (slide: Slide, id: string, x: number, y: number): Slide => updateElement(slide, id, { x, y });
export const resizeElement = (slide: Slide, id: string, width: number, height: number): Slide => updateElement(slide, id, { width, height });
