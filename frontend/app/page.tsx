type WorkspaceOverview = {
  workspace: {
    id: string;
    name: string;
    description: string;
    focus_mode: string;
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
    id: "ws-skripsi-ai",
    name: "Workspace Skripsi AI",
    description: "Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan skripsi.",
    focus_mode: "deadline-aware",
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

function formatDueDate(value: string) {
  return new Intl.DateTimeFormat("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Jakarta",
  }).format(new Date(value));
}

async function getWorkspaceOverview(): Promise<WorkspaceOverview> {
  try {
    const response = await fetch(`${apiBaseUrl}/api/v1/workspaces/overview`, {
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error("Failed to fetch workspace overview");
    }

    return (await response.json()) as WorkspaceOverview;
  } catch {
    return fallbackOverview;
  }
}

export default async function Home() {
  const overview = await getWorkspaceOverview();
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
            <p className="workspace-kicker">
              Focus mode: <strong>{overview.workspace.focus_mode}</strong> · terakhir sinkron{