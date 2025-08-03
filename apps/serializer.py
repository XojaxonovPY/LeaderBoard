from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from apps.models import Submission, Homework, SubmissionFile
from apps.tasks import ai_check_submissions


class FileModelSerializer(ModelSerializer):
    homework = IntegerField(required=True, write_only=True)
    student = IntegerField(read_only=True)

    class Meta:
        model = SubmissionFile
        fields = ('id', 'file_name', 'content', 'line_count', 'homework', 'student')
        read_only_fields = ('id', 'line_count')

    def create(self, validated_data):
        uploaded_file = validated_data.get('content')
        homework_id = validated_data.pop('homework')
        student_id = validated_data.pop('student')

        # Submission yaratish
        submission = Submission.objects.create(
            homework_id=homework_id,
            student_id=student_id
        )

        # Fayl ichidagi qatorlar sonini hisoblash
        line_count = 0
        if uploaded_file:
            uploaded_file.open()
            content_bytes = uploaded_file.read()
            content_text = content_bytes.decode('utf-8')
            res = ai_check_submissions(content_text, homework_id, submission)
            line_count = len(content_text.strip().splitlines())
            uploaded_file.seek(0)
        # Qo‘shimcha qiymatlarni validated_data ichiga beramiz
        validated_data['line_count'] = line_count
        validated_data['submission'] = submission

        return super().create(validated_data)


class SubmissionModelSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'final_grade', 'student', 'homework', 'ai_grade', 'ai_feedback', 'submitted_at')
        read_only_fields = ('id', 'student', 'homework', 'ai_grade', 'ai_feedback', 'created_at', 'submitted_at',
                            'homework')


class HomeworkModelSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'title', 'description', 'points', 'start_date', 'deadline', 'teacher', 'group',
                  'file_extensions', 'created_at')
        read_only_fields = ('id', 'created_at', 'teacher')
