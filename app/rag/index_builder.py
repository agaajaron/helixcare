import os

def build_policy_index(policies_dir: str = "data/policies", persist_dir: str = "storage/policies", force_rebuild: bool = False):
    # Heavy imports deferred here so torch/sentence-transformers only load when the flow runs
    from llama_index.core import (
        SimpleDirectoryReader,
        VectorStoreIndex,
        StorageContext,
        load_index_from_storage,
    )
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core.node_parser import SentenceSplitter

    embed = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if not force_rebuild and os.path.exists(os.path.join(persist_dir, "docstore.json")):
        storage = StorageContext.from_defaults(persist_dir=persist_dir)
        return load_index_from_storage(storage, embed_model=embed)

    docs = SimpleDirectoryReader(policies_dir).load_data()
    splitter = SentenceSplitter(chunk_size=800, chunk_overlap=120)
    nodes = splitter.get_nodes_from_documents(docs, show_progress=True)
    index = VectorStoreIndex(nodes, embed_model=embed)
    index.storage_context.persist(persist_dir=persist_dir)
    return index
