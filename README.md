# TrixTweaker

Otimizador geral do Windows (PT-BR / EN). Navegação por setas, menu de contexto Win10 + Win11, sem dependências externas — stdlib puro.

## Árvore

```
trixtweaker/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .editorconfig
├── conftest.py
├── trixtweaker.py                 # entrypoint fino — chama cli.main()
├── src/
│   └── trixtweaker/
│       ├── __init__.py
│       ├── __main__.py            # python -m trixtweaker
│       ├── cli.py                 # argparse: --action/--profile/--install-ctx
│       ├── config.py              # VERSION, paths, WORKDIR, State
│       ├── i18n.py                # STRINGS, T(), prefs
│       ├── log.py                 # log, hist_add/get, cleanup_old_logs
│       ├── security/
│       │   ├── dpapi.py           # dpapi_encrypt/decrypt, secure_read/write
│       │   └── sanitize.py        # safe_path, sanitize_log
│       ├── system/
│       │   ├── info.py            # sys_info, is_admin, elevate
│       │   ├── registry.py        # reg_set/backup/exists/delete/enum
│       │   ├── process.py         # run, popen, service_exists
│       │   └── av.py              # detect_av, av_is_active
│       ├── ui/
│       │   ├── ansi.py            # cores, set_title, clear
│       │   ├── screen.py          # Screen, menu_pick, read_key
│       │   ├── feedback.py        # spin/ok/fail/info/emit/pause/confirm
│       │   ├── beep.py            # beep()
│       │   └── breadcrumb.py      # crumb_push/pop/str
│       ├── actions/               # tweaks por domínio (sem lógica de menu)
│       │   ├── performance.py, games.py, discord.py, cleanup.py
│       │   ├── network.py, privacy.py, experience.py, startup.py
│       │   ├── system_ops.py, context_menu.py
│       ├── menus/                 # loops menu_pick que chamam actions/
│       │   ├── main_menu.py, performance.py, games.py, discord.py
│       │   ├── experience.py, cleanup.py, network.py, privacy.py
│       │   ├── startup.py, system.py, av.py, history.py
│       │   ├── prefs.py, security.py, context.py
│       ├── profiles.py            # run_profile
│       └── update.py              # check_update + download
├── tests/
│   ├── test_dpapi.py, test_registry.py, test_i18n.py
│   ├── test_sanitize.py, test_actions_smoke.py
└── scripts/
    ├── release.py, install_menu.py, build.ps1
```

## Instalação

```powershell
pip install -e .
```

## Uso

```powershell
python trixtweaker.py                 # menu interativo
python -m trixtweaker                 # idem
python trixtweaker.py --version
python trixtweaker.py --action cleanup --silent
python trixtweaker.py --profile gaming
python trixtweaker.py --lang en
python trixtweaker.py --install-ctx   # como admin
python trixtweaker.py --uninstall-ctx
python trixtweaker.py --dry-run
```

Ações diretas (`--action`): `temp logs dns trash prefetch thumbs shaders discord cleanup performance experience privacy network`.
Perfis (`--profile`): `gaming performance experience discord cleanup privacy network`.

## Build

```powershell
scripts/build.ps1
# ou:
pyinstaller --onefile --console --clean --uac-admin --paths src --name TrixTweaker --icon=trix.ico trixtweaker.py
```

Release (build + GitHub release + version.txt):

```powershell
python scripts/release.py
```

## Testes

```powershell
python -m pytest tests/ -q
```

## Regras de contribuição

- Adicionar ação nova = editar um arquivo em `actions/` + registrar no `ACTIONS` em `actions/__init__.py`.
- Toda saída visível passa por `ui.feedback`. Todo `subprocess` passa por `system.process`. Todo `winreg` passa por `system.registry`. Todo DPAPI passa por `security.dpapi`.
- Estado mutável vive em `config.state` / `config.PREFS`.
