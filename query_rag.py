"""
query_rag.py
------------
Contoh alur retrieval hybrid: vector similarity search + graph traversal,
lalu (opsional) kirim ke Claude API untuk dijawab.

Cara pakai:
    python query_rag.py "endpoint mana yang dipakai halaman upload di frontend?"

Prasyarat: sudah menjalankan build_rag_from_graph.py terlebih dahulu,
sehingga ada folder ./chroma_db/ dan file ./edge_lookup.json.
"""

import json
import sys
import chromadb
from sentence_transformers import SentenceTransformer

TOP_K = 8          # jumlah node paling relevan dari vector search
MAX_HOPS = 1        # seberapa jauh traversal ke node tetangga


def load_edge_lookup(path="edge_lookup.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def vector_search(query, collection, model, top_k=TOP_K):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
    )
    return results


def traverse_neighbors(node_ids, edge_lookup, max_hops=MAX_HOPS):
    """Ambil node tetangga (relasi langsung) dari node-node awal."""
    visited = set(node_ids)
    frontier = set(node_ids)

    for _ in range(max_hops):
        next_frontier = set()
        for nid in frontier:
            for rel, target in edge_lookup.get(nid, []):
                if target not in visited:
                    next_frontier.add(target)
                    visited.add(target)
        frontier = next_frontier

    return visited - set(node_ids)  # hanya node tambahan hasil traversal


def main():
    if len(sys.argv) < 2:
        print('Usage: python query_rag.py "pertanyaan Anda di sini"')
        sys.exit(1)

    query = sys.argv[1]

    print("Loading vector database...")
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("alpr_knowledge_graph")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    edge_lookup = load_edge_lookup()

    print(f"\nQuery: {query}\n")
    print("=== Vector Search Results (top-k paling mirip) ===")
    results = vector_search(query, collection, model)

    matched_ids = results["ids"][0]
    matched_docs = results["documents"][0]
    matched_meta = results["metadatas"][0]

    for i, (nid, doc, meta) in enumerate(zip(matched_ids, matched_docs, matched_meta)):
        print(f"\n[{i+1}] id={nid}")
        print(f"    {doc}")
        print(f"    repo={meta.get('repo')} type={meta.get('type')} community={meta.get('community')}")

    print("\n=== Graph Traversal (node terhubung dari hasil di atas) ===")
    neighbor_ids = traverse_neighbors(matched_ids, edge_lookup)

    if neighbor_ids:
        # Ambil detail node tetangga dari collection
        neighbor_data = collection.get(ids=list(neighbor_ids))
        for nid, doc in zip(neighbor_data["ids"], neighbor_data["documents"]):
            print(f"\n- id={nid}")
            print(f"  {doc}")
    else:
        print("(Tidak ada node tetangga langsung, atau edge_lookup kosong)")

    print("\n=== Konteks Gabungan untuk dikirim ke LLM ===")
    context_parts = matched_docs
    if neighbor_ids:
        neighbor_data = collection.get(ids=list(neighbor_ids))
        context_parts += neighbor_data["documents"]

    context = "\n---\n".join(context_parts)
    print(context[:2000] + ("..." if len(context) > 2000 else ""))

    print(
        "\n\nContoh langkah selanjutnya: kirim `query` + `context` di atas "
        "sebagai prompt ke Claude API (lihat bagian anthropic_api_in_artifacts "
        "kalau mau dibuatkan versi Artifact interaktifnya)."
    )


if __name__ == "__main__":
    main()
