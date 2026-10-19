"""Update the photo gallery data from the folders in assets/photos/.

_data/photos.yml is the source of the gallery and may be edited by hand
(titles, descriptions, owners, order). This script only adds what is missing:

- a folder in assets/photos/ without an album entry -> new album at the top
  (slug = folder name, title/description/owner/owner_url empty)
- an image file without a photo entry -> new photo at the end of its album
  (sorted by file name, title/description empty); the album's "updated" date
  is set to today
- BMP and PNG files without transparency are converted to JPEG (the original
  file is replaced)
- missing thumbnails (assets/photos/<album>/thumbs/, longest side 400px) and
  missing image sizes are created
- the album page _albums/<slug>.html is created, and its title is kept in sync
  with photos.yml (the page shows the data from photos.yml)

Existing values are never changed. Entries whose file is missing are kept and
reported as a warning.

Usage (needs Pillow and PyYAML: pip install pillow pyyaml):
    python _tools/build_photos.py
"""
import json
import os
import sys
from datetime import date

import yaml
from PIL import Image

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOS_DIR = os.path.join(SITE, "assets", "photos")
DATA_FILE = os.path.join(SITE, "_data", "photos.yml")
ALBUM_PAGES_DIR = os.path.join(SITE, "_albums")
URL_PREFIX = "/assets/photos"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
THUMB_SIZE = 400
JPEG_QUALITY = 90        # BMP/PNG converted to JPEG
THUMB_QUALITY = 82

HEADER = """\
# Photo gallery (pages: /photos/ and /photos/<slug>/).
# May be edited by hand. Run _tools/build_photos.py after adding folders or
# images to assets/photos/; it adds missing albums, photos, thumbnails and sizes.
"""

ALBUM_KEYS = ["slug", "title", "description", "updated", "owner", "owner_url", "photos"]
PHOTO_KEYS = ["file", "thumb", "width", "height", "thumb_width", "thumb_height", "title", "description"]


def uses_transparency(im):
    """True if the image has at least one pixel that is not fully opaque."""
    if im.mode == "P" and "transparency" in im.info:
        im = im.convert("RGBA")
    if im.mode in ("RGBA", "LA"):
        return im.getchannel("A").getextrema()[0] < 255
    return False


def on_white(im):
    """Flatten transparency onto white (for JPEG output)."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.getchannel("A"))
        return bg
    return im.convert("RGB")


def to_path(url):
    return os.path.join(SITE, *url.strip("/").split("/"))


def convert_if_needed(path):
    """Convert BMP and opaque PNG to JPEG, replacing the file. Returns the (new) path."""
    stem, ext = os.path.splitext(path)
    if ext.lower() not in (".bmp", ".png"):
        return path
    with Image.open(path) as im:
        im.load()
        if ext.lower() == ".png" and uses_transparency(im):
            return path
        target = stem + ".jpg"
        if os.path.exists(target):
            print(f"  WARNING: {os.path.relpath(path, SITE)} not converted, {os.path.basename(target)} exists")
            return path
        on_white(im).save(target, "JPEG", quality=JPEG_QUALITY, optimize=True)
    os.remove(path)
    print(f"  converted {os.path.relpath(path, SITE)} -> {os.path.basename(target)}")
    return target


def complete_photo(photo, slug):
    """Add missing thumbnail and sizes to a photo entry. Returns False if the file is missing."""
    path = to_path(photo["file"])
    if not os.path.exists(path):
        print(f"  WARNING: {photo['file']} is missing")
        return False

    if not photo.get("thumb"):
        name = os.path.splitext(os.path.basename(path))[0] + ".jpg"
        photo["thumb"] = f"{URL_PREFIX}/{slug}/thumbs/{name}"
    thumb_path = to_path(photo["thumb"])

    needs_thumb = not os.path.exists(thumb_path)
    if needs_thumb or not photo.get("width") or not photo.get("height"):
        with Image.open(path) as im:
            photo["width"], photo["height"] = im.size
            if needs_thumb:
                thumb = on_white(im)
                thumb.thumbnail((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
                os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
                thumb.save(thumb_path, "JPEG", quality=THUMB_QUALITY, optimize=True)
                print(f"  thumbnail {photo['thumb']}")

    if not photo.get("thumb_width") or not photo.get("thumb_height"):
        with Image.open(thumb_path) as im:
            photo["thumb_width"], photo["thumb_height"] = im.size
    return True


def write_album_page(album):
    """Create or update _albums/<slug>.html. Only the title is stored there (for
    the browser tab and SEO tags), everything else comes from photos.yml."""
    slug = album["slug"]
    path = os.path.join(ALBUM_PAGES_DIR, slug + ".html")
    content = ("---\n"
               "# Generated by _tools/build_photos.py, edit _data/photos.yml instead\n"
               f"title: {json.dumps(album.get('title') or slug, ensure_ascii=False)}\n"
               "---\n")
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != content:
        os.makedirs(ALBUM_PAGES_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"  album page _albums/{slug}.html {'updated' if old else 'created'}")


def ordered(entry, keys):
    """Return entry with known keys in a fixed order, unknown keys kept at the end."""
    result = {k: entry.get(k, "") for k in keys}
    result.update({k: v for k, v in entry.items() if k not in keys})
    return result


def main():
    albums = []
    if os.path.exists(DATA_FILE):
        albums = yaml.safe_load(open(DATA_FILE, encoding="utf-8")) or []
    by_slug = {a["slug"]: a for a in albums}
    today = date.today().isoformat()

    folders = sorted(d for d in os.listdir(PHOTOS_DIR) if os.path.isdir(os.path.join(PHOTOS_DIR, d)))

    # New folders become new albums at the top
    new_albums = []
    for slug in folders:
        if slug not in by_slug:
            album = {"slug": slug, "title": "", "description": "", "updated": today,
                     "owner": "", "owner_url": "", "photos": []}
            new_albums.append(album)
            by_slug[slug] = album
            print(f"new album: {slug}")
    albums = new_albums + albums

    added = 0
    for album in albums:
        slug = album["slug"]
        album["photos"] = album.get("photos") or []
        folder = os.path.join(PHOTOS_DIR, slug)
        if not os.path.isdir(folder):
            print(f"WARNING: folder for album '{slug}' is missing")
            continue

        known = {os.path.normcase(to_path(p["file"])) for p in album["photos"] if p.get("file")}
        files = sorted(f for f in os.listdir(folder)
                       if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(IMAGE_EXTENSIONS))

        new_photos = 0
        for name in files:
            path = os.path.join(folder, name)
            if os.path.normcase(path) in known:
                continue
            path = convert_if_needed(path)
            if os.path.normcase(path) in known:
                continue
            album["photos"].append({"file": f"{URL_PREFIX}/{slug}/{os.path.basename(path)}",
                                    "title": "", "description": ""})
            new_photos += 1
            print(f"  new photo: {slug}/{os.path.basename(path)}")

        if new_photos:
            album["updated"] = today
            added += new_photos

        for photo in album["photos"]:
            complete_photo(photo, slug)
        write_album_page(album)
        album["photos"] = [ordered(p, PHOTO_KEYS) for p in album["photos"]]

    albums = [ordered(a, ALBUM_KEYS) for a in albums]
    for a in albums:
        a["updated"] = str(a["updated"])  # keep dates as strings in YAML

    with open(DATA_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(HEADER + "\n")
        yaml.safe_dump(albums, f, sort_keys=False, allow_unicode=True, width=1000)

    print(f"\n{len(albums)} albums, {sum(len(a['photos']) for a in albums)} photos "
          f"({len(new_albums)} new albums, {added} new photos)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(__doc__)
    main()
