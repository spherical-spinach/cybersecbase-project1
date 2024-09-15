from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, csrf_exempt
from django.contrib.auth import authenticate, login, logout
import sqlite3

from .models import Choice, Question

@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# @login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# @login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            return render(request, 'polls/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'polls/login.html')

def logout_view(request):
    logout(request)
    return redirect('polls:login')

@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
@login_required
def create_question(request):
    if request.method == 'POST':

        question_text = request.POST['question_text']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        choice3 = request.POST['choice3']
        choice4 = request.POST['choice4']

        question = Question.objects.create(
            question_text=question_text,
            pub_date=timezone.now(),
            author=request.user
        )

        # To fix sql injection, COMMENT between THIS...

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        cursor.execute(f'INSERT INTO polls_choice (question_id, choice_text, votes) VALUES ({question.id}, "{choice1}", 0)')
        cursor.execute(f'INSERT INTO polls_choice (question_id, choice_text, votes) VALUES ({question.id}, "{choice2}", 0)')
        cursor.execute(f'INSERT INTO polls_choice (question_id, choice_text, votes) VALUES ({question.id}, "{choice3}", 0)')
        cursor.execute(f'INSERT INTO polls_choice (question_id, choice_text, votes) VALUES ({question.id}, "{choice4}", 0)')

        conn.commit()
        conn.close()

        # ...and THIS...

        # ...and UNCOMMENT between THIS

        # Choice.objects.create(
        #     question=question,
        #     choice_text=choice1,
        #     votes=0
        # )
        # Choice.objects.create(
        #     question=question,
        #     choice_text=choice2,
        #     votes=0
        # )
        # Choice.objects.create(
        #     question=question,
        #     choice_text=choice3,
        #     votes=0
        # )
        # Choice.objects.create(
        #     question=question,
        #     choice_text=choice4,
        #     votes=0
        # )

        # ...and THIS
        
    return redirect('polls:index')