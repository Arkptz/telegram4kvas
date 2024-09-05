from pydantic_settings import BaseSettings
from pydantic import Field
import os
import tomllib
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_version_: str | None = None
    token: str = Field(description="API ключ бота, полученный от @BotFather")
    usernames: list[str] = Field(
        default_factory=list, description="Ваш логин(или несколько) в Телеграм", examples=["dnstkrv", "cowboy82"]
    )
    user_ids: list[int] = Field(
        default_factory=list,
        description="Или Ваш ID(или несколько) без кавычек, необязательно вводить и логин и ID, можно что-то одно",
    )
    base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @property
    def app_version(self) -> str:
        if self.app_version_ is None:
            try:
                with open(os.path.join(self.base_dir, "pyproject.toml"), "rb") as py_file:
                    data = tomllib.load(py_file)
                    self.app_version_ = data["tool"]["poetry"]["version"]  # type: ignore
            except FileNotFoundError:
                self.app_version_ = "0.0.1"
        return self.app_version_  # type: ignore


SETTINGS = Settings()  # type: ignore
