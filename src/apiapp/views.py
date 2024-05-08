from .models import Quiz, Question, Choice, UserResponse
from .serializer import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserResponseSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action



class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer



class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer



class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer



class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    # Custom action to handle quiz submissions
    @action(detail=True, methods=['post'])
    def submit_quiz(self, request, pk=None):
        quiz = self.get_object()
        user_responses_data = request.data.get('user_responses')
        serializer = UserResponseSerializer(data=user_responses_data, many=True)
        if serializer.is_valid():
            serializer.save()
            # Calculate score
            score = calculate_quiz_score(quiz, user_responses_data)
            return Response({'score': score}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calculate_quiz_score(quiz, user_responses_data):
    # Calculate score logic goes here
    # Example logic: count correct responses
    total_score = 0
    for user_response_data in user_responses_data:
        choice = Choice.objects.get(id=user_response_data['choice'])
        if choice.is_correct:
            total_score += 1
    return total_score
