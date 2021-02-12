import sys
import functools
import os
import random
import ctypes
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from pytube import YouTube
from urllib import parse
from googleapiclient.discovery import build  # API를 호출할 함수 제작
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtMultimedia
from PyQt5.QtCore import QDir, QUrl


form_class = uic.loadUiType("PyEx_v3.ui")[0]
form_class_loading = uic.loadUiType("loading.ui")[0]


counter = 0

# 화면을 띄우는데 사용되는 Class 선언


class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 윈도우 타이틀
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("파이익스")
        self.setWindowIcon(QIcon("icon/youtube.png"))

        # 열기
        self.show()

        # 초기 show 이벤트
        self.tab_one()

        # 윈도우 사이즈 고정
        self.setFixedSize(1190, 790)

        # 이미지 세팅
        self.main_play.setPixmap(QtGui.QPixmap("icon\play-button.png"))
        self.main_play.setContentsMargins(59, 59, 59, 59)

        self.main_down.setPixmap(QtGui.QPixmap("icon\cloud-computing.png"))
        self.main_down.setContentsMargins(59, 59, 59, 59)

        self.main_settings.setPixmap(QtGui.QPixmap("icon\settings.png"))
        self.main_settings.setContentsMargins(59, 59, 59, 59)

        self.icon.setContentsMargins(7, 7, 7, 7)
        self.minimize.setContentsMargins(10, 10, 10, 10)
        self.close_icon.setContentsMargins(13, 13, 13, 13)
        self.media_icon.setContentsMargins(57, 57, 57, 57)
        self.media_icon_2.setContentsMargins(57, 57, 57, 57)
        self.media_icon_3.setContentsMargins(57, 57, 57, 57)
        self.media_icon_4.setContentsMargins(57, 57, 57, 57)

        # 메뉴 클릭 이벤트 처리
        self.main_play.mousePressEvent = functools.partial(
            self.tab_one, self.main_play)
        self.main_down.mousePressEvent = functools.partial(
            self.tab_two, self.main_down)
        self.main_settings.mousePressEvent = functools.partial(
            self.tab_three, self.main_settings)

        # 창 닫기/최소화 이벤트 처리
        self.close_icon.mousePressEvent = functools.partial(
            self.close, self.close_icon)
        self.minimize.mousePressEvent = functools.partial(
            self.hide, self.minimize)

        self.media_container.mousePressEvent = functools.partial(
            self.run_file, self.media_container)
        self.media_container_2.mousePressEvent = functools.partial(
            self.run_file_2, self.media_container_2)
        self.media_container_3.mousePressEvent = functools.partial(
            self.run_file_3, self.media_container_3)
        self.media_container_4.mousePressEvent = functools.partial(
            self.run_file_4, self.media_container_4)

        # 함수 연결
        self.search_button.clicked.connect(self.search)
        self.user_input.returnPressed.connect(self.search)
        self.extract_button.clicked.connect(self.extract_video)

        # 유튜브 API 키
        API_KEY = "AIzaSyAuxoo9kr49sbv4r3lcX6o2BhHPSwEOuRg"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        # 유튜브 데이터 객체
        self.youtube_data = build(YOUTUBE_API_SERVICE_NAME,
                                  YOUTUBE_API_VERSION, developerKey=API_KEY)

        # 영상 목록 딕셔너리
        self.video_dict = {}

        # 미디어 부분
        file_list = os.listdir(
            "C:\\Users\\손범수\\Documents\\개발\\PyEx_v3\\extract\\국힙")

        # 비효율적인 방법 나중에 리팩토링
        self.media_title.setText(
            file_list[random.randint(0, len(file_list)-1)])
        self.media_title_2.setText(
            file_list[random.randint(0, len(file_list)-1)])
        self.media_title_3.setText(
            file_list[random.randint(0, len(file_list)-1)])
        self.media_title_4.setText(
            file_list[random.randint(0, len(file_list)-1)])

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.media_player)

    def tab_one(self, event=None, dummy=None):
        # 숨길 위젯들
        self.down_title.hide()
        self.settings_title.hide()
        self.user_input.hide()
        self.search_button.hide()
        self.youtube_list.hide()
        self.select_video.hide()
        self.extract_button.hide()
        self.music_button.hide()
        self.video_button.hide()

        # 나타낼 위젯들
        self.video_title.show()
        self.media_container.show()
        self.media_container_2.show()
        self.media_container_3.show()
        self.media_container_4.show()
        self.media_player.show()

    def tab_two(self, event=None, dummy=None):
        # 숨길 위젯들
        self.settings_title.hide()
        self.video_title.hide()
        self.media_container.hide()
        self.media_container_2.hide()
        self.media_container_3.hide()
        self.media_container_4.hide()
        self.media_player.hide()

        # 나타낼 위젯들
        self.down_title.show()
        self.user_input.show()
        self.search_button.show()
        self.youtube_list.show()
        self.select_video.show()
        self.extract_button.show()
        self.music_button.show()
        self.video_button.show()

    def tab_three(self, event=None, dummy=None):
        # 숨길 위젯들
        self.video_title.hide()
        self.down_title.hide()
        self.user_input.hide()
        self.search_button.hide()
        self.youtube_list.hide()
        self.select_video.hide()
        self.extract_button.hide()
        self.music_button.hide()
        self.video_button.hide()
        self.media_container.hide()
        self.media_container_2.hide()
        self.media_container_3.hide()
        self.media_container_4.hide()

        # 나타낼 위젯들
        self.settings_title.show()

    def search(self):
        self.video_dict.clear()
        self.youtube_list.clear()
        user_input = self.user_input.text()

        search_response = self.youtube_data.search().list(
            # - q : 검색어
            # - order : 정렬방법
            # - part : 필수 매개변수
            # - maxResults : 결과개수
            # 공식문서 - https://developers.google.com/youtube/v3/docs/search/list?hl=ko

            q=user_input,
            order="relevance",
            part="snippet",
            maxResults=15
        ).execute()

        for video in search_response["items"]:
            try:
                video_title = video["snippet"]["title"]
                video_id = video["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                self.video_dict[video_title] = video_url
                self.youtube_list.addItem(video_title)
            except KeyError:
                pass

    def extract_video(self):
        try:
            self.title = self.select_video.text()
            url = self.video_dict[self.title.strip("\n")]
            self.yt = YouTube(url)
        except KeyError:
            pass

        if self.music_button.isChecked():
            self.extract_button.setText("추출")
            self.yt.streams.filter(only_audio=True).first().download("extract")
            self.extract_button.setText("추출 완료!")

        elif self.video_button.isChecked():
            self.extract_button.setText("추출")
            self.yt.streams.filter(
                progressive=True, file_extension='mp4').first().download("extract")
            self.extract_button.setText("추출 완료!")

    # 매우 비효율적임 나중에 리팩토링
    def run_file(self, event=None, dummy=None):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))
        self.player.play()

    def run_file_2(self, event=None, dummy=None):
        media_title = self.media_title_2.text()
        print(media_title)

    def run_file_3(self, event=None, dummy=None):
        media_title = self.media_title_3.text()
        print(media_title)

    def run_file_4(self, event=None, dummy=None):
        media_title = self.media_title_4.text()
        print(media_title)


class Loading_GUI(QMainWindow, form_class_loading):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 윈도우 타이틀
        self.setWindowTitle("파이익스")
        self.setWindowIcon(QIcon("icon\youtube.png"))

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()

        # QTimer 시작
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # 밀리세컨드 타이머
        self.timer.start(35)

    def progress(self):
        global counter

        # 프로그래스 바 값 세팅
        self.progressBar.setValue(counter)

        # 로딩창 닫고 다른 gui열기
        if counter > 100:
            # 타이머 멈춤
            self.timer.stop()

            # 다른 gui 출력
            self.main = MainWindow()
            self.main.show()

            # 로딩창 닫기
            self.close()

        # 카운터 증가
        counter += 5


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Loading_GUI()
    app.exec_()
