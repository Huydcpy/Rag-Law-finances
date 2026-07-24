from pathlib import Path
from llama_index.core import SimpleDirectoryReader

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

documents = SimpleDirectoryReader(
    input_dir=str(RAW_DIR),
    recursive=True,
).load_data()

print(f"Loaded {len(documents)} documents")