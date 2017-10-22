# ../gungame/plugins/custom/gg_projectile_kills/gg_projectile_kills.py

"""Plugin used to cause projectiles to be 1 hit kills."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-package
from configobj import ConfigObj

# Source.Python
from core import GAME_NAME
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPreHook
from memory import make_object

# GunGame
from gungame.core.paths import GUNGAME_DATA_PATH
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_ini_file = GUNGAME_DATA_PATH / info.name + '.ini'
_projectile_weapons = ConfigObj(_ini_file).get(GAME_NAME, [])


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'on_take_damage')
@EntityPreHook(EntityCondition.is_human_player, 'on_take_damage')
def _pre_take_damage(stack_data):
    """Set player health/armor to allow projectile kill."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    take_damage_info = make_object(TakeDamageInfo, stack_data[1])
    attacker = Entity(take_damage_info.attacker)
    if attacker.classname != 'player':
        return

    victim = make_object(Entity, stack_data[0])
    if victim.team == attacker.team and 'gg_ffa' not in gg_plugin_manager:
        return

    if Entity(take_damage_info.weapon).classname not in _projectile_weapons:
        return

    victim.health = 1
    victim.armor = 0
    take_damage_info.damage = max(1, take_damage_info.damage)
