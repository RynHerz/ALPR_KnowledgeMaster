"""
generate_answer.py
-------------------
Tahap "Generation" dari pipeline RAG: mengambil hasil retrieval
(vector search + graph traversal dari query_rag.py) lalu mengirimnya
sebagai konteks ke Google Gemini API untuk dirangkai jadi jawaban
natural.

Cara pakai:
    pip install google-genai chromadb sentence-transformers --break-system-packages
    set GEMINI_API_KEY di environment variable (atau file .env)
    python generate_answer.py "endpoint mana yang dipakai halaman upload di frontend?"

Catatan model:
    Nama model Gemini berubah dari waktu ke waktu. Jika model default di
    bawah gagal/deprecated, jalankan dulu list_models() untuk melihat
    model yang tersedia saat ini di akun Anda, lalu isi env var
    GEMINI_MODEL dengan nama model yang valid.
"""

import json
import os
import sys

import chromadb
from sentence_transformers import SentenceTransformer

try:
    from dotenv import load_dotenv
    load_dotenv()  # baca file .env di folder ini kalau ada
except ImportError:
    pass  # python-dotenv opsional; kalau tidak ada, tetap bisa pakai env var manual

try:
    from google import genai
except ImportError:
    print(
        "Package belum terinstall. Jalankan dulu:\n"
        "  pip install google-genai --break-system-packages\n"
    )
    sys.exit(1)

TOP_K = 8
MAX_HOPS = 1
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")


def load_edge_lookup(path="edge_lookup.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def vector_search(query, collection, model, top_k=TOP_K):
    query_embedding = model.encode([query]).tolist()
    return collection.query(query_embeddings=query_embedding, n_results=top_k)


def traverse_neighbors(node_ids, edge_lookup, max_hops=MAX_HOPS):
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
    return visited - set(node_ids)


def list_models(client):
    """Bantu debug kalau nama model default sudah tidak valid lagi."""
    print("Model yang tersedia untuk akun Gemini Anda:")
    for m in client.models.list():
        print(f"  - {m.name}")


def build_context(query, collection, embed_model, edge_lookup):
    results = vector_search(query, collection, embed_model)
    matched_ids = results["ids"][0]
    matched_docs = results["documents"][0]

    neighbor_ids = traverse_neighbors(matched_ids, edge_lookup)
    neighbor_docs = []
    if neighbor_ids:
        neighbor_data = collection.get(ids=list(neighbor_ids))
        neighbor_docs = neighbor_data["documents"]

    context = "\n---\n".join(matched_docs + neighbor_docs)
    return context, matched_ids, neighbor_ids


def main():
    if len(sys.argv) < 2:
        print('Usage: python generate_answer.py "pertanyaan Anda"')
        sys.exit(1)

    query = sys.argv[1]

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(
            "GEMINI_API_KEY tidak ditemukan di environment variable.\n"
            "Set dulu, contoh (Windows PowerShell):\n"
            '  $env:GEMINI_API_KEY="isi_key_anda"\n'
            "atau (Linux/Mac):\n"
            '  export GEMINI_API_KEY="isi_key_anda"'
        )
        sys.exit(1)

    print("Loading vector database & embedding model...")
    client_db = chromadb.PersistentClient(path="./chroma_db")
    collection = client_db.get_collection("alpr_knowledge_graph")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    edge_lookup = load_edge_lookup()

    print("Retrieving context...")
    context, matched_ids, neighbor_ids = build_context(query, collection, embed_model, edge_lookup)

    print(f"Retrieved {len(matched_ids)} node utama + {len(neighbor_ids)} node tetangga.\n")

    prompt = f"""Kamu adalah asisten teknis yang menjelaskan arsitektur codebase ALPR Cargo
(sistem deteksi plat nomor kendaraan cargo), yang terdiri dari repo frontend (Next.js)
dan backend (Express + Prisma) terpisah.

Berikut konteks kode yang relevan, diambil dari knowledge graph codebase (setiap baris
adalah satu node/simbol kode beserta lokasi filenya):

{context}

Pertanyaan pengguna: {query}

Jawab dalam Bahasa Indonesia, jelas dan ringkas, dengan menyebutkan nama file dan
fungsi/komponen yang relevan dari konteks di atas. Jika konteks tidak cukup untuk
menjawab, katakan dengan jujur bagian mana yang tidak tersedia."""

    print("Mengirim ke Gemini API...")
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=DEFAULT_MODEL,
            contents=prompt,
        )
        print("\n=== Jawaban ===\n")
        print(response.text)
    except Exception as e:
        print(f"\nError saat memanggil Gemini API: {e}")
        print(f"\nModel yang dicoba: {DEFAULT_MODEL}")
        print("Menampilkan daftar model yang tersedia untuk membantu debug:\n")
        try:
            list_models(client)
        except Exception as e2:
            print(f"Gagal juga mengambil daftar model: {e2}")
        print(
            "\nSet environment variable GEMINI_MODEL ke salah satu nama model "
            "di atas, lalu coba lagi."
        )


if __name__ == "__main__":
    main()
