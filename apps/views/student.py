from datetime import datetime, timedelta

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Homework, Submission
from apps.serializer import HomeworkModelSerializer, FileModelSerializer
from apps.serializer import SubmissionModelSerializer


@extend_schema(tags=['students'])
class SubmissionCreatAPIView(CreateAPIView):
    serializer_class = FileModelSerializer

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.id)


@extend_schema(tags=['students'])
class SubmissionListAPIView(ListAPIView):
    serializer_class = SubmissionModelSerializer
    queryset = Submission.objects.all()


@extend_schema(tags=['students'])
class HomeworkListAPIView(ListAPIView):
    serializer_class = HomeworkModelSerializer
    queryset = Homework.objects.all()


@extend_schema(tags=['students'], parameters=[
    OpenApiParameter(
        name='monthly',
        description='enter month',
        required=False,
        type=str,
    ),
    OpenApiParameter(
        name='day',
        description='enter days',
        required=False,
        type=str,
    ),
    OpenApiParameter(
        name='last month',
        description='enter days',
        required=False,
        type=str,
    ),
])
class LeaderBoardAPIView(APIView):
    def get(self, request):
        user = request.user
        queryset = Submission.objects.filter(student=user)

        # query params
        monthly = request.query_params.get('monthly')  # '2025-06'
        day = request.query_params.get('day')  # '2025-06-20'
        last_month = request.query_params.get('last month')  # faqat mavjudligini tekshirish

        if monthly:
            try:
                year, month = map(int, monthly.split('-'))
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1)
                else:
                    end_date = datetime(year, month + 1, 1)
                queryset = queryset.filter(created_at__gte=start_date, created_at__lt=end_date)
            except:
                pass

        if day:
            try:
                target_day = datetime.strptime(day, "%Y-%m-%d").date()
                queryset = queryset.filter(created_at__date=target_day)
            except:
                pass

        if last_month is not None:
            today = now().date()
            first_day_this_month = today.replace(day=1)
            last_month_end = first_day_this_month - timedelta(days=1)
            last_month_start = last_month_end.replace(day=1)
            queryset = queryset.filter(created_at__date__gte=last_month_start, created_at__date__lte=last_month_end)

        total_score = queryset.aggregate(total=Coalesce(Sum(F('final_grade')) + Sum(F('ai_grade')), 0))

        return Response({
            "student_id": user.id,
            "student_name": user.full_name,
            "total_score": total_score
        })
