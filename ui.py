import flet as ft

# Константы
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
PRIMARY_BACKGROUND_COLOR = "#181A25"
SECONDARY_BACKGROUND_COLOR = "#13151E"
BORDER_COLOR = "#303241"


class NavigationDrawer(ft.NavigationDrawer):
    def __init__(self, on_select):
        super().__init__(
            indicator_color=SECONDARY_BACKGROUND_COLOR,
            controls=self.create_drawer_items(),
            bgcolor=SECONDARY_BACKGROUND_COLOR
        )
        self.on_select = on_select

    def create_drawer_items(self):
        items = []
        destinations = [
            (ft.icons.HOME, "Home Page"),
            (ft.icons.ALARM, "Alarm"),
            (ft.icons.WB_SUNNY, "Weather"),
            (ft.icons.EVENT, "Calendar"),
            (ft.icons.CALENDAR_VIEW_DAY, "Schedule"),
            (ft.icons.TIMER, "Timer"),
            (ft.icons.ADD, "Add")
        ]
        for icon, label in destinations:
            items.append(self.create_drawer_item(icon, label))
            items.append(ft.Divider(thickness=2))
        return items

    @staticmethod
    def create_drawer_item(icon, label):
        return ft.NavigationDrawerDestination(icon=icon, selected_icon=icon, label=label)

    def open_drawer(self, e):
        self.open = True
        self.update()


class ChatWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tabs = []
        self.tab_content = []
        self.create_tabs()
        self.chat_interface = self.create_chat_interface()

    def create_tabs(self):
        for i in range(3):
            tab = ft.Container(
                content=ft.Text(f"Tab {i + 1}"),
                alignment=ft.alignment.center,
                width=140,
                height=60,
                bgcolor=SECONDARY_BACKGROUND_COLOR,
                border_radius=ft.BorderRadius(20, 20, 0, 0),
                border=ft.border.all(2, BORDER_COLOR),
                data=i,
                on_click=self.on_tab_click,
            )
            self.tabs.append(tab)

            content = ft.Container(
                content=ft.Text(f"Content for Tab {i + 1}", bgcolor="blue"),
                height=550,
                width=1250,
                margin=ft.margin.only(top=58),
                padding=ft.padding.all(20),
                border=ft.border.all(2, BORDER_COLOR),
                bgcolor=SECONDARY_BACKGROUND_COLOR,
                border_radius=ft.border_radius.all(20),
                visible=False
            )
            self.tab_content.append(content)

        self.set_active_tab(0)

    def on_tab_click(self, e):
        active_tab = int(e.control.data)
        self.set_active_tab(active_tab)

    def set_active_tab(self, active_tab: int):
        for idx, tab in enumerate(self.tabs):
            if idx == active_tab:
                tab.bgcolor = SECONDARY_BACKGROUND_COLOR
                tab.border.bottom = None
                tab.border_radius = ft.BorderRadius(20, 20, 0, 0)
            else:
                tab.bgcolor = SECONDARY_BACKGROUND_COLOR
                tab.border = ft.border.all(2, BORDER_COLOR)
            self.tab_content[idx].visible = idx == active_tab
        self.page.update()

    def create_chat_interface(self) -> ft.Stack:
        tab_bar = ft.Container(ft.Row(self.tabs, spacing=50), left=50)
        chat = ft.Stack([ft.Stack(self.tab_content), tab_bar])
        return chat


class VoiceAssistantApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_ui()

    def setup_ui(self):
        self.page.title = "Voice Assistant"
        self.page.theme_mode = "dark"
        self.page.bgcolor = PRIMARY_BACKGROUND_COLOR
        self.page.window_width = WINDOW_WIDTH
        self.page.window_height = WINDOW_HEIGHT

        self.drawer = NavigationDrawer(self.on_drawer_select)
        self.page.drawer = self.drawer

        self.chat_window = ChatWindow(self.page)
        all_page = ft.Stack(
            controls=[
                ft.Container(
                    content=ft.IconButton(ft.icons.MENU, on_click=self.page.drawer.open_drawer),
                    top=0,
                    left=0,
                    width=50,
                    height=50,
                ),
                ft.Container(
                    content=self.chat_window.chat_interface,
                    top=60,
                    left=140
                )
            ],
            width=self.page.window_width,
            height=self.page.window_height
        )
        self.page.add(all_page)

    def on_drawer_select(self, e):
        pass

    def main(self):
        self.page.update()


def main(page: ft.Page):
    app = VoiceAssistantApp(page)
    app.main()


if __name__ == '__main__':
    ft.app(target=main, view=ft.WEB_BROWSER)
