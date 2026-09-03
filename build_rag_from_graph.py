"""
build_rag_from_graph.py
------------------------
Mengubah merged-graph.json (hasil Graphify) menjadi vector database
lokal (ChromaDB) untuk keperluan RAG.

Cara pakai:
    pip install chromadb sentence-transformers --break-system-packages
    python build_rag_from_graph.py merged-graph.json

Setelah selesai, akan muncul folder ./chroma_db/ berisi vector index.
Jalankan query_rag.py untuk mencoba tanya-jawab.
"""

import json
import sys
import os

def load_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_nodes_and_edges(data):
    """
    Graphify bisa menyimpan graph dengan nama key yang sedikit berbeda
    tergantung versi (nodes/edges atau nodes/links). Fungsi ini mencoba
    menebak otomatis.
    """
    nodes = None
    edges = None

    # Coba key umum untuk nodes
    for key in ["nodes", "Nodes", "vertices"]:
        if key in data and isinstance(data[key], list):
            nodes = data[key]
            break

    # Coba key umum untuk edges
    for key in ["edges", "Edges", "links", "relations"]:
        if key in data and isinstance(data[key], list):
            edges = data[key]
            break

    if nodes is None:
        raise ValueError(
            f"Tidak menemukan daftar node. Key yang ada di JSON: {list(data.keys())}\n"
            "Silakan cek manual struktur file dan sesuaikan find_nodes_and_edges()."
        )

    return nodes, edges or []


def node_id(node):
    for key in ["id", "ID", "node_id", "name"]:
        if key in node:
            return str(node[key])
    return str(hash(json.dumps(node, sort_keys=True)))


def node_to_text(node):
    """
    Ubah satu node jadi deskripsi teks yang enak di-embed.
    Menyesuaikan field yang tersedia, apapun namanya.
    """
    parts = []

    name = node.get("name") or node.get("label") or node.get("id") or "unknown"
    community_name = node.get("community_name") or node.get("community") or ""
    is_callable = node.get("_callable") is True
    ntype = node.get("type") or node.get("kind") or node.get("category") or node.get("file_type") or ""

    raw_file = node.get("source_file") or node.get("file") or node.get("file_path") or node.get("path") or ""
    source_loc = node.get("source_location") or ""
    if raw_file and source_loc:
        file_path = f"{raw_file}:{source_loc}"
    else:
        file_path = raw_file

    repo = node.get("repo") or node.get("source_repo") or node.get("origin") or ""
    docstring = node.get("docstring") or node.get("summary") or node.get("description") or ""
    signature = node.get("signature") or ""

    parts.append(f"Name: {name}")
    if community_name:
        parts.append(f"Domain/Module: {community_name}")
    if is_callable:
        parts.append("Kind: function/method (callable)")
    if ntype:
        parts.append(f"Type: {ntype}")
    if repo:
        parts.append(f"Repo: {repo}")
    if file_path:
        parts.append(f"File: {file_path}")
    if signature:
        parts.append(f"Signature: {signature}")
    if docstring:
        parts.append(f"Description: {docstring}")

    return " | ".join(parts)


def build_edge_lookup(edges):
    """Bangun index: node_id -> list of (relation, target_id) (dua arah / bidirectional)"""
    lookup = {}
    for e in edges:
        src = e.get("source") or e.get("from") or e.get("src")
        dst = e.get("target") or e.get("to") or e.get("dst")
        rel = e.get("type") or e.get("relation") or e.get("label") or "related_to"
        if src is None or dst is None:
            continue
        lookup.setdefault(str(src), []).append((rel, str(dst)))
        lookup.setdefault(str(dst), []).append((f"{rel}_reverse", str(src)))
    return lookup


def main():
    if len(sys.argv) < 2:
        print("Usage: python build_rag_from_graph.py <path_to_merged-graph.json>")
        sys.exit(1)

    graph_path = sys.argv[1]
    print(f"Loading graph from {graph_path} ...")
    data = load_graph(graph_path)

    nodes, edges = find_nodes_and_edges(data)
    print(f"Found {len(nodes)} nodes and {len(edges)} edges.")

    edge_lookup = build_edge_lookup(edges)

    # Simpan edge_lookup untuk dipakai saat query nanti (graph traversal)
    with open("edge_lookup.json", "w", encoding="utf-8") as f:
        json.dump(edge_lookup, f, indent=2)
    print("Saved edge_lookup.json (untuk graph traversal saat retrieval).")

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print(
            "\nPackage belum terinstall. Jalankan dulu:\n"
            "  pip install chromadb sentence-transformers --break-system-packages\n"
        )
        sys.exit(1)

    print("Loading embedding model (all-MiniLM-L6-v2, lokal, gratis)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("alpr_knowledge_graph")

    ids, texts, metadatas = [], [], []
    for node in nodes:
        nid = node_id(node)
        text = node_to_text(node)
        ids.append(nid)
        texts.append(text)

        raw_file = node.get("source_file") or node.get("file") or node.get("file_path") or node.get("path") or ""
        source_loc = node.get("source_location") or ""
        meta_file = f"{raw_file}:{source_loc}" if (raw_file and source_loc) else raw_file

        metadatas.append({
            "repo": node.get("repo") or node.get("source_repo") or "unknown",
            "type": node.get("type") or node.get("kind") or node.get("category") or node.get("file_type") or "unknown",
            "file": meta_file,
            "community": str(node.get("community_name") or node.get("community") or "unknown"),
        })

    print(f"Embedding {len(texts)} nodes... (bisa beberapa menit tergantung jumlah node)")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    # ChromaDB punya batas ukuran batch, kirim per 500
    batch_size = 500
    for i in range(0, len(ids), batch_size):
        collection.add(
            ids=ids[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            documents=texts[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
        )

    print(f"\nSelesai! Vector database tersimpan di ./chroma_db/")
    print(f"Total node ter-index: {len(ids)}")
    print("Sekarang jalankan query_rag.py untuk mencoba tanya-jawab.")


if __name__ == "__main__":
    main()
