# Certificate Branding Assets

Drop your files here to brand every generated certificate automatically —
no code changes needed:

- `university_logo.png` — your university/college logo (transparent background
  recommended). Shown centered at the top of every certificate.
- `authority_signature.png` — a scanned or transparent-background signature
  image. Shown above the signature line at the bottom of every certificate.

Both are optional. If a file isn't here, that certificate section simply
falls back gracefully (no logo, or just the printed name/title under an
empty line) — nothing breaks.

Also edit these two lines in `config.py` to set the printed name/title under
the signature line:

    SIGNATORY_NAME = "[Enter Signatory Name]"
    SIGNATORY_TITLE = "Course Coordinator, Programming with Python"
