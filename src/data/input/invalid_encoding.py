from pathlib import Path


Path("invalid_encoding.json").write_bytes(b'{"prompt": "\xff"}')
