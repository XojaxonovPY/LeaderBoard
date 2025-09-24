import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

import django

django.setup()

from apps.models import Submission, Homework
from root.settings import API_KEY

from google import generativeai as genai


def ai_check_submissions(file_code: str, homework_id: int, submission: Submission) -> dict:
    # Google Gemini API sozlash
    genai.configure(api_key=API_KEY)

    homework = Homework.objects.filter(id=homework_id).first()
    if not homework:
        raise Exception("Homework topilmadi!")

    # Prompt yasash
    prompt = (
        f"Topshiriq fayl turi: {homework.file_extensions}\n"
        f"Mavzu: {homework.title}\n"
        f"Topshiriq tavsifi: {homework.description}\n"
        f"Muddati: {homework.start_date} dan {homework.deadline} gacha\n\n"
        f"Quyidagi kodni tahlil qiling va faqat quyidagi formatda javob bering:\n\n"
        f"Ball: <0-{homework.points}>\n"
        f"Izoh: <qisqa va aniq xulosa O'zbek tilida>\n\n"
        f"⚠️ Iltimos, bu formatdan tashqari hech qanday matn, salomlashuv yoki izoh yozmang.\n\n"
        f"Fayl: {submission.files.name}\n\n"
        f"{file_code}"
    )

    # Gemini modelini chaqirish
    model = genai.GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content(prompt)

    # Natijani olish
    text = response.text.strip()
    lines = text.splitlines()

    result = {"ai_grade": None, "ai_feedback": text}
    for line in lines:
        if line.lower().startswith("ball:"):
            try:
                score = int(line.split(":", 1)[1].split("/")[0].strip())
                result["ai_grade"] = score
            except:
                continue
        elif line.lower().startswith("izoh:"):
            result["ai_feedback"] = line.split(":", 1)[1].strip()

    # Submission’ni yangilash
    submission.ai_grade = result.get("ai_grade")
    submission.ai_feedback = result.get("ai_feedback")
    submission.save()

    return result
