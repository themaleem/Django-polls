from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from poll.models import Poll,Choice,Vote,User
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from poll.forms import PollForm,EditPollForm,ChoiceForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# API views
from .serializers import UserSerializer,VoteSerializer,PollSerializer,ChoiceSerializer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt  #allows csrf from any origin
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
# Create your views here.


# API funcs starts
# Versions of API in acsending order
# comment out all but one at an instance 
# and edit urls.py to match the uncommented view 

# Version 1

# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

# @csrf_exempt
# def user_list(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         users_serializer = UserSerializer(users, many=True)
#         return JSONResponse(users_serializer.data)
    
#     elif request.method == 'POST':
#         user_data = JSONParser().parse(request)
#         user_serializer = UserSerializer(data=user_data)
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return JSONResponse(user_serializer.data, status=status.HTTP_201_CREATED)
#         return JSONResponse(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class PollList(APIView):
#     def get(self,request):
#         polls=Poll.objects.all()
#         data=PollSerializer(polls,many=True).data
#         return JSONResponse(data)

# class PollDetail(APIView):
#     def get(self,request,pk):
#         poll=get_object_or_404(Poll,pk=pk)
#         data=PollSerializer(poll).data
#         return JSONResponse(data)

# version 2
class Users(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class PollList2(generics.ListCreateAPIView):
    queryset=Poll.objects.all()
    serializer_class=PollSerializer

class PollDetail2(generics.RetrieveDestroyAPIView):
    queryset=Poll.objects.all()
    serializer_class=PollSerializer

class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        queryset=Choice.objects.filter(poll_id=self.kwargs['poll_pk'])
        return queryset
    serializer_class=ChoiceSerializer

class ChoiceDetail(generics.RetrieveDestroyAPIView):
    queryset=Choice.objects.all()
    serializer_class=ChoiceSerializer

class CreateVote(generics.CreateAPIView):
    serializer_class=VoteSerializer
    def post(self,request,poll_pk,choice_pk):
        voted_by=request.data.get('user')
        data={'poll':poll_pk,'choice':choice_pk,'user':voted_by}
        serializer=VoteSerializer(data=data)
        if serializer.is_valid():
            vote=serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class PollViewSet(viewsets.ModelViewSet):
    queryset=Poll.objects.all()
    serializer_class=PollSerializer

# API func ends


@login_required
def polls(request):
    polls=Poll.objects.all()
    search_keyword=''

    if 'title' in request.GET:
        polls=polls.order_by('text')
    if 'latest' in request.GET:
        polls=polls.order_by('-pub_date')
    if 'mine' in request.GET:
        polls=request.user.poll_set.all().order_by('text')
    if 'search' in request.GET:
        search_keyword=request.GET['search']
        polls=polls.filter(text__icontains=search_keyword)
    
    get_dict_copy=request.GET.copy()
    params=get_dict_copy.pop('page',True) and get_dict_copy.urlencode()

    
    paginator=Paginator(polls,3)
    page=request.GET.get('page')
    polls=paginator.get_page(page)

    context={
        'polls':polls,
        'params':params,
        'search':search_keyword,
    }
    return render(request,'poll/polls.html',context)

@login_required
def add_poll(request):
    if request.method=="POST":
        form=PollForm(request.POST)
        if form.is_valid():
            new_poll=form.save(commit=False)
            new_poll.owner=request.user
            new_poll.save()
            new_choice1=Choice(poll=new_poll,choice_text=form.cleaned_data['choice1']).save()
            new_choice2=Choice(poll=new_poll,choice_text=form.cleaned_data['choice2']).save()
            messages.success(request,"Poll and Choices added successfully",extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('poll:polls')
    else:
        form = PollForm()

    context={
        'form':form 
    }
    return render(request,'poll/add_poll.html',context)

@login_required
def edit_poll(request,poll_id):
    poll=get_object_or_404(Poll,id=poll_id)
    if request.user!=poll.owner:
        return HttpResponse("You're not authorized to view this page")
    
    if request.method=="POST":
        form=EditPollForm(request.POST,instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,"Poll edit successful",extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('poll:polls')
    else:
        form=EditPollForm(instance=poll)
        
    context={
        'poll':poll,
        'form':form
    }
    return render(request,'poll/edit_poll.html',context)

@login_required
def add_choice(request,poll_id):
    poll=get_object_or_404(Poll,id=poll_id)
    if request.user!=poll.owner:
        return HttpResponse("You're not authorized to view this page")
    
    if request.method=="POST":
        form=ChoiceForm(request.POST)
        if form.is_valid():
            new_choice=form.save(commit=False)
            new_choice.poll=poll
            new_choice.save()
            messages.success(request,"Choice added successfully",extra_tags='alert alert-success alert-dismissible fade show')
            return redirect(reverse('poll:details',kwargs={'poll_id':poll_id}))
    else:
        form=ChoiceForm()
        
    context={
        'poll':poll,
        'form':form
    }
    return render(request,'poll/add_choice.html',context)

@login_required
def edit_choice(request,choice_id):
    choice=get_object_or_404(Choice,id=choice_id)
    if request.user!=choice.poll.owner:
        return HttpResponse("You're not authorized to make changes to this choice")
    
    if request.method=="POST":
        form=ChoiceForm(request.POST,instance=choice)
        if form.is_valid():
            
            form.save()
            messages.success(request,"Choice edited successfully",extra_tags='alert alert-success alert-dismissible fade show')
            return redirect(reverse('poll:edit_poll',kwargs={'poll_id':choice.poll.id}))
    else:
        form=ChoiceForm(instance=choice)

    context={
        'form':form,
        'choice':choice
    }
    return render(request,'poll/edit_choice.html',context)

@login_required
def delete_choice(request,choice_id):
    choice=get_object_or_404(Choice,id=choice_id)
    if request.method=='POST':
        choice.delete()
        messages.success(request,"Choice deleted successfully",extra_tags='alert alert-success alert-dismissible fade show')
        return redirect(reverse('poll:edit_poll',kwargs={'poll_id':choice.poll.id}))
        
    context={
        'choice':choice,
        'poll':False
    }
    return render(request,'poll/confirm_delete.html',context)

@login_required
def delete_poll(request,poll_id):
    poll=get_object_or_404(Poll,id=poll_id)
    if request.method=='POST':
        poll.delete()
        messages.success(request,"Poll deleted successfully",extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('poll:polls')
        
    context={
        'choice':False,
        'poll':poll
    }
    return render(request,'poll/confirm_delete.html',context)

@login_required
def poll_detail(request,poll_id):
    poll=get_object_or_404(Poll,id=poll_id)
    user_can_vote = poll.user_can_vote(request.user) #return True if user can vote, else False
    context={
        'poll':poll,
        'user_can_vote':user_can_vote,
    }
    return render(request, 'poll/poll_details.html',context)

@login_required
def poll_vote(request,poll_id):
    choice_id=request.POST.get('choice')
    poll=Poll.objects.get(id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request,"You cannot vote twice on one Poll!")
        return redirect(reverse('poll:details',kwargs={'poll_id':poll.id}))


    if choice_id:
        choice=Choice.objects.get(id=choice_id)
        new_vote=Vote(user=request.user,poll=poll,choice=choice)
        new_vote.save()

        context={
            'choice' : choice,
            'poll':poll
        }
    else:
        messages.error(request,"No choice was chosen!")
        return HttpResponseRedirect(reverse('poll:details',args=(poll_id,)))
    return render(request,'poll/poll_results.html',context)