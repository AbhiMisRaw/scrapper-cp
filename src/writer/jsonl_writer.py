import aiofiles
import json
from pathlib import Path


class AsyncJsonlWriter:
    def __init__(
        self,
        output_dir: str,
        source_name: str,
        flush_every: int = 10,
        max_records: int = 10000,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.source_name = source_name
        self.flush_every = flush_every
        self.max_records = max_records

        self.file = None
        self.file_index = 1

        self.buffer = []
        self.record_count = 0

    async def start(self):
        await self._open_new_file()

    async def _open_new_file(self):
        if self.file:
            await self.file.flush()
            await self.file.close()

        file_path = self.output_dir / f"{self.source_name}_{self.file_index}.jsonl"
        self.file = await aiofiles.open(file_path, mode="w", encoding="utf-8")
        print("file has been opened")

        self.file_index += 1
        self.record_count = 0

    async def write(self, data: dict):
        line = json.dumps(data, ensure_ascii=False)
        self.buffer.append(line)
        self.record_count += 1

        if len(self.buffer) >= self.flush_every:
            await self.flush()

        if self.record_count >= self.max_records:
            await self._rotate()

    async def flush(self):
        if not self.buffer:
            return

        await self.file.write(("\n".join(self.buffer) + "\n"))
        self.buffer.clear()

    async def _rotate(self):
        await self.flush()
        await self._open_new_file()

    async def close(self):
        await self.flush()
        await self.file.close()
        print("file is written completly.")