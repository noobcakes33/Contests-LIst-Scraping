import requests
from bs4 import BeautifulSoup
import json
import webbrowser
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QFormLayout, QGroupBox, QLabel, QScrollArea
import sys
from PyQt5 import QtGui, QtCore


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Contests"
        self.left = 500
        self.top = 50
        self.width = 950
        self.height = 800
        self.iconName = "panic.jpg"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        formLayout = QFormLayout()
        groupBox = QGroupBox("C-List")

        labelList = []
        buttonList = []

        contests = self.get_contests()

        for i in range(len(contests)):
            labelList.append(QLabel(
                "<b style='color:blue'>" + contests[i]["title"] + "</b>" +
                "<p>Start: " + contests[i]["start"] +
                "<br/>End : " + contests[i]["end"] +
                "<br/>Zone: " + contests[i]["zone"] + "</p>"))

            buttonList.append(QPushButton("\n" + "Enter Contest" + "\n\n" + "[" + contests[i]["location"] + "]" + "\n"))
            buttonList[i].setStyleSheet('QPushButton {color: red;}')
            formLayout.addRow(labelList[i], buttonList[i])
            url = contests[i]["url"]
            buttonList[i].clicked.connect(self.enter(url))

        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(900)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        self.setLayout(layout)
        self.show()

    def get_contests(self):
        URL = "https://clist.by/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='contests')
        contests_info = results.find_all('a', class_='data-ace')

        contests = []
        for c in contests_info:
            data = c
            data = str(data)
            try:
                data = "{" + data[data.index("'{") + 2: data.index("}'")].strip() + "}"
                json_data = json.loads(data)

                title = json_data["title"]
                url = json_data["desc"][5:]
                location = json_data["location"]
                start = json_data["time"]["start"]
                end = json_data["time"]["end"]
                zone = json_data["time"]["zone"]

                contest_info = {"title": title,
                                "url": url,
                                "location": location,
                                "start": start,
                                "end": end,
                                "zone": zone}

                contests.append(contest_info)
            except:
                pass
        return contests

    def enter(self, link):
        def enter_contest():
            webbrowser.open(link)

        return enter_contest


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
