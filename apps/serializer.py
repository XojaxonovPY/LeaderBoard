from rest_framework.serializers import ModelSerializer

from apps.models import Submission, Homework, SubmissionFile


class FileModelSerializer(ModelSerializer):
    class Meta:
        model = SubmissionFile
        fields = ('id','file_name', 'content', 'line_count')
        read_only_fields = ('id', 'line_count')

    def create(self, validated_data):
        uploaded_file = validated_data.get('content')

        line_count = 0
        if uploaded_file:
            uploaded_file.open()  # Fayl ochiladi, agar yopilgan bo‘lsa
            content_bytes = uploaded_file.read()
            content_text = content_bytes.decode('utf-8')  # Kodlashga qarab
            line_count = len(content_text.strip().splitlines())
            uploaded_file.seek(0)  # Faylni qayta o'qish uchun reset

        validated_data['line_count'] = line_count
        return super().create(validated_data)


class SubmissionSaveModelSerializer(ModelSerializer):
    files = FileModelSerializer(many=True)

    class Meta:
        model = Submission
        fields = ('id', 'student', 'homework', 'created_at', 'submitted_at', 'files')
        read_only_fields = ('id', 'student', 'created_at', 'submitted_at')

    def create(self, validated_data):
        files_data = validated_data.pop('files')
        submission = Submission.objects.create(**validated_data)
        for file_data in files_data:
            SubmissionFile.objects.create(submission=submission, **file_data)
        return submission


class SubmissionModelSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'final_grade', 'student', 'homework', 'ai_grade', 'ai_feedback', 'submitted_at')
        read_only_fields = ('id', 'student', 'homework', 'ai_grade', 'ai_feedback', 'created_at', 'submitted_at',
                            'homework')


class HomeworkModelSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('id', 'title', 'description', 'points', 'start_date', 'deadline', 'line_limit', 'teacher', 'group',
                  'file_extensions', 'ai_grading_prompt', 'created_at')
        read_only_fields = ('id', 'created_at', 'teacher')
