from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from enum import StrEnum


class CallbackButtons(StrEnum):
    host_manage = "host_manage"
    connects_manage = "connects_manage"
    service = "service"

    add_host = "add_host"
    delete_host = "delete_host"
    list_hosts = "list_hosts"
    clear_hosts_list = "clear_hosts_list"
    import_hosts = "import_hosts"
    export_hosts = "export_hosts"

    launch_test = "launch_test"
    launch_debug = "launch_debug"
    launch_reset = "launch_reset"
    reboot_router = "reboot_router"
    terminal = "terminal"
    update_bot = "update_bot"

    interface_list = "interface_list"
    interface_change = "interface_change"
    install_xray = "install_xray"
    delete_xray = "delete_xray"


class Keyboards:
    @classmethod
    def main_menu(
        cls,
    ):
        build = InlineKeyboardBuilder()
        build.add(
            InlineKeyboardButton(
                text="Управление хостами",
                callback_data=CallbackButtons.host_manage.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Управление подключениями",
                callback_data=CallbackButtons.connects_manage.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Сервис",
                callback_data=CallbackButtons.service.value,
            )
        )
        build.adjust(1)
        return build.as_markup()

    @classmethod
    def host_manage_menu(
        cls,
    ):
        build = InlineKeyboardBuilder()
        build.add(
            InlineKeyboardButton(
                text="Добавить хост",
                callback_data=CallbackButtons.add_host.value,
            )
        )

        build.add(
            InlineKeyboardButton(
                text="Удалить хост",
                callback_data=CallbackButtons.delete_host.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Список хостов",
                callback_data=CallbackButtons.list_hosts.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Очистить список",
                callback_data=CallbackButtons.clear_hosts_list.value,
            )
        )

        build.add(
            InlineKeyboardButton(
                text="Импорт",
                callback_data=CallbackButtons.import_hosts.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Экспорт",
                callback_data=CallbackButtons.export_hosts.value,
            )
        )
        build.adjust(1)
        return build.as_markup()

    @classmethod
    def service_message_menu(cls):
        build = InlineKeyboardBuilder()
        build.add(
            InlineKeyboardButton(
                text="Запустить test",
                callback_data=CallbackButtons.launch_test.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Запустить debug",
                callback_data=CallbackButtons.launch_debug.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Запустить reset",
                callback_data=CallbackButtons.launch_reset.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Перезагрузить роутер",
                callback_data=CallbackButtons.reboot_router.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Терминал",
                callback_data=CallbackButtons.terminal.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Обновить бота",
                callback_data=CallbackButtons.update_bot.value,
            )
        )
        build.adjust(1)
        return build.as_markup()

    @classmethod
    def connection_menu(
        cls,
    ):
        build = InlineKeyboardBuilder()
        build.add(
            InlineKeyboardButton(
                text="Список интерфейсов",
                callback_data=CallbackButtons.interface_list.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Смена интерфейсов",
                callback_data=CallbackButtons.interface_change.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Установить XRay",
                callback_data=CallbackButtons.install_xray.value,
            )
        )
        build.add(
            InlineKeyboardButton(
                text="Удалить XRay",
                callback_data=CallbackButtons.delete_xray.value,
            )
        )
        build.adjust(1)
        return build.as_markup()
