# MVP Scope

## Tujuan MVP

MVP difokuskan pada satu alur yang benar-benar berguna untuk mahasiswa: melihat workspace akademik, memantau tugas prioritas, dan menyiapkan fondasi agent-driven workflow tanpa langsung melompat ke orkestrasi kompleks.

## In Scope

- autentikasi dasar pengguna
- satu atau beberapa workspace per pengguna
- daftar agent dasar per workspace
- task management sederhana
- overview dashboard yang menampilkan task aktif, due today, agent aktif, dan dokumen terindeks
- unggah dokumen sederhana
- ringkasan dokumen berbasis AI secara manual
- scheduler ringan untuk reminder dan review harian
- activity log dasar

## Sudah Ada di Branch Scaffold

- struktur monorepo awal
- baseline frontend Next.js
- baseline backend FastAPI
- baseline worker Python
- auth demo dengan token bearer ringan
- workspace overview API yang sudah terkait user aktif
- homepage yang login demo lalu membaca overview backend
- model database dan migration awal untuk `users`, `workspaces`, dan `tasks`
- auth dan workspace service yang sudah memakai PostgreSQL baseline
- task CRUD dasar berbasis database

## Ditunda Setelah MVP Dasar Stabil

- multi-agent orchestration penuh
- approval workflow kompleks lintas channel
- notifikasi WhatsApp, Telegram, atau multi-channel lain
- vector database production-grade
- collaboration multi-user tingkat lanjut
- analytics dan reporting mendalam

## Alasan Prioritas

- fitur inti harus bisa didemokan tanpa integrasi berlebihan
- data flow frontend ke backend perlu nyata sejak awal
- mahasiswa butuh manfaat cepat: task, deadline, dokumen, dan ritme kerja
- scope tetap harus realistis untuk tugas akhir atau skripsi

## Target Increment Berikutnya

1. document upload + metadata
2. scheduler reminder harian
3. activity log dasar
4. agent run history
5. document retrieval context
