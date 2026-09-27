"""Internacionalizacao PT-BR/EN e preferencias persistidas."""
from __future__ import annotations
from . import config

STRINGS: dict[str, dict[str, str]] = {
    "pt": {
        "app_sub": "PT-BR  ·  otimizador geral",
        "user": "USUARIO", "pc": "PC", "os": "OS", "cpu": "CPU",
        "ram": "RAM", "gpu": "GPU", "admin": "ADMIN", "freed": "LIBERADO",
        "admin_yes": "sim", "admin_no": "nao",
        "path": "caminho",
        "help_bar": "↑↓ mover · ENTER selecionar · PgUp/PgDn pagina · ESC voltar",
        "pause": "pressione ENTER para voltar",
        "cancel": "cancelar", "choice": "escolha: ", "confirm": "confirmar?",
        "select_cat": "selecione uma categoria", "back": "Voltar",
        "apply_all": "APLICAR TUDO",
        "session_freed": "MB liberados nesta sessao",
        "bye": "ate a proxima.",
        "ok": "OK", "skipped": "--", "failed": "!!", "dry": "DRY",
        "fatal": "erro fatal",
        "no_admin_warn": "rodando sem privilegios de administrador",
        "no_admin_hint": "algumas otimizacoes de sistema podem falhar.",
        "no_admin_hint2": "para aplicar tudo: execute como admin.",
        "interrupted": "interrompido.",
        "sound_now": "som", "sound_on": "ligado", "sound_off": "desligado",
        "av_title": "DETECCAO DE ANTIVIRUS",
        "av_found": "antivirus detectado",
        "av_none": "nenhum antivirus detectado",
        "av_warn": "alguns tweaks podem ser bloqueados por ele",
        "menu_av": "ANTIVIRUS",
        "av_list": "listar antivirus detectado",
        "av_check_tweak": "checar se tweak especifico sera bloqueado",
        "av_checking": "checando se tweaks serao bloqueados",
        "av_ok": "tweaks de registro normalmente passam",
        "av_risky": "tweaks que mexem em servicos podem ser revertidos pelo AV",
        "menu_prefs": "PREFERENCIAS",
        "prefs_sound": "som de navegacao",
        "prefs_lang": "idioma",
        "prefs_mouse": "suporte a mouse",
        "enable": "ligado", "disable": "desligado",
        "menu_history": "HISTORICO",
        "history_show": "ver ultimos tweaks aplicados",
        "history_clear": "limpar historico",
        "history_empty": "historico vazio",
        "update_check": "checando atualizacao",
        "update_current": "voce esta na ultima versao",
        "update_available": "nova versao disponivel",
        "update_download": "baixar agora?",
        "update_hash_ok": "hash validado",
        "update_hash_bad": "hash invalido — download corrompido",
        "update_url_missing": "UPDATE_URL nao configurada",
        "update_url_invalid": "UPDATE_URL invalida — deve ser https",
        "menu_backup": "BACKUP DE CONFIG",
        "backup_export": "exportar config + registry",
        "backup_import": "importar config",
        "backup_done": "backup salvo",
        "backup_import_done": "config importada",
        "menu_experience": "EXPERIENCIA",
        "exp_anim": "Desativar animacoes e transparencia",
        "exp_widgets": "Desativar widgets / noticias / Copilot",
        "exp_explorer_open": "Explorer abrir em Este Computador",
        "exp_ext": "Mostrar extensoes de arquivo",
        "exp_ctx": "Menu de contexto classico (Win11)",
        "exp_start_rec": "Iniciar: remover recomendados",
        "exp_start_tips": "Iniciar: remover dicas e sugestoes",
        "exp_ads": "Desativar ID de publicidade",
        "exp_timeline": "Desativar historico de atividades",
        "exp_lockscreen": "Desativar tela de bloqueio",
        "exp_seconds": "Relogio com segundos",
        "exp_all": "APLICAR PACOTE EXPERIENCIA",
        "sec_title": "SEGURANCA",
        "sec_wipe": "apagar config + history do disco",
        "sec_status": "status de criptografia",
        "menu_ctx": "MENU DE CONTEXTO",
        "ctx_install": "Instalar menu de contexto no Explorer",
        "ctx_uninstall": "Remover menu de contexto",
        "ctx_installed": "menu instalado",
        "ctx_removed": "menu removido",
        "ctx_hint": "clique direito numa pasta ou no desktop",
        "ctx_win11_note": "no Win11 aparece em 'Mostrar mais opcoes'",
    },
    "en": {
        "app_sub": "EN  ·  general optimizer",
        "user": "USER", "pc": "PC", "os": "OS", "cpu": "CPU",
        "ram": "RAM", "gpu": "GPU", "admin": "ADMIN", "freed": "FREED",
        "admin_yes": "yes", "admin_no": "no",
        "path": "path",
        "help_bar": "↑↓ move · ENTER select · PgUp/PgDn page · ESC back",
        "pause": "press ENTER to return",
        "cancel": "cancel", "choice": "choice: ", "confirm": "confirm?",
        "select_cat": "select a category", "back": "Back",
        "apply_all": "APPLY ALL",
        "session_freed": "MB freed this session",
        "bye": "see you.",
        "ok": "OK", "skipped": "--", "failed": "!!", "dry": "DRY",
        "fatal": "fatal error",
        "no_admin_warn": "running without administrator privileges",
        "no_admin_hint": "some system tweaks may fail.",
        "no_admin_hint2": "to apply everything: run as admin.",
        "interrupted": "interrupted.",
        "sound_now": "sound", "sound_on": "on", "sound_off": "off",
        "menu_av": "ANTIVIRUS",
        "av_title": "ANTIVIRUS DETECTION",
        "av_found": "antivirus detected",
        "av_none": "no antivirus detected",
        "av_warn": "some tweaks may be blocked by it",
        "av_list": "list detected antivirus",
        "av_check_tweak": "check if a specific tweak will be blocked",
        "av_checking": "checking if tweaks will be blocked",
        "av_ok": "registry tweaks usually pass",
        "av_risky": "tweaks touching services may be reverted by AV",
        "menu_prefs": "PREFERENCES",
        "prefs_sound": "navigation sound",
        "prefs_lang": "language",
        "prefs_mouse": "mouse support",
        "enable": "on", "disable": "off",
        "menu_history": "HISTORY",
        "history_show": "view last applied tweaks",
        "history_clear": "clear history",
        "history_empty": "history empty",
        "update_check": "checking update",
        "update_current": "you are on the latest version",
        "update_available": "new version available",
        "update_download": "download now?",
        "update_hash_ok": "hash validated",
        "update_hash_bad": "invalid hash — corrupted download",
        "update_url_missing": "UPDATE_URL not set",
        "update_url_invalid": "UPDATE_URL invalid — must be https",
        "menu_backup": "CONFIG BACKUP",
        "backup_export": "export config + registry",
        "backup_import": "import config",
        "backup_done": "backup saved",
        "backup_import_done": "config imported",
        "menu_experience": "EXPERIENCE",
        "exp_anim": "Disable animations and transparency",
        "exp_widgets": "Disable widgets / news / Copilot",
        "exp_explorer_open": "Explorer opens in This PC",
        "exp_ext": "Show file extensions",
        "exp_ctx": "Classic context menu (Win11)",
        "exp_start_rec": "Start: remove recommendations",
        "exp_start_tips": "Start: remove tips and suggestions",
        "exp_ads": "Disable advertising ID",
        "exp_timeline": "Disable activity history",
        "exp_lockscreen": "Disable lock screen",
        "exp_seconds": "Clock with seconds",
        "exp_all": "APPLY EXPERIENCE PACK",
        "sec_title": "SECURITY",
        "sec_wipe": "wipe config + history from disk",
        "sec_status": "encryption status",
        "menu_ctx": "CONTEXT MENU",
        "ctx_install": "Install Explorer context menu",
        "ctx_uninstall": "Remove context menu",
        "ctx_installed": "menu installed",
        "ctx_removed": "menu removed",
        "ctx_hint": "right-click a folder or the desktop",
        "ctx_win11_note": "on Win11 it appears under 'Show more options'",
    },
}


def T(key: str) -> str:
    """Retorna a string traduzida para o idioma ativo."""
    lang = config.state.LANG
    return STRINGS.get(lang, STRINGS["pt"]).get(key, key)


def set_lang(code: str) -> None:
    """Define o idioma ativo e persiste em disco."""
    code = (code or "pt").lower()
    if code not in STRINGS:
        code = "pt"
    config.state.LANG = code
    config.PREFS["lang"] = code
    save_prefs()


def load_prefs() -> None:
    """Carrega preferencias do disco para o estado global."""
    from .security.dpapi import secure_read
    cfg = secure_read(config.CONFIG_FILE)
    for k in config.PREFS:
        if k in cfg:
            config.PREFS[k] = cfg[k]
    config.state.LANG = config.PREFS.get("lang", "pt")


def save_prefs() -> None:
    """Persiste as preferencias em disco cifrado."""
    from .security.dpapi import secure_write
    secure_write(config.CONFIG_FILE, config.PREFS)


def load_prefs_lang() -> None:
    """Sincroniza o idioma do state com PREFS."""
    config.state.LANG = config.PREFS.get("lang", "pt")
