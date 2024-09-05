from typing import Any
from pydantic import BaseModel, Field, validator
import asyncio
import re
from urllib.parse import parse_qs, urlparse
import aiofiles


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


def build_json_data(dict_result: dict[str, Any], routerip: str):
    user = User(
        id=re.sub("[\[|'|\]]", "", dict_result["id"]),
        flow=re.sub("[\[|'|\]]", "", dict_result["flow"]),
        publicKey=re.sub("[\[|'|\]]", "", dict_result["pbk"]),
        fingerprint=re.sub("[\[|'|\]]", "", dict_result["fp"]),
        serverName=re.sub("[\[|'|\]]", "", dict_result["sni"]),
        shortId=re.sub("[\[|'|\]]", "", dict_result["sid"]),
        spiderX=re.sub("[\[|'|\]]", "", dict_result["spx"]),
    )

    vnext = Vnext(
        address=re.sub("[\[|'|\]]", "", dict_result["server"]),
        port=int(re.sub("[\[|'|\]]", "", dict_result["port"])),
        users=[user],
    )

    outbound = Outbound(settings={"vnext": [vnext]})

    stream_settings = StreamSettings(
        network=re.sub("[\[|'|\]]", "", dict_result["type"]),
        security=re.sub("[\[|'|\]]", "", dict_result["security"]),
        realitySettings={
            "publicKey": user.public_key,
            "fingerprint": user.fingerprint,
            "serverName": user.server_name,
            "shortId": user.short_id,
            "spiderX": user.spider_x,
        },
        tcpSettings={"header": {"type": "none"}},
    )

    config = XRayConfig(inbounds=[Inbound(listen=str(routerip))], outbounds=[outbound])

    return config.model_dump_json()
