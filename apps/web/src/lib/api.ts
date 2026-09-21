import type { Asset, Presentation, Slide } from "@/types/presentation";

export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API}${path}`, init);
  if (!response.ok) throw new Error((await response.json().catch(() => null))?.error?.message ?? "Request failed");
  return response.json() as Promise<T>;
}

export const createPresentation = (title: string) => request<Presentation>("/presentations", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title }) });
export const getPresentation = (id: string) => request<Presentation>(`/presentations/${id}`);
export const updatePresentation = (id: string, patch: { title?: string; description?: string }) => request<Presentation>(`/presentations/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) });
export const addSlide = (id: string) => request<Slide>(`/presentations/${id}/slides`, { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" });
export const updateSlide = (id: string, patch: Partial<Slide>) => request<Slide>(`/slides/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) });
export const deleteSlide = async (id: string) => { await request<void>(`/slides/${id}`, { method: "DELETE" }); };
export async function uploadImage(presentationId: string, file: File, alt: string): Promise<Asset> {
  const form = new FormData(); form.append("file", file); form.append("alt", alt);
  return request<Asset>(`/presentations/${presentationId}/assets`, { method: "POST", body: form });
}
export const exportPptx = (id: string) => window.open(`${API}/presentations/${id}/export`, "_blank", "noopener,noreferrer");
export const assetUrl = (source: string) => source.startsWith("asset://") ? `${API}/assets/${source.slice(8).split(".")[0]}` : source;
