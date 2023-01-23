from twitterGUI import *

class UserGUI(Ui_Form):
    def __init__(self,window):
        self.setupUi(window)
        


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = UserGUI(Form)
    Form.show()
    sys.exit(app.exec_())