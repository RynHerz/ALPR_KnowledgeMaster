# ALPR_KnowledgeMaster - Cross-Repo Knowledge Graph

Repository ini berisi knowledge graph gabungan (cross-repo) dari sistem **Automatic License Plate Recognition (ALPR) Cargo**, yang menggabungkan struktur kode, dependensi, arsitektur, dan relasi semantik dari sisi frontend dan backend.

Dibuat menggunakan tool **[Graphify](https://github.com/RynHerz)** untuk keperluan **Retrieval-Augmented Generation (RAG)**, pemahaman arsitektur komprehensif, dan penalaran multi-hop bagi Agentic AI / LLM.

---

## 🔗 Sumber Repositori

Knowledge graph ini diekstraksi dan digabungkan dari dua repositori utama:

1. **Frontend**: [https://github.com/RynHerz/Alpr_Cargo](https://github.com/RynHerz/Alpr_Cargo)
   - Stack: Next.js, React, Tailwind CSS, TypeScript monorepo.
   - Komponen UI dashboard, visualisasi feed kamera ALPR, deteksi plat nomor, parsing format plat Indonesia, dan manajemen kontainer/kargo.
2. **Backend**: [https://github.com/RynHerz/BE_ALPR](https://github.com/RynHerz/BE_ALPR)
   - Stack: Express.js, TypeScript, Prisma ORM, Multer.
   - REST API backend, manajemen storage/upload hasil snapshot plat kargo, dan integrasi database Prisma.

---

## 📂 Struktur Direktori

```text
ALPR_KnowledgeMaster/
├── merged-graph.json       # Knowledge graph gabungan (Cross-Repo) untuk RAG
├── frontend-graph/         # Hasil ekstraksi Graphify lengkap dari Alpr_Cargo
│   ├── graph.json          # Node & relasi frontend (343 nodes, 639 edges)
│   ├── graph.html          # Visualisasi interaktif D3 force-directed frontend
│   ├── GRAPH_REPORT.md     # Laporan arsitektur, god nodes, & komunitas frontend
│   ├── manifest.json       # Manifest hashing berkas
│   └── cache/              # Cache ekstraksi AST & semantik
├── backend-graph/          # Hasil ekstraksi Graphify lengkap dari BE_ALPR
│   ├── graph.json          # Node & relasi backend (64 nodes, 67 edges)
│   ├── graph.html          # Visualisasi interaktif D3 force-directed backend
│   ├── GRAPH_REPORT.md     # Laporan arsitektur, god nodes, & komunitas backend
│   ├── manifest.json       # Manifest hashing berkas
│   └── cache/              # Cache ekstraksi AST
└── README.md               # Dokumentasi knowledge graph ini
```

---

## 📊 Ringkasan Graph

| Metrik | Frontend (`Alpr_Cargo`) | Backend (`BE_ALPR`) | Gabungan (`merged-graph.json`) |
| :--- | :--- | :--- | :--- |
| **Total Nodes** | 343 | 64 | **407** |
| **Total Edges** | 639 | 67 | **706** |
| **Namespacing** | `alpr-cargo-ai-backend-skeleton::*` | `BE_ALPR::*` | Terintegrasi cross-repo |

---

## 🛠️ Penggunaan untuk RAG & Analisis

### 1. Navigasi & Graph Querying via Graphify CLI

- **Mencari Jalur Terpendek Antar Komponen (Shortest Path)**:
  ```bash
  graphify path "<Node_Frontend>" "<Node_Backend>" --graph merged-graph.json
  ```

- **Mendapatkan Penjelasan Node & Tetangganya**:
  ```bash
  graphify explain "<Node_Name>" --graph merged-graph.json
  ```

### 2. Integrasi Pipeline RAG

Berkas `merged-graph.json` dapat dimuat langsung ke dalam pipeline RAG atau Graph RAG (seperti LangChain, LlamaIndex, FalkorDB, Neo4j, dsb.) sebagai:
- **Topology-aware context**: Memberikan konteks relasi antarmuka frontend dan endpoint backend.
- **Dependency context**: Menghubungkan tipe data frontend (`shared-types`, `DetectionResult`) dengan skema data Prisma backend.
- **Hierarchical community indexing**: Memudahkan navigasi klaster fungsional (UI, deteksi ALPR, API route, database).

### 3. Visualisasi Grafis

Untuk melihat interaksi komponen secara visual dalam graf interaktif, buka berkas `graph.html` di browser:
- Frontend visualizer: `frontend-graph/graph.html`
- Backend visualizer: `backend-graph/graph.html`

---

*Generated and merged using Graphify.*
