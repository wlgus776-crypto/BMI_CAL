import tkinter as tk
from tkinter import messagebox


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


root = tk.Tk()
root.title("BMI 계산기")
root.geometry("320x280")
root.resizable(False, False)

tk.Label(root, text="키 (cm)").pack(pady=(20, 0))
entry_height = tk.Entry(root, justify="center")
entry_height.pack()

tk.Label(root, text="몸무게 (kg)").pack(pady=(10, 0))
entry_weight = tk.Entry(root, justify="center")
entry_weight.pack()

tk.Button(root, text="계산하기", command=calculate).pack(pady=15)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack()

advice_label = tk.Label(
    root, text="", wraplength=280, justify="center", fg="gray20"
)
advice_label.pack(pady=(8, 0))

root.mainloop()
