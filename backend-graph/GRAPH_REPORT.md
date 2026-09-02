# Graph Report - BE_ALPR  (2026-09-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 64 nodes · 67 edges · 5 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3850c48d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- devDependencies
- compilerOptions
- index.ts
- dependencies
- package.json

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 11 edges
2. `scripts` - 6 edges
3. `prisma` - 3 edges
4. `prisma` - 2 edges
5. `tsx` - 2 edges
6. `@types/cors` - 2 edges
7. `@types/express` - 2 edges
8. `@types/multer` - 2 edges
9. `@types/node` - 2 edges
10. `typescript` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (5 total, 0 thin omitted)

### Community 0 - "devDependencies"
Cohesion: 0.13
Nodes (15): devDependencies, prisma, tsx, @types/cors, @types/express, @types/multer, @types/node, typescript (+7 more)

### Community 1 - "compilerOptions"
Cohesion: 0.14
Nodes (13): src, compilerOptions, declaration, esModuleInterop, module, moduleResolution, outDir, resolveJsonModule (+5 more)

### Community 2 - "index.ts"
Cohesion: 0.21
Nodes (7): prisma, app, router, router, storage, upload, router

### Community 3 - "dependencies"
Cohesion: 0.18
Nodes (11): cors, express, multer, dependencies, cors, express, multer, @prisma/client (+3 more)

### Community 4 - "package.json"
Cohesion: 0.20
Nodes (9): name, private, scripts, build, dev, prisma:generate, prisma:migrate, start (+1 more)

## Knowledge Gaps
- **34 isolated node(s):** `prisma`, `tsx`, `@types/cors`, `@types/express`, `@types/multer` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 36 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `devDependencies` connect `devDependencies` to `package.json`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `package.json`?**
  _High betweenness centrality (0.148) - this node is a cross-community bridge._
- **What connects `prisma`, `tsx`, `@types/cors` to the rest of the system?**
  _34 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Should `compilerOptions` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._