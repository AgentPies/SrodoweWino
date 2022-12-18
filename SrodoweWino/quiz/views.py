from django.forms import ModelForm
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Question, Players
import random

# Create your views here.

#Classes that handle forms
class NewQuestionForm(ModelForm):
  question = forms.TextInput()
  answer = forms.TextInput()
  class Meta:
    model = Question
    fields = ['question', 'answer']
  
class NewPlayerForm(ModelForm):
  player = forms.TextInput()
  class Meta:
    model = Players
    fields = ['name']  
  
#Quiz site
def quiz(request):
  players = Players.objects.all()
  for i,player in enumerate(players):
    if player.current_player:
      previous_player = player
      previous_player.current_player = False
      previous_player.save()
      try:
        current_player = players[i+1]
      except IndexError:
        current_player = players[0]
      current_player.current_player = True
      current_player.save()
      break
  else:
    current_player = players[0]
    current_player.current_player = True
    current_player.save()
  
  #Handle situation when running out of questions
  all_used = True
  for question in Question.objects.all():
    if question.used == False:
      all_used= False
      break
  if all_used:
    questions = Question.objects.all()
    for question in questions:
      question.used = False
      question.save()
    return render(request, 'scoreboard.html', {'players':players})  
  
  #Chooses random question
  question_id = random.randint(0, Question.objects.count()-1)
  qs = Question.objects.all()[question_id]
  
  #If it is already used it will search for another until it findes not used
  while(qs.used):
    question_id = random.randint(0, Question.objects.count()-1)
    qs = Question.objects.all()[question_id]

  if request.POST.get('add_points'):
    # Add the points for the question to the player's score
    previous_player.score += 1
    previous_player.save()
    #Changes question to be used (restarts it when you return to home page)
    qs.used = True
    qs.save()
  
  if request.POST.get('no_points'):
    qs.used = True
    qs.save()
  
  if request.POST.get('skip'):
    previous_player.current_player = True
    previous_player.save()
    current_player.current_player = False
    current_player.save()
    current_player = previous_player

    
  return render(request, 'quiz.html', {
    'questions': qs, 'current_player': current_player, 'players': Players.objects.all()
  })

def index(request):
  Players.objects.all().delete()
  questions = Question.objects.all()
  for question in questions:
    question.used = False
    question.save()
  return render(request, 'index.html')

def add(request):
  if request.POST:
    form = NewQuestionForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'add.html', {
    'form': NewQuestionForm
  })
  
def players(request):
  players = Players.objects.all()
  if request.POST:
    form = NewPlayerForm(request.POST)
    if form.is_valid():
      form.save()
  return render(request, 'players.html', {
    'form': NewPlayerForm, 'players': players
  })
  
def scoreboard(request):
  players = Players.objects.all()
  return render(request, 'scoreboard.html', {
      'players': players
  })