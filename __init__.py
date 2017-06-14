import logging
import aiohttp

from opsdroid.matchers import match_regex, match_crontab
from opsdroid.message import Message


_LOGGER = logging.getLogger(__name__)


@match_regex(r'.*seal.*vault.*')
async def seal_the_vault(opsdroid, config, message):
    vault_url = config.get('vault-url', None)
    vault_token = config.get('vault-token', None)
    if vault_url is None or vault_token is None:
        await message.respond("No vault url and/or token has been specified in the config.")
        return

    seal_url = "{}/v1/sys/seal".format(config.get('vault-url'))
    seal_headers = {'X-Vault-Token': vault_token}
    async with aiohttp.ClientSession() as session:
        async with session.put(seal_url, headers=seal_headers) as resp:
            status = await resp.json()
            _LOGGER.debug(resp.status)
            if resp.status == 204:
                await message.respond("I sealed the vault.")
                if config.get("announce-on-seal", False):
                    await seal_status(opsdroid, config, None)
            elif resp.status == 403:
                await message.respond("Looks like I don't have permission to seal the vault.")
            else:
                await message.respond("Something unusual happened, the vault probably isn't sealed.")


@match_crontab('0 * * * *')
@match_regex(r'.*(seal|vault).*(status|sealed).*')
async def seal_status(opsdroid, config, message):
    announce_sealed, announce_unsealed = True, True
    if message is None:
        announce_sealed = config.get("announce-sealed", True)
        announce_unsealed = config.get("announce-unsealed", False)
        message = Message("",
                          None,
                          config.get("room", opsdroid.default_connector.default_room),
                          opsdroid.default_connector)
    vault_url = config.get('vault-url', None)
    if vault_url is None:
        await message.respond("No vault url has been specified in the config.")
        return

    status_url = "{}/v1/sys/seal-status".format(config.get('vault-url'))
    async with aiohttp.ClientSession() as session:
        async with session.get(status_url) as resp:
            status = await resp.json()
            if status["sealed"] and announce_sealed:
                await message.respond("The vault is sealed.")
            if not status["sealed"] and announce_unsealed:
                await message.respond("The vault is not sealed.")
