type AuthResponse = {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    name: string;
    email: string;
  };
};

type WorkspaceOverview = {
  workspace: {
    id: string;
    name: string;
    description: string;
    focus_mode: string;
    owner_id: string;
    updated_at: string;
  };
  stats: {
    active_tasks: number;
    due_today: number;
    active_agents: number;
    indexed_documents: number;
  };
  upcoming_tasks: Array<{
    title: string;
    course: string;
    due_at: string;
    priority: string;
    agent_name: string;
    status: string;
  }>;
  highlights: Array<{
    title: string;
    detail: string;
    category: string;
  }>;
};

const fallbackOverview: WorkspaceOverview = {
  workspace: {
    id: "ws-user-demo",
    name: "Workspace Demo",
    description: "Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan skripsi.",
    focus_mode: "deadline-aware",
    owner_id: "user-demo",
    updated_at: new Date().toISOString(),
  },
  stats: {
    active_tasks: 6,
    due_today: 2,
    active_agents: 3,
    indexed_documents: 18,
  },
  upcoming_tasks: [
    {
      title: "Finalkan ringkasan Bab 2",
      course: "Metodologi Penelitian",
      due_at: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString(),
      priority: "high",
      agent_name: "Document Agent",
      status: "in_review",
    },
    {
      title: "Susun timeline eksperimen",
      course: "Skripsi",
      due_at: new Date(Date.now() + 26 * 60 * 60 * 1000).toISOString(),
      priority: "medium",
      agent_name: "Task Planner Agent",
      status: "queued",
    },
    {
      title: "Rapikan catatan jurnal utama",
      course: "Natural Language Processing",
      due_at: new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString(),
      priority: "medium",
      agent_name: "Study Agent",
      status: "ready",
    },
  ],
  highlights: [
    {
      title: "Morning sync selesai",
      detail: "Deadline hari ini sudah diprioritaskan ulang berdasarkan urgensi tugas.",
      category: "scheduler",
    },
    {
      title: "Dokumen terbaru terindeks",
      detail: "Tiga referensi skripsi baru siap dipakai untuk tanya jawab berbasis dokumen.",
      category: "documents",
    },
    {
      title: "Review malam dijadwalkan",
      detail: "Agent akan menyiapkan ringkasan progres dan risiko pada pukul 20:00.",
      category: "reporting",
    },
  ],
};

const apiBaseUrl =
  process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const browserApiBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const demoEmail = process.env.DEMO_USER_EMAIL ?? "demo@mahasiswa.local";
const demoPassword = process.env.DEMO_USER_PASSWORD ?? "demo12345";

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Jakarta",
  }).format(new Date(value));
}

async function getDemoToken(): Promise<AuthResponse | null> {
  try {
    const response = await fetch(`${apiBaseUrl}/api/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: demoEmail,
        password: demoPassword,
      }),
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    return (await response.json()) as AuthResponse;
  } catch {
    return null;
  }
}

async function getWorkspaceOverview(): Promise<{ overview: WorkspaceOverview; demoUserName: string }> {
  try {
    const auth = await getDemoToken();
    if (!auth) {
      throw new Error("Demo auth unavailable");
    }

    const response = await fetch(`${apiBaseUrl}/api/v1/workspaces/overview`, {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${auth.access_token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch workspace overview");
    }

    return {
      overview: (await response.json()) as WorkspaceOverview,
      demoUserName: auth.user.name,
    };
  } catch {
    return {
      overview: fallbackOverview,
      demoUserName: "Demo Mahasiswa",
    };
  }
}

export default async function Home() {
  const { overview, demoUserName } = await getWorkspaceOverview();
  const stats = [
    {
      label: "Task aktif",
      value: `${overview.stats.active_tasks}`,
    },
    {
      label: "Jatuh tempo hari ini",
      value: `${overview.stats.due_today}`,
    },
    {
      label: "Agent aktif",
      value: `${overview.stats.active_agents}`,
    },
    {
      label: "Dokumen terindeks",
      value: `${overview.stats.indexed_documents}`,
    },
  ];

  return (
    <main className="page">
      <section className="hero">
        <div className="hero-copy">
          <div>
            <div className="eyebrow">AI Agent Workspace 24/7 untuk Mahasiswa</div>
            <h1 className="headline">{overview.workspace.name}</h1>
            <p className="subcopy">{overview.workspace.description}</p>
            <p className="subcopy">
              Login demo aktif sebagai <strong>{demoUserName}</strong> dengan mode fokus{" "}
              <strong>{overview.workspace.focus_mode}</strong>. Sinkron terakhir pada{" "}
              {formatDateTime(overview.workspace.updated_at)}.
            </p>
            <div className="actions">
              <a className="primary" href={`${browserApiBaseUrl}/docs`}>
                Buka API Docs
              </a>
              <a className="secondary" href={`${browserApiBaseUrl}/api/v1/system/summary`}>
                Lihat System Summary
              </a>
            </div>
            <div className="support-grid">
              {stats.map((item) => (
                <div className="support-item" key={item.label}>
                  <span className="support-label">{item.label}</span>
                  <strong className="support-value">{item.value}</strong>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="status-strip">
            {overview.highlights.map((item) => (
              <span key={item.title}>{item.title}</span>
            ))}
          </div>

          <div className="studio">
            <div className="canvas">
              <div className="workspace-panel">
                <div>
                  <h2>Task Prioritas</h2>
                  <p>
                    Homepage sekarang login dengan akun demo seeded lebih dulu, lalu mengambil
                    overview workspace yang sudah diproteksi bearer token.
                  </p>
                </div>

                <div className="agenda-list">
                  {overview.upcoming_tasks.map((item) => (
                    <div className="agenda-item" key={`${item.title}-${item.due_at}`}>
                      <strong>{item.title}</strong>
                      <span>
                        {item.course} · {item.agent_name} · {item.priority} priority · {item.status}
                      </span>
                      <span>Deadline {formatDateTime(item.due_at)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="timeline-panel">
                <h3>Highlight Agent</h3>
                <p>
                  Ownership workspace sekarang sudah diikat ke user aktif, jadi batch berikutnya
                  tinggal meneruskan model ini ke database dan task CRUD.
                </p>
                <div className="timeline-list">
                  {overview.highlights.map((item) => (
                    <div className="timeline-item" key={`${item.category}-${item.title}`}>
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
