# Development/ — Agent Guide

## Purpose

Build tooling, debug utilities, and platform-specific USD tools. This folder is not part of the
USD content library — it supports the development workflow for creating and validating content in
`schemas/` and `Features/`.

## Folder Layout

```
Development/
  build-development/    # Platform-specific USD tool distributions
    Windows-usdtools/   # Pre-built USD command-line tools for Windows
      2405/             # Tool version (year + month, e.g. 2405 = May 2024)
        all.zip         # Full tool package
        pythontools/    # usdzip and other Python-based USD tools
    screenShots/        # Development screenshots for documentation
    debug/              # Debug utilities and scripts
  debug/                # Debug notes and guides
    ReadMe.md           # How to use the debug tools
```

## Adding New Tools or Utilities

- Place platform-specific tool distributions under `build-development/<Platform>-usdtools/<version>/`.
- Use the version folder name format `YYMM` (e.g., `2405` for May 2024).
- Add a `ReadMe.md` in any new subfolder explaining what the tools are and how to use them.
- Commit with the message pattern:
  ```
  Development: add <tool or platform> <version>
  ```

## Debug Notes

See [`debug/ReadMe.md`](debug/ReadMe.md) for guidance on debugging USD file issues and using the
bundled diagnostic tools.
