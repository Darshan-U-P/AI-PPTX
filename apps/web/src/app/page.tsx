"use client";

import { ChangeEvent, useState } from "react";
import { addSlide, assetUrl, createPresentation, deleteSlide, exportPptx, getPresentation, updatePresentation, updateSlide, uploadImage } from "@/lib/api";
import { createElement, createImageElement, createShapeElement, createTextElement, deleteElement, moveElement, resizeElement, updateElement } from "@/lib/mutations";
import type { Element, Presentation, Slide } from "@/types/presentation";

export default function Home() {
  const [presentation, setPresentation] = useState<Presentation | null>(null);
  const [selectedSlideId, setSelectedSlideId] = useState<string | null>(null);
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null);
  const [title, setTitle] = useState("Untitled presentation");
  const [status, setStatus] = useState("");
  const selectedSlide = presentation?.slides.find((slide) => slide.id === selectedSlideId);
  const selectedElement = selectedSlide?.elements.find((element) => element.id === selectedElementId);

  const replaceSlide = (next: Slide) => setPresentation((current) => current && ({ ...current, slides: current.slides.map((slide) => slide.id === next.id ? next : slide) }));
  async function start() { const next = await createPresentation(title); setPresentation(next); setTitle(next.metadata.title); setStatus("Presentation created"); }
  async function saveTitle() { if (!presentation) return; const next = await updatePresentation(presentation.id, { title }); setPresentation(next); setStatus("Saved"); }
  async function reload() { if (!presentation) return; const next = await getPresentation(presentation.id); setPresentation(next); setStatus("Reloaded from API"); }
  async function addNewSlide() { if (!presentation) return; const next = await addSlide(presentation.id); setPresentation({ ...presentation, slides: [...presentation.slides, next] }); setSelectedSlideId(next.id); setStatus("Slide added"); }
  async function persistSlide(next: Slide) { const saved = await updateSlide(next.id, { order: next.order, elements: next.elements }); replaceSlide(saved); setStatus("Saved"); }
  async function addElement(element: Element) { if (!selectedSlide) return; const next = createElement(selectedSlide, element); await persistSlide(next); setSelectedElementId(element.id); }
  async function removeElement() { if (!selectedSlide || !selectedElement) return; await persistSlide(deleteElement(selectedSlide, selectedElement.id)); setSelectedElementId(null); }
  async function removeSlide() { if (!selectedSlide || !presentation) return; await deleteSlide(selectedSlide.id); const next = await getPresentation(presentation.id); setPresentation(next); setSelectedSlideId(next.slides[0]?.id ?? null); setSelectedElementId(null); }
  async function moveSlide(direction: number) { if (!selectedSlide || !presentation) return; const order = Math.max(0, Math.min(presentation.slides.length - 1, selectedSlide.order + direction)); const saved = await updateSlide(selectedSlide.id, { order }); const next = await getPresentation(presentation.id); setPresentation(next); setSelectedSlideId(saved.id); }
  async function changeElement(patch: Partial<Element>) { if (!selectedSlide || !selectedElement) return; await persistSlide(updateElement(selectedSlide, selectedElement.id, patch)); }
  async function imagePicked(event: ChangeEvent<HTMLInputElement>) { const file = event.target.files?.[0]; if (!file || !presentation) return; const asset = await uploadImage(presentation.id, file, file.name); const next = await getPresentation(presentation.id); setPresentation(next); await addElement(createImageElement(asset.source, asset.alt)); }

  return <main className="min-h-screen bg-slate-100 p-4 text-slate-900"><div className="mx-auto grid max-w-7xl grid-rows-[auto_1fr_auto] overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
    <header className="flex items-center justify-between gap-4 border-b border-slate-200 px-6 py-4"><div><h1 className="font-semibold">Brahma Slides</h1><p className="text-sm text-slate-500">Manual IR-first editor</p></div>{presentation && <div className="flex gap-2"><button onClick={reload} className="button-secondary">Reload</button><button onClick={saveTitle} className="button-secondary">Save</button><button onClick={() => exportPptx(presentation.id)} className="button-primary">Export PPTX</button></div>}</header>
    {!presentation ? <section className="grid min-h-[560px] place-items-center p-8"><div className="w-full max-w-md space-y-4 rounded-lg border p-6"><h2 className="text-lg font-semibold">Create a presentation</h2><input aria-label="Presentation title" value={title} onChange={(event) => setTitle(event.target.value)} className="input"/><button onClick={start} className="button-primary w-full">Create presentation</button></div></section> : <section className="grid min-h-[560px] grid-cols-[190px_1fr_250px]">
      <aside className="border-r border-slate-200 p-3"><h2 className="mb-3 text-sm font-semibold uppercase text-slate-500">Slides</h2>{[...presentation.slides].sort((a, b) => a.order - b.order).map((slide) => <button key={slide.id} onClick={() => { setSelectedSlideId(slide.id); setSelectedElementId(null); }} className={`mb-2 w-full rounded border p-3 text-left text-sm ${selectedSlideId === slide.id ? "border-indigo-300 bg-indigo-50" : "border-slate-200 bg-white"}`}>Slide {slide.order + 1}<span className="block text-xs text-slate-400">{slide.elements.length} elements</span></button>)}</aside>
      <div className="grid place-items-center bg-slate-50 p-8"><div className="relative w-full max-w-3xl overflow-hidden border border-slate-300 bg-white shadow" style={{ aspectRatio: `${presentation.dimensions.width}/${presentation.dimensions.height}`, background: selectedSlide?.background }}>{selectedSlide ? selectedSlide.elements.map((element) => <CanvasElement key={element.id} element={element} dimensions={presentation.dimensions} selected={selectedElementId === element.id} onSelect={() => setSelectedElementId(element.id)} />) : <p className="grid h-full place-items-center text-slate-400">Add a slide to begin</p>}</div></div>
      <aside className="border-l border-slate-200 p-4"><h2 className="text-sm font-semibold uppercase text-slate-500">Properties</h2><label className="label">Presentation title<input value={title} onChange={(event) => setTitle(event.target.value)} onBlur={saveTitle} className="input mt-1"/></label>{selectedSlide && <div className="mt-5 space-y-2"><button onClick={() => addElement(createTextElement())} className="button-secondary w-full">Add text</button><button onClick={() => addElement(createShapeElement())} className="button-secondary w-full">Add shape</button><label className="button-secondary block w-full cursor-pointer text-center">Add image<input type="file" accept="image/png,image/jpeg,image/gif,image/webp" onChange={imagePicked} className="hidden"/></label><div className="flex gap-2"><button onClick={() => moveSlide(-1)} className="button-secondary flex-1">↑ Slide</button><button onClick={() => moveSlide(1)} className="button-secondary flex-1">↓ Slide</button></div><button onClick={removeSlide} className="button-danger w-full">Delete slide</button></div>}{selectedElement && <ElementInspector element={selectedElement} onChange={changeElement} onDelete={removeElement}/>}</aside>
    </section>}
    <footer className="flex items-center justify-between border-t border-slate-200 px-6 py-3"><button disabled={!presentation} onClick={addNewSlide} className="text-sm font-medium text-indigo-700 disabled:text-slate-400">+ Add slide</button><span className="text-sm text-slate-500">{status || (presentation ? `IR version ${presentation.version}` : "No presentation")}</span></footer>
  </div></main>;
}

function CanvasElement({ element, dimensions, selected, onSelect }: { element: Element; dimensions: { width: number; height: number }; selected: boolean; onSelect: () => void }) {
  const style = { left: `${element.x / dimensions.width * 100}%`, top: `${element.y / dimensions.height * 100}%`, width: `${element.width / dimensions.width * 100}%`, height: `${element.height / dimensions.height * 100}%`, zIndex: element.z_index, transform: `rotate(${element.rotation}deg)`, opacity: element.opacity };
  const classes = `absolute overflow-hidden ${selected ? "ring-2 ring-indigo-500" : ""}`;
  if (element.type === "text") return <button onClick={onSelect} style={{ ...style, color: element.color, fontSize: `${element.font_size ?? 18}px` }} className={`${classes} text-left`}>{element.text}</button>;
  if (element.type === "shape") return <button aria-label="Shape" onClick={onSelect} style={{ ...style, background: element.fill, border: `${element.stroke_width ?? 0}px solid ${element.stroke}`, borderRadius: element.shape_type === "ellipse" ? "9999px" : element.shape_type === "rounded_rectangle" ? "12px" : "0" }} className={classes}/>;
  if (element.type === "image" && element.source) return <button aria-label={element.alt ?? "Image"} onClick={onSelect} style={style} className={classes}><img alt={element.alt ?? ""} src={assetUrl(element.source)} className="h-full w-full object-contain"/></button>;
  return <button aria-label={element.type} onClick={onSelect} style={style} className={classes}>{element.type}</button>;
}

function ElementInspector({ element, onChange, onDelete }: { element: Element; onChange: (patch: Partial<Element>) => void; onDelete: () => void }) {
  const number = (name: "x" | "y" | "width" | "height", value: number) => <label className="label">{name}<input type="number" step="0.1" min="0" value={value} onChange={(event) => onChange({ [name]: Number(event.target.value) })} className="input mt-1"/></label>;
  return <div className="mt-6 space-y-3 border-t pt-4"><h3 className="text-sm font-semibold">Selected {element.type}</h3>{element.type === "text" && <label className="label">Text<textarea value={element.text ?? ""} onChange={(event) => onChange({ text: event.target.value })} className="input mt-1 min-h-20"/></label>}<div className="grid grid-cols-2 gap-2">{number("x", element.x)}{number("y", element.y)}{number("width", element.width)}{number("height", element.height)}</div><button onClick={onDelete} className="button-danger w-full">Delete element</button></div>;
}
