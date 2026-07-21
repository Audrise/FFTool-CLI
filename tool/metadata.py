from mutagen import File
from pathlib import Path

# index = None  → set tag to all songs
# index = int   → set tag just for one song

class MetadataEditor:
    SUPPORTED_EXT = {".flac", ".mp3", ".ogg", ".m4a", ".aac"} # more formats in next update!

    def __init__(self, target_path):
        self.target_path = Path(target_path)

        if not self.target_path.exists():
            raise FileNotFoundError("Path not found!")

        self.files = self._collect_files()

    def _collect_files(self):
        if self.target_path.is_file():
            return [self.target_path]

        files = []
        for ext in self.SUPPORTED_EXT:
            files.extend(self.target_path.rglob(f"*{ext}"))
        return sorted(files)

    # listing function
    def list_metadata(self, index=None):
        targets = self.files

        if index is not None:
            if index < 0 or index >= len(self.files):
                raise IndexError("Invalid song index")
            targets = [self.files[index]]

        result = {}

        for file in targets:
            audio = File(file, easy=False)
            if audio and audio.tags:
                result[str(file)] = dict(audio.tags)
            else:
                result[str(file)] = {}

        return result

    def set_tag(self, key, value, index=None):
        targets = self.files

        if index is not None:
            if index < 0 or index >= len(self.files):
                raise IndexError("Index lagu tidak valid")
            targets = [self.files[index]]

        for file in targets:
            audio = File(file, easy=False)
            if audio is None:
                continue

            if audio.tags is None:
                audio.add_tags()

            audio.tags[key] = value
            audio.save()

    def delete_tag(self, key, index=None):
        targets = self.files

        if index is not None:
            if index < 0 or index >= len(self.files):
                raise IndexError("Index lagu tidak valid")
            targets = [self.files[index]]

        for file in targets:
            audio = File(file, easy=False)
            if audio is None:
                continue

            if audio.tags and key in audio.tags:
                del audio.tags[key]
                audio.save()

    def clear_tags(self):
        for file in self.files:
            audio = File(file, easy=False)
            if audio and audio.tags:
                audio.tags.clear()
                audio.save()
