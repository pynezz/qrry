#!/usr/bin/env python3
"""
    QRry - quarry

    Detect URLs in a markdown files and insert inline QR codes below each link.

    For those that like physical copies of various documents,
    this simplifies looking up mentioned sources by scanning the code while you read.
"""

import re
import sys
import base64
import hashlib
import pathlib
from io import BytesIO
from pathlib import Path

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

def make_qr_b64(url: str) -> str:
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def process_markdown(text: str, qr_dir: Path) -> str:
    # Match markdown links [text](url) where url is http/https
    link_re = re.compile(r'\[([^\]]+)\]\((https?://[^)]+)\)')

    seen = {}
    lines = text.split('\n')
    out = []

    for line in lines:
        out.append(line)

        # Skip lines inside code blocks
        stripped = line.strip()
        if stripped.startswith('```'):
            # Toggle through until closing fence
            out.append(line) if line != out[-1] else None
            continue

        matches = link_re.findall(line)
        for label, url in matches:
            # Deduplicate: one QR per unique URL
            url_hash = hashlib.md5(b'' + url.encode()).hexdigest()[:10]
            if url_hash in seen:
                continue
            seen[url_hash] = url

            # Generate QR and save as image file
            qr_filename = f"qr-{url_hash}.png"
            qr_path = qr_dir / qr_filename

            if not qr_path.exists():
                qr = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_M,
                    box_size=4, border=2,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                )
                img.save(str(qr_path))

            # Insert image reference right after the line
            # Using a small HTML img for size control (Obsidian supports this)
            out.append(f'<img src="{qr_dir.name}/{qr_filename}" alt="QR: {url}" width="100" />')
            out.append('')

    return '\n'.join(out)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <markdown-file> [output-file]")
        sys.exit(1)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_stem(src.stem + "-qr")


    # Put QR images in a sibling directory
    qr_dir = dst.parent / f"{dst.stem}-qrcodes"
    qr_dir.mkdir(parents=True, exist_ok=True)
    # src = src.as_posix()
    # dst = dst.as_posix()

    try:
        text = src.read_text(encoding='utf-8', errors='ignore', newline='\n')
    except UnicodeEncodeError() as e:
        print(e)

    result = process_markdown(text, qr_dir)
    dst.write_text(result, encoding='utf-8', newline='\n')

    print(f"Written: {dst}")
    print(f"QR codes: {qr_dir}/")


if __name__ == "__main__":
    main()
