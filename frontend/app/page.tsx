import { revalidatePath } from "next/cache";

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
    scheduler_enabled: boolean;
    reminder_window_hours: number;
    max_tasks_per_run: number;
    updated_at: string;
  };
  scheduler_settings: {
    scheduler_enabled: boolean;
    reminder_window_hours: number;
    max_tasks_per_run: number;
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

type DocumentItem = {
  id: string;
  workspace_id: string;
  owner_id: string;
  title: string;
  original_filename: string;
  content_type: string;
  size_bytes: number;
  processing_status: string;
  retrieval_preview: string | null;
  indexed_at: string | null;
  retrieval_ready: boolean;
  created_at: string;
  updated_at: string;
};

type SchedulerRunItem = {
  id: string;
  workspace_id: string;
  owner_id: string;
  job_name: string;
  trigger_type: string;
  status: string;
  summary: string;
  started_at: string;
  finished_at: string | null;
  created_at: string;
  updated_at: string;
};

const fallbackOverview: WorkspaceOverview = {
  workspace: {
    id: "ws-user-demo",
    name: "Workspace Demo",
    description: "Ruang kerja untuk tugas, ringkasan dokumen, dan ritme pengerjaan skripsi.",
    focus_mode: "deadline-aware",
    owner_id: "user-demo",
    scheduler_enabled: true,
    reminder_window_hours: 24,
    max_tasks_per_run: 2,
    updated_at: new Date().toISOString(),
  },
  scheduler_settings: {
    scheduler_enabled: true,
    reminder_window_hours: 24,
    max_tasks_per_run: 2,
  },
  stats: {
    active_tasks: 6,
    due_today: 2,
    active_agents: 3,
    indexed_documents: 2,
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
      title: "Retrieval context aktif",
      detail: "Dokumen teks dan PDF sederhana sekarang bisa disiapkan menjadi context retrieval dasar.",
      category: "documents",
    },
    {
      title: "Review malam dijadwalkan",
      detail: "Agent akan menyiapkan ringkasan progres dan risiko pada pukul 20:00.",
      category: "reporting",
    },
  ],
};

const fallbackDocuments: DocumentItem[] = [
  {
    id: "doc-demo-1",
    workspace_id: "ws-user-demo",
    owner_id: "user-demo",
    title: "Ringkasan Metodologi",
    original_filename: "ringkasan-metodologi.txt",
    content_type: "text/plain",
    size_bytes: 61,
    processing_status: "indexed",
    retrieval_preview: "Ringkasan metodologi penelitian untuk workspace demo mahasiswa.",
    indexed_at: new Date().toISOString(),
    retrieval_ready: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: "doc-demo-2",
    workspace_id: "ws-user-demo",
    owner_id: "user-demo",
    title: "Catatan Literatur NLP",
    original_filename: "catatan-literatur-nlp.txt",
    content_type: "text/plain",
    size_bytes: 71,
    processing_status: "indexed",
    retrieval_preview: "Catatan literatur NLP dasar untuk review literatur dan indexing awal.",
    indexed_at: new Date().toISOString(),
    retrieval_ready: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

const fallbackSchedulerRuns: SchedulerRunItem[] = [
  {
    id: "srun-demo-latest",
    workspace_id: "ws-user-demo",
    owner_id: "user-demo",
    job_name: "manual-refresh",
    trigger_type: "manual",
    status: "success",
    summary: "Scheduler demo terakhir dijalankan manual untuk menyegarkan shortlist deadline dan ritme belajar.",
    started_at: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
    finished_at: new Date(Date.now() - 20 * 60 * 1000 + 2000).toISOString(),
    created_at: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
    updated_at: new Date(Date.now() - 20 * 60 * 1000).toISOString(),
  },
  {
    id: "srun-demo-worker",
    workspace_id: "ws-user-demo",
    owner_id: "user-demo",
    job_name: "daily-reminder",
    trigger_type: "worker",
    status: "success",
    summary: "Worker demo mengecek deadline 24 jam dan menyiapkan agent run pengingat.",
    started_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    finished_at: new Date(Date.now() - 3 * 60 * 60 * 1000 + 2000).toISOString(),
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    updated_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  },
];

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

function formatFileSize(bytes: number) {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function clampNumber(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
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

async function getWorkspaceSnapshot(): Promise<{
  overview: WorkspaceOverview;
  demoUserName: string;
  documents: DocumentItem[];
  schedulerRuns: SchedulerRunItem[];
}> {
  try {
    const auth = await getDemoToken();
    if (!auth) {
      throw new Error("Demo auth unavailable");
    }

    const overviewResponse = await fetch(`${apiBaseUrl}/api/v1/workspaces/overview`, {
      cache: "no-store",
      headers: {
        Authorization: `Bearer ${auth.access_token}`,
      },
    });

    if (!overviewResponse.ok) {
      throw new Error("Failed to fetch workspace overview");
    }

    const overview = (await overviewResponse.json()) as WorkspaceOverview;
    const documentsResponse = await fetch(
      `${apiBaseUrl}/api/v1/workspaces/${overview.workspace.id}/documents`,
      {
        cache: "no-store",
        headers: {
          Authorization: `Bearer ${auth.access_token}`,
        },
      },
    );

    const documents = documentsResponse.ok
      ? ((await documentsResponse.json()) as DocumentItem[])
      : fallbackDocuments;
    const schedulerRunsResponse = await fetch(
      `${apiBaseUrl}/api/v1/workspaces/${overview.workspace.id}/scheduler-runs?limit=4`,
      {
        cache: "no-store",
        headers: {
          Authorization: `Bearer ${auth.access_token}`,
        },
      },
    );

    const schedulerRuns = schedulerRunsResponse.ok
      ? ((await schedulerRunsResponse.json()) as SchedulerRunItem[])
      : fallbackSchedulerRuns;

    return {
      overview,
      demoUserName: auth.user.name,
      documents,
      schedulerRuns,
    };
  } catch {
    return {
      overview: fallbackOverview,
      demoUserName: "Demo Mahasiswa",
      documents: fallbackDocuments,
      schedulerRuns: fallbackSchedulerRuns,
    };
  }
}

async function triggerManualSchedulerRun(workspaceId: string) {
  "use server";

  const auth = await getDemoToken();
  if (!auth) {
    throw new Error("Demo auth unavailable");
  }

  const response = await fetch(`${apiBaseUrl}/api/v1/workspaces/${workspaceId}/scheduler-runs/trigger`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${auth.access_token}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to trigger manual scheduler run");
  }

  revalidatePath("/");
}

async function updateWorkspaceSchedulerSettings(workspaceId: string, formData: FormData) {
  "use server";

  const auth = await getDemoToken();
  if (!auth) {
    throw new Error("Demo auth unavailable");
  }

  const reminderWindowHours = clampNumber(
    Number.parseInt(String(formData.get("reminder_window_hours") ?? "24"), 10) || 24,
    1,
    168,
  );
  const maxTasksPerRun = clampNumber(
    Number.parseInt(String(formData.get("max_tasks_per_run") ?? "2"), 10) || 2,
    1,
    10,
  );

  const response = await fetch(`${apiBaseUrl}/api/v1/workspaces/${workspaceId}/scheduler-settings`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${auth.access_token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      scheduler_enabled: formData.get("scheduler_enabled") === "on",
      reminder_window_hours: reminderWindowHours,
      max_tasks_per_run: maxTasksPerRun,
    }),
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to update scheduler settings");
  }

  revalidatePath("/");
}

export default async function Home() {
  const { overview, demoUserName, documents, schedulerRuns } = await getWorkspaceSnapshot();
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
      label: "Dokumen siap retrieval",
      value: `${overview.stats.indexed_documents}`,
    },
  ];
  const indexedDocuments = documents.filter((item) => item.retrieval_ready);

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
                    Dashboard sekarang sudah membaca jumlah dokumen yang benar-benar siap dipakai
                    untuk retrieval context, bukan sekadar total upload mentah.
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

              <div className="side-stack">
                <div className="timeline-panel">
                  <div className="panel-header">
                    <div>
                      <h3>Scheduler Manual</h3>
                      <p>
                        Jalankan refresh singkat untuk memperbarui shortlist deadline dan histori
                        run workspace.
                      </p>
                      <p>
                        Rule aktif:{" "}
                        {overview.scheduler_settings.scheduler_enabled ? "auto aktif" : "auto nonaktif"} · horizon{" "}
                        {overview.scheduler_settings.reminder_window_hours} jam · max{" "}
                        {overview.scheduler_settings.max_tasks_per_run} task per run
                      </p>
                    </div>
                    <form action={triggerManualSchedulerRun.bind(null, overview.workspace.id)}>
                      <button className="manual-trigger" type="submit">
                        Jalankan Sekarang
                      </button>
                    </form>
                  </div>
                  <form
                    className="scheduler-settings-form"
                    action={updateWorkspaceSchedulerSettings.bind(null, overview.workspace.id)}
                  >
                    <label className="scheduler-toggle">
                      <input
                        defaultChecked={overview.scheduler_settings.scheduler_enabled}
                        name="scheduler_enabled"
                        type="checkbox"
                      />
                      <span>Auto scheduler aktif</span>
                    </label>
                    <div className="scheduler-settings-grid">
                      <label className="scheduler-field">
                        <span>Horizon reminder</span>
                        <div className="scheduler-input-row">
                          <input
                            defaultValue={overview.scheduler_settings.reminder_window_hours}
                            max={168}
                            min={1}
                            name="reminder_window_hours"
                            type="number"
                          />
                          <small>jam</small>
                        </div>
                      </label>
                      <label className="scheduler-field">
                        <span>Maks task per run</span>
                        <div className="scheduler-input-row">
                          <input
                            defaultValue={overview.scheduler_settings.max_tasks_per_run}
                            max={10}
                            min={1}
                            name="max_tasks_per_run"
                            type="number"
                          />
                          <small>task</small>
                        </div>
                      </label>
                    </div>
                    <button className="settings-submit" type="submit">
                      Simpan Rule
                    </button>
                  </form>
                  <div className="timeline-list">
                    {schedulerRuns.map((item) => (
                      <div className="timeline-item" key={item.id}>
                        <strong>
                          {item.trigger_type === "manual" ? "Manual Trigger" : "Worker Tick"} ·{" "}
                          {item.job_name}
                        </strong>
                        <span>{item.summary}</span>
                        <span>
                          {item.status} · {formatDateTime(item.started_at)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="timeline-panel retrieval-panel">
                  <h3>Retrieval Context</h3>
                  <p>
                    Upload teks dan PDF sederhana kini langsung membentuk preview context dasar
                    untuk kebutuhan agent, pencarian, dan rangkuman akademik.
                  </p>
                  <div className="timeline-list">
                    {indexedDocuments.slice(0, 3).map((item) => (
                      <div className="timeline-item" key={item.id}>
                        <strong>{item.title}</strong>
                        <span>{item.retrieval_preview ?? "Preview belum tersedia."}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="documents-band">
        <div className="documents-header">
          <div>
            <div className="eyebrow">Document Retrieval</div>
            <h2>Dokumen yang sudah siap jadi context</h2>
          </div>
          <p>
            Batch ini menambahkan preview retrieval, status indexing, dan endpoint context search
            dasar per workspace.
          </p>
        </div>

        <div className="documents-grid">
          {documents.map((item) => (
            <article className="document-card" key={item.id}>
              <div className="document-meta">
                <span className={`document-badge ${item.retrieval_ready ? "ready" : "pending"}`}>
                  {item.retrieval_ready ? "Retrieval Ready" : item.processing_status}
                </span>
                <span>{formatFileSize(item.size_bytes)}</span>
              </div>
              <h3>{item.title}</h3>
              <p>{item.retrieval_preview ?? "Dokumen belum punya context preview yang siap dipakai."}</p>
              <div className="document-footer">
                <span>{item.original_filename}</span>
                <span>
                  {item.indexed_at ? `Indexed ${formatDateTime(item.indexed_at)}` : "Menunggu indexing"}
                </span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
