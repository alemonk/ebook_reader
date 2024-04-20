from PySide6.QtCore import Qt

class KeyPressHandler:
    def __init__(self, widget):
        self.widget = widget

    def handle_key_press(self, event):

        print('--------------------------------------------------------------------------------')
        print(self.widget.objectName())

        # if event.key() == Qt.Key_Up:
        #     if self.widget.objectName() == 'HOME_MENU':
        #         print('scroll_up()')
        #         self.widget.scroll_up()
        #     else:
        #         print('show_previous()')
        #         self.widget.show_previous()

        # if event.key() == Qt.Key_Down:
        #     if self.widget.objectName() == 'HOME_MENU':
        #         print('scroll_down()')
        #         self.widget.scroll_down()
        #     else:
        #         print('show_next()')
        #         self.widget.show_next()

        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     print('select_item()')
        #     self.widget.select_item()

        # if event.key() == Qt.Key_Escape:
        #     print('close()')
        #     self.widget.close()
        
        if event.key() == Qt.Key_D:
            self.widget.show_next()
        if event.key() == Qt.Key_A:
            self.widget.show_previous()
        if event.key() == Qt.Key_Up:
            self.widget.scroll_up()
        if event.key() == Qt.Key_Down:
            self.widget.scroll_down()
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.widget.select_item()
        if event.key() == Qt.Key_Escape:
            self.widget.close()

        print('--------------------------------------------------------------------------------')
