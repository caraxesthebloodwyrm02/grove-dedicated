# Lo7 language prototypes

This directory holds the **three** Lo7 manifest service implementations that parity tests compare:

| Path | Role |
|------|------|
| [`python/src/light_of_the_seven/lo7/`](python/src/light_of_the_seven/lo7/) | Python `lo7-manifest` / `lo7-heatmap` (Hatch package entry still uses `light_of_the_seven.lo7` via symlink from `src/light_of_the_seven/lo7`). |
| [`rust/`](rust/) | Standalone Cargo **workspace** for `lo7-manifest-service` only (`cargo build -p lo7-manifest-service` from this `rust/` directory). |
| [`go/lo7_manifest_service/`](go/lo7_manifest_service/) | Go binary; `go build` from that directory. |

## Git branch convention (hub + per-language)

Use a **central integration branch** for the batch, plus **topic branches** that can diverge per prototype:

1. **`feature/lo7-prototype-hub`** — default integration branch: all three prototypes land here before `main` / `develop`.
2. **`feature/lo7-prototype-python`** — work that touches only `prototype/python/` (and the `src/.../lo7` symlink if needed).
3. **`feature/lo7-prototype-rust`** — work under `prototype/rust/` only.
4. **`feature/lo7-prototype-go`** — work under `prototype/go/` only.

Create the hub branch first, **make at least one commit** (Git cannot create additional named branches until the repository has an initial commit), then add branch pointers:

```bash
git checkout -b feature/lo7-prototype-hub
# … commit …
git branch feature/lo7-prototype-python
git branch feature/lo7-prototype-rust
git branch feature/lo7-prototype-go
```

Use **merge PRs** into `feature/lo7-prototype-hub`, then one PR from hub to `develop` / `main`. For parallel checkouts, use **`git worktree add`** on the per-language branches.

If this tree lives inside a **parent monorepo** (for example `grove`), create those branches at the **parent repository root** and commit with a pathspec such as `archive/light_of_the_seven/…`. Do **not** run `git init` here unless you intend a separate Lo7-only repository.

## Windows note

The Python layout uses a **symlink** `src/light_of_the_seven/lo7` → `prototype/python/.../lo7`. Enable `git config core.symlinks true` or clone on a filesystem that supports symlinks; otherwise duplicate the tree or adjust Hatch `packages` to point at `prototype/python/src` only.
