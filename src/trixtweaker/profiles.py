"""Perfis de otimizacao que combinam acoes."""
from __future__ import annotations
from .actions.cleanup import (
    act_delivery_optimization,
    act_dns,
    act_logs,
    act_prefetch,
    act_temp,
    act_thumbnails,
    act_wu_cache,
)
from .actions.discord import act_discord_optimize_all
from .actions.experience import (
    act_exp_ads,
    act_exp_anim,
    act_exp_explorer_open,
    act_exp_ext,
    act_exp_lockscreen,
    act_exp_seconds,
    act_exp_start_rec,
    act_exp_start_tips,
    act_exp_timeline,
    act_exp_widgets,
)
from .actions.games import (
    act_dvr,
    act_game_mode,
    act_gpu,
    act_nagle,
    act_prioridade,
    act_shaders,
    act_tcp,
)
from .actions.network import act_rede_reset
from .actions.performance import (
    act_animacoes,
    act_apps_bg,
    act_efeitos,
    act_energia,
    act_memoria,
    act_sysmain,
    act_telemetria,
)
from .actions.privacy import (
    act_priv_ads,
    act_priv_camera_mic,
    act_priv_cortana,
    act_priv_location,
)
from .ui.feedback import fail


def run_profile(name: str) -> bool:
    """Executa um perfil nomeado de otimizacao."""
    name = name.lower()
    if name == "gaming":
        for fn in (act_energia, act_game_mode, act_dvr, act_tcp, act_nagle,
                   act_prioridade, act_gpu, act_shaders):
            fn()
    elif name == "performance":
        for fn in (act_energia, act_telemetria, act_animacoes, act_efeitos,
                   act_sysmain, act_memoria, act_apps_bg):
            fn()
    elif name == "experience":
        for fn in (act_exp_anim, act_exp_widgets, act_exp_explorer_open,
                   act_exp_ext, act_exp_start_rec, act_exp_start_tips,
                   act_exp_ads, act_exp_timeline, act_exp_seconds):
            fn()
    elif name == "discord":
        act_discord_optimize_all()
    elif name == "cleanup":
        for fn in (act_temp, act_wu_cache, act_logs, act_dns, act_prefetch,
                   act_thumbnails, act_delivery_optimization):
            fn()
    elif name == "privacy":
        for fn in (act_priv_cortana, act_priv_ads, act_priv_location, act_priv_camera_mic):
            fn()
    elif name == "network":
        act_rede_reset()
    else:
        fail(f"perfil desconhecido: {name}")
        return False
    return True
