import json
import os
import threading
import urllib.parse
import urllib.request
import tkinter as tk
from tkinter import messagebox


def load_env(path=".env"):
    env = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip()
    return env


ENV = load_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
OPENWEATHER_API_KEY = ENV.get("w_apikey", "")


def get_weather(city):
    if not OPENWEATHER_API_KEY:
        return None
    query = urllib.parse.urlencode(
        {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric", "lang": "kr"}
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{query}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }
    except Exception:
        return None


def weather_summary(weather):
    return f"{weather['temp']:.0f}°C, {weather['description']}"


def weather_tip(weather):
    temp = weather["temp"]
    description = weather["description"]
    summary = weather_summary(weather)
    if "비" in description or "눈" in description:
        return f"현재 {summary}. 실내 운동을 고려해보세요."
    if temp >= 28:
        return f"현재 {summary}. 수분을 충분히 섭취하며 운동하세요."
    if temp <= 5:
        return f"현재 {summary}. 충분히 몸을 풀고 운동하세요."
    return f"현재 {summary}. 야외 활동하기 좋은 날씨예요."


ADVICE = {
    "저체중": "끼니를 거르지 말고 단백질과 탄수화물을 충분히 챙겨 체중을 늘려보세요.",
    "정상": "지금의 균형 잡힌 식습관과 운동 습관을 꾸준히 유지해주세요.",
    "과체중": "간식과 야식을 줄이고 주 3회 이상 걷기 등 가벼운 운동을 시작해보세요.",
    "비만": "식단 조절과 규칙적인 운동을 병행하고, 필요하다면 전문가 상담을 받아보세요.",
    "고도비만": "건강에 위험할 수 있으니 병원을 방문해 전문적인 관리 계획을 세우는 것을 권장해요.",
}


def classify_bmi(bmi):
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23:
        return "정상"
    elif bmi < 25:
        return "과체중"
    elif bmi < 30:
        return "비만"
    else:
        return "고도비만"


def calculate():
    try:
        height_cm = float(entry_height.get())
        weight_kg = float(entry_weight.get())
        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("입력 오류", "키와 몸무게를 올바른 숫자로 입력해주세요.")
        return

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    category = classify_bmi(bmi)

    result_label.config(text=f"BMI: {bmi:.1f}  ({category})")
    advice_label.config(text=ADVICE[category])

    city = entry_city.get().strip() or "Seoul"
    weather_label.config(text="날씨 정보를 불러오는 중...")
    threading.Thread(target=fetch_weather, args=(city,), daemon=True).start()


def fetch_weather(city):
    weather = get_weather(city)

    def update_label():
        if weather is None:
            weather_label.config(
                text="날씨 정보를 가져올 수 없습니다. (.env의 API 키 또는 도시명을 확인하세요)"
            )
        else:
            weather_label.config(text=weather_tip(weather))

    root.after(0, update_label)


root = tk.Tk()
root.title("BMI 계산기")
root.geometry("320x360")
root.resizable(False, False)

tk.Label(root, text="키 (cm)").pack(pady=(20, 0))
entry_height = tk.Entry(root, justify="center")
entry_height.pack()

tk.Label(root, text="몸무게 (kg)").pack(pady=(10, 0))
entry_weight = tk.Entry(root, justify="center")
entry_weight.pack()

tk.Label(root, text="도시 (날씨 조회용)").pack(pady=(10, 0))
entry_city = tk.Entry(root, justify="center")
entry_city.insert(0, "Seoul")
entry_city.pack()

tk.Button(root, text="계산하기", command=calculate).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

advice_label = tk.Label(
    root, text="", wraplength=280, justify="center", fg="gray20"
)
advice_label.pack(pady=(8, 0))

weather_label = tk.Label(
    root, text="", wraplength=280, justify="center", fg="steelblue"
)
weather_label.pack(pady=(8, 0))

root.mainloop()
