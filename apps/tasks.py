import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

import django

django.setup()

from apps.models import Submission, Homework
from root.settings import API_KEY, API_URL
import requests


def ai_check_submissions(file_code: str, homework_id: int, submission: Submission) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    homework = Homework.objects.filter(id=homework_id).first()
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Siz foydalanuvchiga yordam beruvchi dasturchi assistentsiz."},
            {"role": "system", "content": f"Topshiriq fayl turi: {homework.file_extensions}"},
            {"role": "system", "content": f"Mavzu: {homework.title}"},
            {"role": "system", "content": f"Topshiriq tavsifi: {homework.description}"},
            {"role": "system", "content": f"Muddati: {homework.start_date} dan {homework.deadline} gacha"},
            {"role": "system", "content": (
                f"Quyidagi kodni tahlil qiling va faqat quyidagi formatda javob bering:\n\n"
                f"Ball: <0-{homework.points}>\n"
                f"Izoh: <qisqa va aniq xulosa O'zbek tilida>\n\n"
                f"⚠️ Iltimos, bu formatdan tashqari hech qanday matn, salomlashuv, yoki izoh yozmang."
            )},
            {"role": "user", "content": f"Quyidagi {submission.files.name} fayldagi kodni tekshiring:\n\n{file_code}"}
        ]

    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        text = response.json()["choices"][0]["message"]["content"]
        lines = text.strip().splitlines()

        result = {"ai_grade": None, "ai_feedback": text.strip()}
        for line in lines:
            if line.lower().startswith("ball:"):
                try:
                    score = int(line.split(":", 1)[1].split("/")[0].strip())
                    result["ai_grade"] = score
                except:
                    continue
            elif line.lower().startswith("izoh:"):
                result["ai_feedback"] = line.split(":", 1)[1].strip()
        print(result)

        submission.ai_grade = result.get("ai_grade")
        submission.ai_feedback = result.get("ai_feedback")
        submission.save()
        return result
    else:
        raise Exception(f"AI server xatosi: {response.status_code} - {response.text}")
