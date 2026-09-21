import "./globals.css";
import type { Metadata } from "next";
export const metadata: Metadata = { title: "Brahma Slides", description: "IR-first presentation editor" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }

