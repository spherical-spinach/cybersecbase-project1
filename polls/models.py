import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

# Here we create admin user and two common users after migration,
# and two Questions each for Alice and Bob
@receiver(post_migrate)
def create_users_and_questions(sender, **kwargs):
    # Check if the users and questions have already been created
    if User.objects.filter(username__in=['admin', 'alice', 'bob']).count() == 3 and \
       Question.objects.filter(author__in=[User.objects.get(username='alice'), User.objects.get(username='bob')]).count() == 2:
        return
    
    # Create the admin user
    admin, _ = User.objects.get_or_create(
        username='admin',
        is_superuser=True,
        is_staff=True
    )
    admin.set_password('admin123')
    admin.save()

    # Create the regular users
    alice, _ = User.objects.get_or_create(username='alice')
    alice.set_password('alice123')
    alice.save()

    bob, _ = User.objects.get_or_create(username='bob')
    bob.set_password('bob123')
    bob.save()

    # Create one Question for four choices authored by Alice
    alice_question = Question.objects.create(
        question_text="What's your favorite season",
        pub_date=timezone.now(),
        author=alice
    )
    Choice.objects.create(
        question=alice_question,
        choice_text="Winter",
        votes=0
    )
    Choice.objects.create(
        question=alice_question,
        choice_text="Spring",
        votes=0
    )
    Choice.objects.create(
        question=alice_question,
        choice_text="Summer",
        votes=0
    )

    Choice.objects.create(
        question=alice_question,
        choice_text="Autumn",
        votes=0
    )

    # Create one Question for three choices authored by Bob
    bob_question = Question.objects.create(
        question_text="What is your favorite primary color?",
        pub_date=timezone.now(),
        author=bob
    )
    Choice.objects.create(
        question=bob_question,
        choice_text="Yellow",
        votes=0
    )
    Choice.objects.create(
        question=bob_question,
        choice_text="Red",
        votes=0
    )
    Choice.objects.create(
        question=bob_question,
        choice_text="Blue",
        votes=0
    )