"""Registro central de acoes (fonte de verdade p/ --action)."""
from __future__ import annotations
from .cleanup import (
    act_dns,
    act_lixeira,
    act_logs,
    act_prefetch,
    act_temp,
    act_thumbnails,
)
from .discord import act_discord_optimize_all
from .experience import (
    act_exp_ads,
    act_exp_anim,
    act_exp_seconds,
    act_exp_start_tips,
    act_exp_timeline,
    act_exp_widgets,
)
from .games import act_shaders
from .performance import (
    act_animacoes,
    act_apps_bg,
    act_efeitos,
    act_energia,
    act_telemetria,
)
from .network import act_rede_reset
from .privacy import (
    act_priv_ads,
    act_priv_camera_mic,
    act_priv_cortana,
    act_priv_location,
)
from .. import config
from ..log import log
from ..security.sanitize import sanitize_log
from ..ui.feedback import emit

ACTIONS: dict[str, object] = {
    "temp": act_temp,
    "logs": act_logs,
    "dns": act_dns,
    "trash": act_lixeira,
    "lixeira": act_lixeira,
    "prefetch": act_prefetch,
    "thumbs": act_thumbnails,
    "shaders": act_shaders,
    "discord": lambda: act_discord_optimize_all(),
    "cleanup": lambda: [act_temp(), act_logs(), act_dns(),
                        act_lixeira(), act_prefetch()],
    "performance": lambda: [act_energia(), act_telemetria(), act_animacoes(),
                            act_efeitos(), act_apps_bg()],
    "experience": lambda: [act_exp_anim(), act_exp_widgets(),
                           act_exp_start_tips(), act_exp_ads(),
                           act_exp_timeline(), act_exp_seconds()],
    "privacy": lambda: [act_priv_cortana(), act_priv_ads(),
                        act_priv_location(), act_priv_camera_mic()],
    "network": lambda: [act_rede_reset(), act_dns()],
}


def run_action(action: str) -> int:
    """Executa acao direta em modo silencioso."""
    config.state.SILENT = True
    fn = ACTIONS.get(action)
    if not fn:
        config.state.SILENT = False
        emit(f"acao desconhecida: {action}")
        return 1
    try:
        fn()
        return 0
    except Exception as e:
        try:
            log(f"action {action} falhou: {sanitize_log(str(e))}")
        except Exception:
            pass
        return 1
