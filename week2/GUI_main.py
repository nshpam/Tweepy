from twitterGUI import *
import sys
class UserGUI(Ui_Form):
    def __init__(self,window):
        self.setupUi(window)
        
app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()

# Create an instance of our app
ui = UserGUI(Form)
# Show the window and start the app
Form.show()
app.exec_() 