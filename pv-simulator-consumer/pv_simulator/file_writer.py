import aiofiles
from aiocsv import AsyncWriter


class FileWriter:
    """
    CSV file writer
    """

    def __init__(self, file_path):
        self._file_path = file_path

    async def write_data(self, data):
        async with aiofiles.open(self._file_path, mode="a", newline="") as file:
            csv_writer = AsyncWriter(file)
            await csv_writer.writerow(data)
