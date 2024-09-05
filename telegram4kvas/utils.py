from pydantic import BaseModel, Field, validator
import asyncio
import re
from log import logger
from urllib.parse import parse_qs, urlparse
import aiofiles


async def run_command(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise Exception(f"Command failed: {stderr.decode()}")
    return stdout.decode().strip()


class User(BaseModel):
    id: str
    flow: str = ""
    encryption: str = "none"
    public_key: str = Field(..., alias="publicKey")
    fingerprint: str = Field(..., alias="fingerprint")
    server_name: str = Field(..., alias="serverName")
    short_id: str = Field("", alias="shortId")
    spider_x: str = Field(..., alias="spiderX")


class Vnext(BaseModel):
    address: str
    port: int
    users: list[User]


class StreamSettings(BaseModel):
    network: str
    security: str
    reality_settings: dict = Field(..., alias="realitySettings")
    tcp_settings: dict = Field({"header": {"type": "none"}}, alias="tcpSettings")


class Outbound(BaseModel):
    tag: str = "vless"
    protocol: str = "vless"
    settings: dict


class Inbound(BaseModel):
    listen: str
    port: int = 1081
    protocol: str = "socks"


class XRayConfig(BaseModel):
    log: dict = {"loglevel": "info"}
    routing: dict = {"rules": [], "domainStrategy": "AsIs"}
    inbounds: list[Inbound]
    outbounds: list[Outbound]


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
