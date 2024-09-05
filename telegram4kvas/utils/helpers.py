from pydantic import BaseModel, Field, validator
import asyncio
import re
from urllib.parse import parse_qs, urlparse
import aiofiles
from .models import build_json_data
import logging

logger = logging.getLogger("helpers")


async def run_command(cmd: str | bytes):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode()}")
    return stdout.decode().strip()


def clean_string(text: str) -> str:
    return (
        text.replace("-", "")
        .replace("[33m", "")
        .replace("[m", "")
        .replace("[1;32m", "")
        .replace("[1;31m", "")
        .replace("[7D", "")
        .replace("[8D", "")
        .replace("[10D", "")
        .replace("[9D", "")
        .replace("[11D", "")
        .replace("[6D", "")
        .replace("[12D", "")
        .replace("[1;31m", "")
        .replace("[36m", "")
        .replace("[14D", "")
        .replace("[1;37m", "")
    )


def clean_string_interfaces(text: str) -> str:
    return (
        text.replace("-", "")
        .replace("[36m", "")
        .replace("[m", "")
        .replace("[8D", "")
        .replace("[1;32m", "")
        .replace("[9D", "")
        .replace("[1;31m", "")
    )


async def vless(url):
    try:
        logger.info("Creating XRay config from VLESS URL")
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL provided")

        dict_str = parse_qs(parsed_url.query)
        dict_netloc = {
            "id": re.split("@|:|\n", parsed_url.netloc)[0],
            "server": re.split("@|:|\n", parsed_url.netloc)[1],
            "port": re.split("@|:|\n", parsed_url.netloc)[2],
        }
        dict_result = {**dict_str, **dict_netloc}

        get_routerip = '/opt/sbin/ip a | grep ": br0:" -A4 | grep "inet " | tr -s " " | cut -d" " -f3 | cut -d"/" -f1'
        routerip = await run_command(get_routerip)

        json_data = build_json_data(dict_result, routerip)

        async with aiofiles.open("/opt/etc/xray/config.json", "w") as file:
            await file.write(json_data)
    except ValueError as e:
        logger.error("Invalid URL: %s", str(e))
    except Exception as e:
        logger.exception("Error in vless function: %s", str(e))


async def scan_interfaces(param="Q"):
    try:
        logger.info("Scanning interfaces with parameter: %s", param)
        if param == "no_shadowsocks":
            command = f'echo "Q" | kvas vpn set | grep -v "shadowsocks" | grep "Интерфейс"'
        else:
            command = f'echo "{param}" | kvas vpn set | grep "Интерфейс"'

        output = await run_command(command)
        output_clean = clean_string_interfaces(output)
        return output_clean
    except Exception as e:
        logger.exception("Error during interface scanning: %s", str(e))
        return "Ошибка при сканировании интерфейсов"
