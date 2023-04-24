from pathlib import Path
import flet as ft


class MaskVisualizer(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.page.update()
        self.images = []

    def build(self):
        # image = ft.Image(src='a')
        self.tf_img_root = ft.TextField(hint_text='Root image folder',
                                        expand=True)
        self.tf_ann_root = ft.TextField(hint_text='Root Annotation folder',
                                        expand=True)

        lv = ft.ListView(height=400)
        for i in self.images[:100]:
            lv.controls.append(ft.Text(f"Image: {i}"))

        return ft.Column(controls=[
            lv,
            ft.Row(controls=[
                self.tf_img_root,
                ft.FloatingActionButton(icon=ft.icons.IMAGE,
                                        on_click=self.set_image_root)
            ]),
            ft.Row(controls=[
                self.tf_ann_root,
                ft.FloatingActionButton(icon=ft.icons.EDIT,
                                        on_click=self.set_ann_root)
            ])
        ])

    def set_image_root(self, e):
        self.images = list(Path(self.tf_img_root.value).glob('*.png'))

    def set_ann_root(self, e):
        self.images = list(Path(self.tf_ann_root.value).glob('*.png'))


def main(page: ft.Page):
    page.title = 'Mask Visualizer'
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 8
    # page.bgcolor = ft.colors.TRANSPARENT
    page.window_height = 700
    page.window_width = 700

    app = MaskVisualizer(page)
    page.add(app)


if __name__ == '__main__':
    ft.app(target=main)
