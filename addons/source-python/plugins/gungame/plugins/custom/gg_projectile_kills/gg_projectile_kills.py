# ../gungame/plugins/custom/gg_projectile_kills/gg_projectile_kills.py

"""Plugin used to cause projectiles to be 1 hit kills."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPreHook
from memory import make_object
from weapons.manager import weapon_manager

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import (
    GunGameMatchStatus,
    GunGameRoundStatus,
    GunGameStatus,
)
from gungame.core.weapons.groups import grenade_weapons

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_projectile_weapons = {
    k for k, v in weapon_manager.projectiles.items() if v in grenade_weapons
}


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, "on_take_damage")
@EntityPreHook(EntityCondition.is_human_player, "on_take_damage")
def _pre_take_damage(stack_data):
    """Set player health/armor to allow projectile kill."""
    if (
        GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE or
        GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE
    ):
        return

    take_damage_info = make_object(TakeDamageInfo, stack_data[1])
    attacker = Entity(take_damage_info.attacker)
    if attacker.classname != "player":
        return

    victim = make_object(Entity, stack_data[0])
    if (
        victim.team_index == attacker.team_index and
        "gg_ffa" not in gg_plugin_manager
    ):
        return

    classname = Entity(take_damage_info.weapon).classname
    if classname not in _projectile_weapons:
        return

    attacker = player_dictionary.from_index(attacker.index)
    if weapon_manager[classname].basename != attacker.level_weapon:
        return

    victim.health = 1
    victim.armor = 0
