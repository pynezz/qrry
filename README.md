# qrry - dead simple URL to QR conversion.

Detect URLs in a markdown files and insert inline QR codes below each link.

For those that like physical copies of various documents, this simplifies looking up mentioned sources by scanning the code while you read.

```shell
# Example markdown document written in Obsidian
$ qrry.py ~/notes/techstuff/os/ostree.md

Written: ~/notes/techstuff/os/ostree-qr.md
QR codes: ~/notes/techstuff/os/ostree-qr-qrcodes/
```

**Before**

<img width="591" height="90" alt="image" src="https://github.com/user-attachments/assets/a116a2fc-ecaa-4fc2-9dc6-edd62e6cf2e9" />

**After**

<img width="auto" height="178" alt="image" src="https://github.com/user-attachments/assets/8b13b4c3-b859-4a41-82ce-812534f13ccb" />

