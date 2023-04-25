from pathlib import Path
import base64
import cv2
import flet as ft
from flet import Text, Row, Container, Column


def main(page: ft.Page):
    page.window_width = 1920 * .8
    page.window_height = 1080 * .8
    page.title = 'Mask Visualizer'
    page.horizontal_alignment = 'top'
    page.vertical_alignment = 'spaceBetween'
    page.theme_mode = ft.ThemeMode.DARK
    theme_color = ft.colors.GREEN_300
    image_list = []
    annotation_list = []

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            set_to_light_theme()
        else:
            set_to_dark_theme()
        page.update()

    def full_screen_changed(e):
        page.window_full_screen = full_screen.value
        page.update()

    def always_on_top_changed(e):
        page.window_always_on_top = always_on_top.value
        page.update()

    def set_to_dark_theme():
        page.theme_mode = ft.ThemeMode.DARK
        theme_switch.label = 'Dark Mode'
        setting_tf.color = ft.colors.WHITE
        annotations_tf.color = ft.colors.WHITE

    def set_to_light_theme():
        page.theme_mode = ft.ThemeMode.LIGHT
        theme_switch.label = 'Light Mode'
        setting_tf.color = ft.colors.BLACK
        annotations_tf.color = ft.colors.BLACK

    def image_root_changed(e):
        image_root = Path(image_root_tf.value)
        if image_root.exists():
            ext = extension_selector.value
            image_list = list(image_root.glob(ext))
        else:
            print('Image root folder does not exist')
        num_img_ctnr.value = f'Number of Images: {len(image_list)}'

    def ann_root_changed(e):
        ann_root = Path(ann_root_tf.value)
        if ann_root.exists():
            annotation_list = list(ann_root.glob('*.json'))
        else:
            print('Annotation root folder does not exist')
        num_ann_ctnr.value = f'Number of Annotations: {len(annotation_list)}'

    def redraw(e):
        jpg_as_text = draw_image(int(resize_width.value),
                                 int(resize_height.value), image)
        image_view.src_base64 = jpg_as_text.decode()
        page.update()

    def draw_image(width, height, image):
        resized_image = cv2.resize(image, (width, height))
        _, buffer = cv2.imencode('.jpg', resized_image)
        jpg_as_text = base64.b64encode(buffer)
        return jpg_as_text

    theme_switch = ft.Switch(label='Dark Mode',
                             value=True,
                             active_color=theme_color,
                             on_change=change_theme)

    full_screen = ft.Switch(label="Full screen",
                            value=False,
                            active_color=theme_color,
                            on_change=full_screen_changed)
    always_on_top = ft.Switch(label="Always on top",
                              active_color=theme_color,
                              value=False,
                              on_change=always_on_top_changed)

    setting_tf = Text("Settings", color=ft.colors.WHITE, size=20)
    annotations_tf = Text('Annotations', color=ft.colors.WHITE, size=20)
    resize_width = ft.TextField(label='Resize width',
                                expand=1,
                                value=1280,
                                border_color=ft.colors.TRANSPARENT)
    resize_height = ft.TextField(label='Resize height',
                                 expand=1,
                                 value=720,
                                 border_color=ft.colors.TRANSPARENT)

    image_path = 'data/dummy_data.jpg'
    image = cv2.imread(image_path)

    jpg_as_text = draw_image(resize_width.value, resize_height.value, image)
    image_view = ft.Image(src_base64=jpg_as_text.decode(),
                          fit=ft.ImageFit.COVER,
                          border_radius=ft.border_radius.all(10),
                          expand=1)

    image_root_tf = ft.TextField(hint_text='Root images folder',
                                 height=48,
                                 border_color=ft.colors.TRANSPARENT,
                                 border_radius=ft.border_radius.all(5))
    ann_root_tf = ft.TextField(hint_text='Root annotations folder',
                               height=48,
                               border_color=ft.colors.TRANSPARENT,
                               border_radius=ft.border_radius.all(5))

    extension_selector = ft.Dropdown(width=8 * 28,
                                     border_color=ft.colors.TRANSPARENT,
                                     hint_text="Select image parttern",
                                     options=[
                                         ft.dropdown.Option("*.png"),
                                         ft.dropdown.Option("*.jpg"),
                                         ft.dropdown.Option("*/*.png"),
                                         ft.dropdown.Option("*/*.jpg"),
                                     ],
                                     on_change=lambda e: image_root_changed(e)
                                     if image_root_tf.value != '' else None)

    num_img_ctnr = ft.Text(f'Number of Images: {len(image_list)}')
    num_ann_ctnr = ft.Text(f'Number of Annotations: {len(annotation_list)}')

    div = Container(border=ft.border.all(1, ft.colors.GREY))
    left_arrow_btn = Container(width=56,
                               height=56,
                               border_radius=ft.border_radius.all(5),
                               content=ft.IconButton(
                                   height=56,
                                   width=56,
                                   icon=ft.icons.KEYBOARD_ARROW_LEFT_OUTLINED,
                                   bgcolor=theme_color,
                                   icon_color=ft.colors.BLACK87))

    right_arrow_btn = Container(width=56,
                                height=56,
                                border_radius=ft.border_radius.all(5),
                                alignment=ft.alignment.center_right,
                                content=ft.IconButton(
                                    height=56,
                                    width=56,
                                    bgcolor=theme_color,
                                    icon=ft.icons.KEYBOARD_ARROW_RIGHT_SHARP,
                                    icon_color=ft.colors.BLACK87))

    page.add(
        Row(vertical_alignment=ft.CrossAxisAlignment.START,
            expand=1,
            controls=[
                Container(
                    height=720,
                    width=1280,
                    alignment=ft.alignment.bottom_center,
                    content=ft.Stack(controls=[
                        image_view,
                        Container(
                            Column(expand=1,
                                   alignment="center",
                                   controls=[
                                       Row(
                                           alignment="spaceBetween",
                                           controls=[
                                               left_arrow_btn, right_arrow_btn
                                           ],
                                       )
                                   ]))
                    ]),
                    border_radius=ft.border_radius.all(10)),
                ft.VerticalDivider(width=1, color="grey"),
                Column(expand=1,
                       alignment='top',
                       controls=[
                           setting_tf,
                           Container(content=theme_switch),
                           Container(content=full_screen),
                           Container(content=always_on_top),
                           Row(vertical_alignment=ft.CrossAxisAlignment.CENTER,
                               controls=[resize_width, resize_height]),
                           ft.ElevatedButton(height=48,
                                             width=128,
                                             text="Re draw image",
                                             color=theme_color,
                                             on_click=redraw),
                           div,
                           Column(controls=[num_img_ctnr, num_ann_ctnr]),
                           div,
                           annotations_tf,
                       ])
            ]), div,
        Row(vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                Container(
                    expand=1,
                    content=image_root_tf,
                    border_radius=ft.border_radius.all(5),
                ), extension_selector,
                Container(
                    content=ft.IconButton(icon=ft.icons.IMAGE,
                                          height=48,
                                          width=48,
                                          icon_color=ft.colors.WHITE,
                                          on_click=image_root_changed),
                    bgcolor=theme_color,
                    border_radius=ft.border_radius.all(5),
                )
            ]),
        Row(vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                Container(
                    expand=1,
                    content=ann_root_tf,
                    border_radius=ft.border_radius.all(5),
                ),
                Container(
                    content=ft.IconButton(icon=ft.icons.ANNOUNCEMENT,
                                          height=48,
                                          width=48,
                                          icon_color=ft.colors.WHITE,
                                          on_click=ann_root_changed),
                    bgcolor=theme_color,
                    border_radius=ft.border_radius.all(5),
                )
            ]))

    page.update()


if __name__ == '__main__':
    ft.app(target=main)
