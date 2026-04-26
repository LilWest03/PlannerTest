const agenda = [
  {
    title: "Linear Algebra Quiz",
    meta: "Due today · Agent reminder aktif",
  },
  {
    title: "Riset mini NLP",
    meta: "3 sumber sudah diindeks",
  },
  {
    title: "Proposal skripsi",
    meta: "Draft bab 1 siap direview",
  },
];

const timeline = [
  {
    title: "09:00 · Sinkron deadline dari kalender",
    detail: "Worker menarik agenda, memperbarui prioritas tugas.",
  },
  {
    title: "13:00 · Ringkasan dokumen kuliah",
    detail: "Backend menyiapkan context untuk workspace aktif.",
  },
  {
    title: "20:00 · Review progres harian",
    detail: "Agent menyusun highlight, risiko, dan next step.",
  },
];

export default function Home() {
  return (
    <main className="page">
      <section className="hero">
        <div className="hero-copy">
          <div>
            <div className="eyebrow">AI Agent Workspace 24/7 untuk Mahasiswa</div>
            <h1 className="headline">Belajar lebih tenang, deadline lebih terkendali.</h1>
            <p className="subcopy">
              Dashboard awal ini menempatkan agenda kuliah, tugas prioritas, dan ritme kerja
              agent dalam satu workspace yang terasa fokus, hangat, dan siap dikembangkan.
            </p>
            <div className="actions">
              <a className="primary" href="http://localhost:8000/docs">
                Buka API Docs
              </a>
              <a className="secondary" href="http://localhost:8000/api/v1/system/summary">
                Lihat System Summary
              </a>
            </div>
            <div className="support-grid">
              <div className="support-item">
                <span className="support-label">Workspace</span>
                <strong className="support-value">Task, dokumen, dan ritme belajar</strong>
              </div>
              <div className="support-item">
                <span className="support-label">Mode</span>
                <strong className="support-value">Student-centered MVP</strong>
              </div>
              <div className="support-item">
                <span className="support-label">Batch</span>
                <strong className="support-value">Frontend, backend, worker baseline</strong>
              </div>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="status-strip">
            <span>Backend API ready</span>
            <span>Worker heartbeat active</span>
            <span>Compose scaffold connected</span>
          </div>

          <div className="studio">
            <div className="canvas">
              <div className="workspace-panel">
                <div>
                  <h2>Ruang kerja harian mahasiswa</h2>
                  <p>
                    Fokus awal untuk MVP adalah menyatukan deadline, ringkasan materi, dan alur
                    task agent ke permukaan kerja yang cepat dipindai.
                  </p>
                </div>

                <div className="agenda-list">
                  {agenda.map((item) => (
                    <div className="agenda-item" key={item.title}>
                      <strong>{item.title}</strong>
                      <span>{item.meta}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="timeline-panel">
                <h3>Agent Rhythm</h3>
                <p>Batch 2 memberi bentuk awal pada alur scheduler dan background processing.</p>
                <div className="timeline-list">
                  {timeline.map((item) => (
                    <div className="timeline-item" key={item.title}>
                      <strong>{item.title}</strong>
                      <span>{item.detail}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
