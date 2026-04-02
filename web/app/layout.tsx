import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body style={{ margin: 0, fontFamily: "system-ui" }}>
        <div style={{ display: "flex", height: "100vh" }}>
          <aside
            style={{
              width: 260,
              borderRight: "1px solid #222",
              padding: 16,
              background: "#0b0b0b",
              color: "#fff",
            }}
          >
            <div style={{ fontWeight: 700, marginBottom: 16 }}>Shortsauto</div>
            <nav style={{ display: "grid", gap: 8 }}>
              <a href="/brief" style={{ color: "#fff", textDecoration: "none" }}>
                Brief
              </a>
              <a href="/drafts" style={{ color: "#fff", textDecoration: "none" }}>
                Drafts
              </a>
            </nav>
          </aside>
          <main style={{ flex: 1, background: "#111", color: "#eee", padding: 20 }}>{children}</main>
        </div>
      </body>
    </html>
  );
}
