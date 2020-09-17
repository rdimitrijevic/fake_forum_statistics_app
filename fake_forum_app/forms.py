from django import forms


class TopicForm(forms.Form):
    creatorUsername = forms.CharField(label="Search by creator username", min_length=1, max_length=30)


class UsersForm(forms.Form):
    username = forms.CharField(label="Search by username", min_length=1, max_length=30)


class PostsForm(forms.Form):
    topicName = forms.CharField(label="Search by topic name", min_length=1, max_length=30)
