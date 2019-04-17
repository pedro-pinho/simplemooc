from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib import messages
from django.db import models
from django.db.models import Avg, Count
from django.http import HttpResponse
from datetime import datetime 

from django.contrib.contenttypes.models import ContentType

from .models import Thread, Activity, Comment
from .forms import ReplyForm

import json

# class ForumView(TemplateView):
#     template_name = 'forum/index.html'
# index = TemplateView.as_view(template_name='forum/index.html')

class ForumView(ListView):
    model = Thread
    paginate_by = 4
    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        
        upvotes = self.object_list.filter(activities__activity_type=Activity.UP_VOTE).count()
        downvotes = self.object_list.filter(activities__activity_type=Activity.DOWN_VOTE).count()
        context['points'] = upvotes-downvotes

        response = []
        tag = self.kwargs.get('tag', '')
        list_of_threads = []
        if tag:
            list_of_threads = self.object_list.filter(tags__slug__icontains=tag)
        else:
            list_of_threads = self.object_list.all()

        for c in list_of_threads:

            upvotes = c.activities.filter(activity_type=Activity.UP_VOTE).count()
            downvotes = c.activities.filter(activity_type=Activity.DOWN_VOTE).count()

            response.append({
                'pk': c.pk,
                'title': c.title,
                'text': c.text,
                'slug': c.slug,
                'user': c.user,
                'answers': c.answers,
                'tags': c.tags,
                'get_absolute_url': c.get_absolute_url,
                'created_at': c.created_at,
                'updated_at': c.updated_at,
                'points': upvotes - downvotes
            })
        order = self.request.GET.get('order','')
        if order == 'answers':
            context['threads'] = sorted(response, key=lambda k: -k['answers'])
        elif order == 'new':
            context['threads'] = sorted(response, key=lambda k: k['updated_at'], reverse=True)
        else:
            context['threads'] = sorted(response, key=lambda k: -k['points']) 
        context['tags'] = Thread.tags.all()
        
        return context

index = ForumView.as_view()

class ThreadView(DetailView):
    model = Thread
    template_name = 'forum/thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        # @todo implement favorite
        upvotes = self.object.activities.filter(activity_type=Activity.UP_VOTE).count()
        downvotes = self.object.activities.filter(activity_type=Activity.DOWN_VOTE).count()
        context['points'] = upvotes-downvotes
        
        comments = []
        for c in (self.object.comentarios.all()):
            upvotes = c.activities.filter(activity_type=Activity.UP_VOTE).count()
            downvotes = c.activities.filter(activity_type=Activity.DOWN_VOTE).count()
            comments.append({
                'pk': c.pk,
                'user': c.user,
                'text': c.text,
                'correct': c.correct,
                'created_at': c.created_at,
                'updated_at': c.updated_at,
                'points': upvotes - downvotes
            })
        
        context['comments'] = comments
        context['form'] = ReplyForm(self.request.POST or None)
        return context

    # DetailView implementa o método get, mas não o post
    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.ERROR, 'Entre para comentar')
            return redirect(self.request.path)
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = context['form']
        if form.is_valid:
            reply = form.save(commit=False)
            reply.thread = self.object
            reply.user = self.request.user
            reply.save()
            messages.add_message(self.request, messages.SUCCESS, 'Comentário enviado')
            context['form'] = ReplyForm
        # render_to_response: parecido com o método render
        # Por herdar do DetailView, o request já está acessivel
        # assim como o template_name
        return self.render_to_response(context)
thread = ThreadView.as_view()

class ReplyCorrectView(View):
    correct = True

    def get(self, request, pk):
        reply = get_object_or_404(Comment, pk=pk, thread__user=request.user)
        reply.correct = self.correct
        reply.save()
        message = 'Resposta atualizada com sucesso'
        if request.is_ajax():
            data = {'success': True, 'message': message}
            return HttpResponse(json.dumps(data), mimetype='application/json')
        else:
            messages.add_message(request, messages.SUCCESS, message)
            return redirect(reply.thread.get_absolute_url())

reply_correct = ReplyCorrectView.as_view()
reply_incorrect = ReplyCorrectView.as_view(correct=False)

class UpvoteView(View):

    def get(self, request, pk):
        # comentario = 17
        # thread = 18
        reply = get_object_or_404(Comment, pk=pk, user=request.user)
        comment = get_object_or_404(Comment, pk=pk, user=request.user)
        content_type = ContentType.objects.get(app_label='form', model='Comment')
        activity = {
            'user': request.user,
            'activity_type': Activity.UP_VOTE,
            'content_type': content_type
        }

        return redirect(reply.thread.get_absolute_url())

    