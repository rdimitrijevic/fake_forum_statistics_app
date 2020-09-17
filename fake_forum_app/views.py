from django.http import HttpResponse
from pymongo import MongoClient
from django.shortcuts import render
from .forms import TopicForm, PostsForm, UsersForm

client = MongoClient("mongodb+srv://lale:lalelale@cluster0-lazue.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test
(posts, users, topics) = (db.posts, db.Users, db.Topics)


# Create your views here.
def users_view(request):
    regex = ''
    if request.method == "POST":
        form = UsersForm(request.POST)
        if form.is_valid():
            regex = form.cleaned_data["username"]
    else:
        form = UsersForm()

    user_array = []
    for user in users.find():
        if regex not in user["username"]:
            continue
        user_array.append({
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "gender": user["gender"]
        })

    return render(request, 'users.html', {"users": user_array, "form": form})


def posts_view(request):
    posts_array = []
    regex = ''

    if request.method == "POST":
        form = PostsForm(request.POST)
        if form.is_valid():
            regex = form.cleaned_data["topicName"]
    else:
        regex = ''
        form = PostsForm()

    pipeline = [
        {
            "$lookup": {
                "from": "Topics",
                "localField": "parentTopic",
                "foreignField": "_id",
                "as": "topic"
            }
        },
        {"$unwind": "$topic"},
        {
            "$match": {
                "topic.title": {
                    "$regex": regex
                }
            }
        }
    ]

    post_results = posts.aggregate(pipeline=pipeline)
    for post in post_results:
        topic = post["topic"]["title"]

        posts_array.append({
            "id": str(post["_id"]),
            "content": post["content"],
            "topic": topic,
            "date": post["createdAt"]
        })

    return render(request, 'posts.html', {"posts": posts_array, "form": form})


def topics_view(request):
    topics_array = []
    regex = ''

    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            regex = form.cleaned_data["creatorUsername"]
    else:
        regex = ''
        form = TopicForm()

    pipeline = [
        {
            "$lookup": {
                "from": "Users",
                "localField": "createdBy",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {
            "$unwind": "$user"
        },
        {
            "$match": {
                "user.username": {"$regex": regex}
            }
        }
    ]

    topic_results = topics.aggregate(pipeline=pipeline)
    for topic in topic_results:
        user = topic["user"]["username"]

        topics_array.append({
            "id": str(topic["_id"]),
            "title": topic["title"],
            "author": user,
            "date": topic["createdAt"]
        })

    return render(request, 'topics.html', {"topics": topics_array, "form": form})
