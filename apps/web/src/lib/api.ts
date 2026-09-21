import type { Presentation, Slide } from "@/types/presentation";
const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function createPresentation(title: string): Promise<Presentation> {
  const response = await fetch(`${API}/presentations`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title }) });
  if (!response.ok) throw new Error("Unable to create presentation");
  return response.json();
}
export async function addSlide(id: string): Promise<Slide> {
  const response = await fetch(`${API}/presentations/${id}/slides`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
  if (!response.ok) throw new Error("Unable to add slide");
  return response.json();
}
export async function updateSlide(id: string, patch: Partial<Slide>): Promise<Slide> {
  const response = await fetch(`${API}/slides/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) });
  if (!response.ok) throw new Error("Unable to update slide");
  return response.json();
}
export function exportPptx(id: string) { window.open(`${API}/presentations/${id}/export`, "_blank", "noopener,noreferrer"); }
