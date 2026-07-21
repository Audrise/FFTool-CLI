from mutagen.flac import FLAC, Picture
from mutagen.mp4 import MP4, MP4Cover
from mutagen.mp3 import MP3
from mutagen.id3 import APIC

class CoverArtEditor:
    def __init__(self, fileobj):
        self.fileobj = fileobj

        if isinstance(fileobj, str):
            self.filepath = fileobj
        else:
            self.filepath = (
                getattr(fileobj, "filepath", None)
                or getattr(fileobj, "name", None)
                or (fileobj.get("filepath") if isinstance(fileobj, dict) else None)
                or (fileobj.get("file") if isinstance(fileobj, dict) else None)
            )

        if not self.filepath:
            raise ValueError(f"Cannot determine file path from {fileobj}")

    def add_cover(self, image_path, mime="image/jpeg"):
        ext = self.filepath.lower().split(".")[-1]

        if ext == "flac":
            audio = FLAC(self.filepath)
            pic = Picture()
            pic.type = 3
            pic.mime = mime
            with open(image_path, "rb") as img:
                pic.data = img.read()
            audio.clear_pictures()
            audio.add_picture(pic)
            audio.save()

        elif ext == "mp3":
            audio = MP3(self.filepath)
            if audio.tags is None:
                audio.add_tags()
            with open(image_path, "rb") as img:
                audio.tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover", data=img.read()))
            audio.save()

        elif ext in ["m4a", "aac"]:
            audio = MP4(self.filepath)
            with open(image_path, "rb") as img:
                audio["covr"] = [MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)]
            audio.save()

        else:
            raise ValueError(f"Unsupported format: {ext}")

    def remove_cover(self):
        ext = self.filepath.lower().split(".")[-1]

        if ext == "flac":
            audio = FLAC(self.filepath)
            audio.clear_pictures()
            audio.save()

        elif ext == "mp3":
            audio = MP3(self.filepath)
            if audio.tags:
                audio.tags.delall("APIC")
                audio.save()

        elif ext in ["m4a", "aac"]:
            audio = MP4(self.filepath)
            if "covr" in audio:
                del audio["covr"]
                audio.save()