# -*- coding:utf-8 -*-
import sys

from django.shortcuts import render,redirect
from .forms import PostForm
from .models import Score
import datetime
import json


# Create your views here.

def score_list(request):
    score_list = Score.objects.all()
    return render(request, 'score/score.html', {"score": score_list})


def monthly_score(request, date):
    year = int(date[:4])
    month = int(date[4:])
    score_list = Score.objects.filter(date__year=year, date__month=month)

    score_dict = dict()
    for data in score_list:
        try:
            if not score_dict[data.name]:
                pass
        except Exception:
            score_dict[data.name] = []

        score_dict[data.name].append(data.score)

    publish_data = list()

    user_dict = dict()

    max_game = 0;
    average_dict = dict()

    for name, scores in score_dict.items():
        user = UserScore(name, scores)
        publish_data.append(user)
        if max_game < user.game_count:
            max_game = user.game_count
        average_dict[user.name] = user.average
        user_dict[user.name] = user

    name_rank_dict = dict()
    rank_name_dict = dict()

    sorted_publish_data = list()

    for user in publish_data:
        name = user.name
        max_game = user.game_count
        name_rank_dict[name] = 1
        for rank_name, rank_int in name_rank_dict.items():
            if rank_name == name:
                continue
            if average_dict[name] > average_dict[rank_name]:
                name_rank_dict[rank_name] = name_rank_dict[rank_name] + 1
            else:
                name_rank_dict[name] = name_rank_dict[name] + 1

    for name, rank in name_rank_dict.items():
        rank_name_dict[rank] = name

    for user in publish_data:
        user.rank = name_rank_dict[user.name]

    for i in range(1, len(rank_name_dict) + 1):
        sorted_publish_data.append(user_dict[rank_name_dict[i]])

    if month == 1:
        year = year - 1
        month = 12
    else:
        month = month - 1

    pre_month_data = get_monthly_score(str(year) + str(month))
    # print(pre_month_data["권영균"].rank)
    # print(pre_month_data["류지원"].rank)

    for month_user in sorted_publish_data:
        try:
            pre_month_user = pre_month_data[month_user.name]

            if pre_month_user.rank > month_user.rank:
                month_user.change_rank = "+" + str(pre_month_user.rank - month_user.rank)
            elif pre_month_user.rank == month_user.rank:
                month_user.change_rank = "-"
            else:
                month_user.change_rank = "-" + str(month_user.rank - pre_month_user.rank)

            if pre_month_user.average > month_user.average:
                month_user.change_average = "-{:.2f}".format(pre_month_user.average - month_user.average)
            elif pre_month_user.average == month_user.average:
                month_user.change_average = "-"
            else:
                month_user.change_average = "+{:.2f}".format(month_user.average - pre_month_user.average)
        except Exception:

            month_user.change_rank = "new"
            month_user.change_average = "new"
            continue

    return render(request, 'score/monthly_score.html',
                  {"score": sorted_publish_data, "line": len(publish_data), "date": date, "max_game": max_game,
                   "rank": name_rank_dict})


def get_monthly_score(date):
    year = int(date[:4])
    month = int(date[4:])
    score_list = Score.objects.filter(date__year=year, date__month=month)

    score_dict = dict()
    for data in score_list:
        try:
            if not score_dict[data.name]:
                pass
        except Exception:
            score_dict[data.name] = []
        score_dict[data.name].append(data.score)
    user_dict = dict()
    publish_data = list()
    average_dict = dict()

    for name, scores in score_dict.items():
        user = UserScore(name, scores)
        user_dict[user.name] = user
        average_dict[user.name] = user.average

    name_rank_dict = dict()

    for name, user in user_dict.items():
        name_rank_dict[name] = 1
        for rank_name, rank_int in name_rank_dict.items():
            if rank_name == name:
                continue
            if average_dict[name] > average_dict[rank_name]:
                name_rank_dict[rank_name] = name_rank_dict[rank_name] + 1
            else:
                name_rank_dict[name] = name_rank_dict[name] + 1

    print(json.dumps(name_rank_dict))

    for name, user in user_dict.items():
        user.rank = name_rank_dict[name]

    return user_dict


def daily_score(request, date):
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:])
    print(year, month, day)

    input_date = datetime.date(year, month, day)

    score_list = Score.objects.filter(date__year=year, date__month=month, date__day=day)

    score_dict = dict()
    for data in score_list:
        try:
            if not score_dict[data.name]:
                pass
        except Exception:
            score_dict[data.name] = []

        score_dict[data.name].append(data.score)

    publish_data = list()

    max_game = 0;
    for name, scores in score_dict.items():
        user = UserScore(name, scores)
        publish_data.append(user)
        if max_game < user.game_count:
            max_game = user.game_count

    print(score_dict)
    return render(request, 'score/daily_score.html',
                  {"score": publish_data, "line": len(publish_data), "date": date, "max_game": max_game})


def post(request):
    if request.method == "POST":
         # create a form instance and populate it with data from the request:
        form = PostForm(request.POST) #PostForm으로 부터 받은 데이터를 처리하기 위한 인스턴스 생성
        if form.is_valid(): #폼 검증 메소드
            score = form.save(commit = True) #lotto 오브젝트를 form으로 부터 가져오지만, 실제로 DB반영은 하지 않는다.
            return render(request, 'score/new_score.html', {'form' : form})
    else:
        form = PostForm() #forms.py의 PostForm 클래스의 인스턴스
        return render(request, 'score/new_score.html', {'form' : form})  # 템플릿 파일 경로 지정, 데이터 전달


class DaliyUser():
    date = str()
    user_list = list()


class UserScore():
    name = str()
    score_list = list()
    total = int()
    average = float()
    game_count = int()
    rank = int()
    change_rank = None
    cahnge_average = None

    def __init__(self, name, score_list):
        self.name = name
        self.score_list = score_list
        self.total = 0
        self.game_count = 0
        for score in score_list:
            self.game_count = self.game_count + 1
            self.total = self.total + score
        self.average = self.total / float(self.game_count)
