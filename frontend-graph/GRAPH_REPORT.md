# Graph Report - alpr-cargo-ai-backend-skeleton  (2026-09-02)

## Corpus Check
- 61 files · ~116,653 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 343 nodes · 639 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.96)
- Token cost: 1,200 input · 850 output

## Community Hubs (Navigation)
- Web Dashboard & UI Components
- ALPR Character & Plate Detection
- Main Web App Views & Props
- API Express & Backend Dependencies
- Web Frontend Dependencies
- Web TypeScript Configuration
- Web Dev Dependencies & Tooling
- Backend Express Server & Prisma DB
- API TypeScript Configuration
- Monorepo Root Package Config
- Architecture Setup & CI Workflow
- UI Tabs Component System
- Shared Types Package
- Web Root Layout & Metadata
- Web ESLint Configuration
- Next.js Build Configuration
- PostCSS Styling Configuration

## God Nodes (most connected - your core abstractions)
1. `cn()` - 40 edges
2. `DetectionResult` - 19 edges
3. `compilerOptions` - 16 edges
4. `WhitelistRule` - 16 edges
5. `Button` - 13 edges
6. `runAlprPipelineMulti()` - 13 edges
7. `compilerOptions` - 11 edges
8. `Badge()` - 11 edges
9. `parseIndonesianPlate()` - 11 edges
10. `runAlprPipeline()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Monorepo Architecture` --verified_by--> `GitHub Actions CI Pipeline`  [INFERRED]
  SETUP_GUIDE.md → .github/workflows/ci.yml
- `Monorepo Architecture` --configured_by--> `PNPM Workspace Configuration`  [INFERRED]
  SETUP_GUIDE.md → pnpm-workspace.yaml
- `AccessManagerModalProps` --references--> `WhitelistRule`  [EXTRACTED]
  apps/web/src/components/AccessManagerModal.tsx → packages/shared-types/src/index.ts
- `CargoManifestDashboardProps` --references--> `DetectionResult`  [EXTRACTED]
  apps/web/src/components/CargoManifestDashboard.tsx → packages/shared-types/src/index.ts
- `DetectionHistoryProps` --references--> `DetectionResult`  [EXTRACTED]
  apps/web/src/components/DetectionHistory.tsx → packages/shared-types/src/index.ts

## Import Cycles
- None detected.

## Communities (17 total, 4 thin omitted)

### Community 0 - "Web Dashboard & UI Components"
Cohesion: 0.13
Nodes (38): PlateCameraFrame(), PlateCameraFrameProps, PlateCaptureResult, Badge(), BadgeProps, badgeVariants, Button, ButtonProps (+30 more)

### Community 1 - "ALPR Character & Plate Detection"
Cohesion: 0.10
Nodes (37): DetectedChar, isCharDetectorLoaded(), predictCharactersFromPlate(), ROBOFLOW_CHAR_NAMES, getRegionInfo(), INDONESIAN_PLATE_REGIONS, RegionInfo, playDetectionAudioBeep() (+29 more)

### Community 2 - "Main Web App Views & Props"
Cohesion: 0.09
Nodes (33): Home(), AccessManagerModal(), AccessManagerModalProps, CargoManifestDashboard(), CargoManifestDashboardProps, DatasetTester(), DatasetTesterProps, DetectionHistory() (+25 more)

### Community 3 - "API Express & Backend Dependencies"
Cohesion: 0.05
Nodes (37): dependencies, @alpr/shared-types, cors, express, multer, @prisma/client, zod, devDependencies (+29 more)

### Community 4 - "Web Frontend Dependencies"
Cohesion: 0.07
Nodes (29): dependencies, @alpr/shared-types, canvas-confetti, class-variance-authority, clsx, lightningcss, lucide-react, next (+21 more)

### Community 5 - "Web TypeScript Configuration"
Cohesion: 0.07
Nodes (28): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+20 more)

### Community 6 - "Web Dev Dependencies & Tooling"
Cohesion: 0.07
Nodes (26): devDependencies, eslint, eslint-config-next, @types/canvas-confetti, @types/node, @types/react, @types/react-dom, typescript (+18 more)

### Community 7 - "Backend Express Server & Prisma DB"
Cohesion: 0.21
Nodes (7): prisma, app, router, router, storage, upload, router

### Community 8 - "API TypeScript Configuration"
Cohesion: 0.14
Nodes (13): compilerOptions, declaration, esModuleInterop, module, moduleResolution, outDir, resolveJsonModule, rootDir (+5 more)

### Community 9 - "Monorepo Root Package Config"
Cohesion: 0.14
Nodes (13): engines, node, name, private, scripts, build, build:api, build:web (+5 more)

### Community 10 - "Architecture Setup & CI Workflow"
Cohesion: 0.22
Nodes (10): ONNX Plate Detector, Lampung Plate Sample 01, Lampung Plate Sample 44, GitHub Actions CI Pipeline, PNPM Workspace Configuration, Express Prisma API Backend, Monorepo Architecture, RAG & Knowledge Base Rationale (+2 more)

### Community 11 - "UI Tabs Component System"
Cohesion: 0.20
Nodes (9): Tabs, TabsContent, TabsContentProps, TabsContext, TabsContextValue, TabsList, TabsProps, TabsTrigger (+1 more)

### Community 12 - "Shared Types Package"
Cohesion: 0.33
Nodes (5): main, name, private, types, version

## Knowledge Gaps
- **135 isolated node(s):** `name`, `version`, `private`, `dev`, `build` (+130 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 145 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cn()` connect `Web Dashboard & UI Components` to `UI Tabs Component System`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `dependencies` connect `Web Frontend Dependencies` to `Web Dev Dependencies & Tooling`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **What connects `name`, `version`, `private` to the rest of the system?**
  _135 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Web Dashboard & UI Components` be split into smaller, more focused modules?**
  _Cohesion score 0.12597402597402596 - nodes in this community are weakly interconnected._
- **Should `ALPR Character & Plate Detection` be split into smaller, more focused modules?**
  _Cohesion score 0.0971322849213691 - nodes in this community are weakly interconnected._
- **Should `Main Web App Views & Props` be split into smaller, more focused modules?**
  _Cohesion score 0.08717948717948718 - nodes in this community are weakly interconnected._
- **Should `API Express & Backend Dependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._