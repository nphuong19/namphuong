import os
import playsound
import speech_recognition as sr 
import time
import sys
import ctypes
import datetime
import wikipedia
import json
import re
import webbrowser
import smtplib
import requests
import urllib
import urllib.request as urllib2
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS 
from youtube_search import YoutubeSearch
import pyttsx3
import keyboard
from googletrans import Translator
import tkinter as tk
from PIL import Image, ImageTk

wikipedia.set_lang('vi')
language = 'vi'
#path = ChromDriverManager().install()

#chuyen van ban thanh am thanh
def speak(text):
    print("T.E.U:", text)
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume= engine.getProperty('volume')
    engine.setProperty('volume',volume -0.0)
    engine.setProperty('rate', rate -60)
    engine.setProperty('voice',voices[1].id)
    engine.say(text)
    engine.runAndWait()

#chuyen giong noi thanh vb 
def get_audio():
    print("Đang nghe...")
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        audio = ear_robot.listen(source, phrase_time_limit=5)
        try:
            text = ear_robot.recognize_google(audio, language="vi-VN")
            print ("Tôi: ", text)
            return text
        except:
            print("T.E.U: Đã xảy ra lỗi ! ...")    
            return 0
#dung chay 
def stop():
    speak ("Hẹn gặp lại !")
#nhan dien giong noi 
def get_text():
    for i in range(3):
        text =get_audio()
        if text:
            return text.lower()
        elif i<2:
            speak("Tôi chưa nghe bạn nói, vui lòng thử lại !")
    time.sleep(3)
    stop()
    return 0
#thoi gian 
def thoigian():
    gio = datetime.datetime.now().strftime("%H:%M:%p")
    speak(gio)
#chao hoi 
def xinchao():
    hour = datetime.datetime.now().hour
    if 6<=hour <10:
        speak("Chào buổi sáng ! ")
    elif 10<=hour<13:
        speak("Chào buổi trưa !")
    elif 12<= hour <18:
        speak("Chào buổi chiều !")
    elif 18<= hour <22:
        speak("Chào buổi tối !")
    elif 22<=hour<24:
        speak("Muộn rồi mà sao còn thức ")
    elif 0<=hour<6:
        speak("Quá khuya rồi, nhanh chóng đi ngủ nào !")
    else:
        speak("Có thể thời gian của tôi đang gặp sự cố, bạn xem lại nhé !")

def open_app(text):
    if "powpoint" in text:
        speak("mở powpoint")
        os.system("C:\\Users\\Admin\\Desktop\\PowerPoint.lnk")
    elif "word" in text:
        speak("mở word")
        os.system("C:\\Users\\Admin\\Desktop\\Word.lnk")
    else:
        speak("Ứng dụng chưa cài đặt. Vui Lòng cài đặt cho tui nha !")
def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở. ")
        if input("Nếu muốn tiếp tục thì nhấn q: ") == "q":
            pass
        return True
    else:
        return False

def open_google_and_search(text):
    search_for = str(text).split("kiếm", 1)[1]
    url = f"https://www.google.com/search?q={search_for}"
    webbrowser.get().open(url)
    speak("Đây là thông tin bạn cần tìm")


def open_google_and_search2():
    speak("Nói thứ bạn cần tìm kiếm trên google")
    search = str(get_text()).lower()
    url = f"https://www.google.com/search?q={search}"
    webbrowser.get().open(url) 
    speak("Đây là thông tin bạn cần tìm")
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    # Đường dẫn trang web để lấy dữ liệu về thời tiết
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    # lưu tên thành phố vào biến city
    city = get_text()
    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
    if not city:
        pass
    # api_key lấy trên open weather map
    api_key = "b4750c6250a078a943b3bf920bb138a0"
    # tìm kiếm thông tin thời thời tiết của thành phố
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    # truy cập đường dẫn của dòng 188 lấy dữ liệu thời tiết
    response = requests.get(call_url)
    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    data = response.json()
    # kiểm tra nếu ko gặp lỗi 404 thì xem xét và lấy dữ liệu
    if data["cod"] != "404":
        # lấy value của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Mặt trời mọc vào {sunrise.hour} giờ {sunrise.minute} phút
        Mặt trời lặn vào {sunset.hour} giờ {sunset.minute} phút
        Nhiệt độ trung bình là {current_temperature} độ C
        Áp suất không khí là {current_pressure} héc tơ Pascal
        Độ ẩm là {current_humidity}%
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó nói dòng dưới 227
        speak("Không tìm thấy địa chỉ của bạn")
def play_youtube():
    speak("Nói nội dung bạn muốn tìm trên youtube")
    search = get_text()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak("Đây là thứ mà tôi tìm được bạn xem qua nhé")
def play_youtube_2():
    speak("Nói nội dung bạn muốn tìm trên youtube")
    search = get_text()
    while True:
        result = YoutubeSearch(search, max_results=10).to_dict()
        if result:
            break
    url = f"https://www.youtube.com" + result[0]['url_suffix']
    webbrowser.get().open(url)
    speak("Đây là thứ mà tôi tìm được bạn xem qua nhé")
    print(result)

# đổi hình nền
def change_background():
    api_key = "RNa1k4vpwcTn_T2MeRCpvVtGGRxKVJRh5EsNdK6wfH8"
    url = 'https://api.unsplash.com/photos/random?count=3&client_id=' + api_key
    response = requests.get(url)
    photos = response.json()
    
    # Tạo cửa sổ đồ họa
    window = tk.Tk()
    window.title("Chọn hình nền")
    
    # Thiết lập hình nền khi nhấp vào ảnh
    def set_wallpaper(image_path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        window.destroy()
        speak("Đã thay đổi hình nền thành công! Hãy kiểm tra hình nền của bạn")
    
    # Hiển thị danh sách ảnh
    speak("Vui lòng chọn hình nền!!!")
    for i, photo in enumerate(photos):
        thumbnail_url = photo['urls']['full']
        image_path = f"D:\\pictures\\thumbnail_{i}.png"
        response = requests.get(thumbnail_url)
        with open(image_path, 'wb') as f:
            f.write(response.content)
    
        
        # Hiển thị ảnh thumbnail
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.BICUBIC)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(window, image=photo)
        label.image = photo
        label.grid(row=i // 5, column=i % 5)
        
        # Gán hàm set_wallpaper cho sự kiện nhấp chuột vào ảnh
        label.bind("<Button-1>", lambda event, path=image_path: set_wallpaper(path))
    
    # Hiển thị cửa sổ
    window.mainloop()
#change_background() 

# mở nhạc có trong máy
# thêm thư viện keyboard
def play_music(path):
    # path là tham số chứa đường dẫn thư mục chứa nhạc
    myPATH = path
    # lấy file nhạc ra
    ds = os.listdir(myPATH)
    # dùng for mở từng bài nhạc
    for i in ds:
        print("\nĐang phát bài: " + i)
        os.system(myPATH + "\\" + i)
        
        print("Nhấn phím '~' để chuyển bài hoặc Esc để dừng trình phát nhạc...")
        while True:
            if keyboard.is_pressed('~'):
                print("\nĐã phát xong bài: " + i)
                break
            elif keyboard.is_pressed('esc'):
                print("\nĐã dừng trình phát nhạc ")                
                return             
#play_music("D:\\music")

# Tìm kiếm từ khóa trên Wikipedia
def search_wikipedia(keyword):
    try:
        result = wikipedia.summary(keyword, sentences=2)
        speak("Đây là kết quả tìm kiếm trênWikipedia:")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  # Lấy 3 lựa chọn đầu tiên
        speak("Có nhiều kết quả cho từ khóa này. Bạn có thể thử một số lựa chọn sau:")
        for i, option in enumerate(options):
            print(f"Lựa chọn {i+1}: {option}")
    except wikipedia.exceptions.PageError:
        speak("Không tìm thấy kết quả nào cho từ khóa này.")
#search_wikipedia()

#main 
def main():
    speak("Xin chào tôi là Tều")
    xinchao()
    name = get_text()
    if name:
        speak(f'Tôi có thể giúp gì cho bạn ')
        while True:
            text = get_text()
            if not text:
                break
            elif ('tạm biệt' in text) or ('hẹn gặp lại' in text):
                stop()
                break
            elif('mấy giờ rồi' in text) or ('bây giờ là mấy giờ' in text):
                thoigian()
            elif('mở ứng dụng' in text):
                open_app(text)
            elif "mở" in text:
                if '.' in text:
                    open_website(text)
            elif "tìm kiếm" in text:
                if str(text).split("kiếm", 1)[1] == "":
                    open_google_and_search2()
                else:
                    open_google_and_search(text)
            elif "thời tiết" in text:
                current_weather()
            elif 'youtube' in text:
                speak("Bạn muốn tìm kiếm đơn giản hay phức tạp")
                yeu_cau = get_text()
                if "đơn giản" in yeu_cau:
                    play_youtube()
                    if input():
                        pass
                elif "phức tạp" in yeu_cau:
                    play_youtube_2()
                    if input("Tiếp tục y/n: ") == "y":
                        pass
            elif "hình nền" in text:
                change_background()
            elif "wikipedia" in text:
                speak("Vui lòng nêu từ khóa bạn muốn tìm kiếm trên Wikipedia:")
                keyword = get_text()
                if keyword:
                    search_wikipedia(keyword)
            elif "phát nhạc" in text:
                speak("Ok. Tôi bắt đầu mở nhạc đây")
                play_music("D:\music")
            else :
                speak("Tôi chưa có chức năng này.")
main()  