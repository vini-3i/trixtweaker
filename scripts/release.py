import hashlib
import re
import subprocess
import sys
from pathlib import Path

VERSION = "0.47.0"
USER = "vini-3i"
REPO = "trixtweaker"
ENTRY = "trixtweaker.py"
EXE_NAME = "TrixTweaker.exe"
ICON = "trix.ico"


def run(cmd, check=True):
    """Executa comando de shell."""
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)


def sync_version(root: Path):
    """Sincroniza VERSION no config e entrypoint."""
    cfg = root / "src" / "trixtweaker" / "config.py"
    if cfg.exists():
        src = cfg.read_text(encoding="utf-8")
        src = re.sub(r'VERSION = "[^"]+"', f'VERSION = "{VERSION}"', src)
        cfg.write_text(src, encoding="utf-8")
    pp = root / "pyproject.toml"
    if pp.exists():
        src = pp.read_text(encoding="utf-8")
        src = re.sub(r'version = "[^"]+"', f'version = "{VERSION}"', src, count=1)
        pp.write_text(src, encoding="utf-8")
    print(f"[ok] VERSION = {VERSION}")


def main():
    """Build + release + version.txt."""
    root = Path(__file__).resolve().parent.parent
    sync_version(root)
    cmd = [sys.executable, "-m", "PyInstaller", "--onefile", "--console",
           "--clean", "--uac-admin", "--paths", "src", "--name", "TrixTweaker"]
    if ICON and (root / ICON).exists():
        cmd += ["--icon", ICON]
    cmd += [ENTRY]
    run(cmd, check=True)
    exe = root / "dist" / EXE_NAME
    if not exe.exists():
        print("[erro] exe nao gerado")
        return
    h = hashlib.sha256()
    with open(exe, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    sha = h.hexdigest()
    print(f"[ok] sha256 = {sha}")
    tag = f"v{VERSION}"
    url = f"https://github.com/{USER}/{REPO}/releases/download/{tag}/{EXE_NAME}"
    r = run(["gh", "release", "create", tag, str(exe), "--title", f"TrixTweaker {VERSION}",
             "--notes", f"Release {VERSION}", "--repo", f"{USER}/{REPO}"], check=False)
    if r.returncode != 0:
        print("[aviso] gh falhou — crie o release manualmente no GitHub")
        print(f"        url esperada: {url}")
    vt = root / "version.txt"
    vt.write_text(f"{VERSION}\n{url}\nsha256:{sha}\nnotas: release {VERSION}\n", encoding="utf-8")
    print("[ok] version.txt atualizado")
    run(["git", "add", "version.txt", "pyproject.toml", "src/trixtweaker/config.py"], check=False)
    run(["git", "commit", "-m", f"release {VERSION}"], check=False)
    run(["git", "push"], check=False)
    print(f"\n[pronto] release {VERSION}")
    print(f"raw: https://raw.githubusercontent.com/{USER}/{REPO}/refs/heads/main/version.txt")


if __name__ == "__main__":
    main()
