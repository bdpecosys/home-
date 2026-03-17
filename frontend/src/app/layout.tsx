import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "GenAI Platform — Co-sell & Buying Intent",
  description: "AI-powered company discovery for startup CEOs",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "system-ui, sans-serif", margin: 0, background: "#f8fafc" }}>
        <nav style={{ background: "#1e293b", color: "#f1f5f9", padding: "12px 24px", fontWeight: 600, fontSize: 18 }}>
          GenAI Platform
        </nav>
        <main style={{ maxWidth: 1100, margin: "0 auto", padding: "24px 16px" }}>
          {children}
        </main>
      </body>
    </html>
  );
}
