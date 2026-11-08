from rest_framework.fields import IntegerField, CharField, FileField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Submission, Assignment, SubmissionFile, Lesson, Source, Book
from root.serializers import CustomModelSerializer
from users.models import Group


# from apps.tasks import ai_check_submissions


class FileModelSerializer(ModelSerializer):
    homework = IntegerField(required=True, write_only=True)
    student = IntegerField(read_only=True)

    class Meta:
        model = SubmissionFile
        fields = ('id', 'homework', 'student')
        read_only_fields = ('id',)

    def create(self, validated_data):
        uploaded_file = validated_data.get('content')
        homework_id = validated_data.pop('homework')
        student_id = validated_data.pop('student')

        # Submission yaratish
        submission = Submission.objects.create(
            homework_id=homework_id,
            student_id=student_id
        )

        line_count = 0
        if uploaded_file:
            uploaded_file.open()
            content_bytes = uploaded_file.read()
            content_text = content_bytes.decode('utf-8')
            # res = ai_check_submissions(content_text, homework_id, submission)
            line_count = len(content_text.strip().splitlines())
            uploaded_file.seek(0)
        validated_data['line_count'] = line_count
        validated_data['submission'] = submission

        return super().create(validated_data)


class SubmissionModelSerializer(ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'final_grade', 'student', 'ai_grade', 'ai_feedback', 'submitted_at')
        read_only_fields = ('id', 'student', 'ai_grade', 'ai_feedback', 'created_at', 'submitted_at')


class HomeworkModelSerializer(ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('id', 'title', 'description', 'start_date', 'deadline', 'created_at')
        read_only_fields = ('id', 'created_at')


class SourceModelSerializer(ModelSerializer):
    class Meta:
        model = Source
        fields = ("id", "name", "link", "lesson", "created_at")
        read_only_fields = ("id", "created_at")


class LessonModelSerializer(CustomModelSerializer):
    group = PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=True)
    sources = SourceModelSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id", "name", "description", "presentation", "status", "group", "teacher",
            "created_at", "updated_at", "sources", "book"
        )
        read_only_fields = ("id", "teacher", "created_at", "status", "updated_at")


class LessonUpdateSerializer(Serializer):
    name = CharField(required=False)
    description = CharField(required=False)
    presentation = FileField()
    status = CharField(required=False)
    group = PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    book = IntegerField(required=False)


class BookModelSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "name", "description", "file", "created_at")
        read_only_fields = ("id", "created_at")


class BookUpdateSerializer(Serializer):
    name = CharField(required=False)
    description = CharField(required=False)
    file = FileField(required=False)
