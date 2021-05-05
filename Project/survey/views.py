from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from .forms import CreateUserForm,MyAccount,ResponseForm,QuestionForm,PollForm,PollOptionForm,DynamicForm,DynamicQuestionForm,GalleryForm,DynamicOptionForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from survey.models import Account,Question,TSurvey,PQuestion,POptions,MyGallery,Dynamic,DynamicQuestion,DynamicResponses,DynamicOptions
from django.http import JsonResponse
from .decorators import unauthenticated_user,allowed_users,admin_only
import os
"""
from io import BytesIO
from xhtml2pdf import pisa
from django.views import View
from django.template.loader import get_template
"""
# Create your views here.
def Home(request):
    return render(request,'home.html',{})

@unauthenticated_user
def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            #return render(request,'account.html',{'me':user})
            return redirect('account')
        else:
            messages.info(request,"Check Your Credentials")
            return render(request,'login.html',{})
    return render(request,'login.html',{})
@unauthenticated_user
def Signup(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            a=User.objects.get(username=username)
            Account.objects.create(user=a)
            messages.success(request,"Hey, "+str(username)+"\nYou can login now")
            return redirect('login')
    return render(request,'signup.html',{'form':form})

@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')

@admin_only
def UserAccount(request):
    return redirect("/survey/")

@login_required(login_url='login')
def Profile(request):
    account=request.user.account
    form=MyAccount(instance=account)
    if request.method=='POST':
        form=MyAccount(request.POST,request.FILES,instance=account)
        if form.is_valid():
            form.save()
    return render(request,'profile.html',{'form':form})

@login_required(login_url='login')
def SurveyPage(request):
    q=Question.objects.all()
    pq=PQuestion.objects.all()
    dy=Dynamic.objects.all()
    return render(request,'survey.html',{'questions':q,'pquestions':pq,'dy':dy})

@login_required(login_url='login')
def Response(request,id):
    q=Question.objects.get(pk=id)
    ans=TSurvey.objects.filter(ques=q)
    return render(request,'response.html',{'res':ans,'q':q})

@login_required(login_url='login')
def Answer(request,id):
    q=Question.objects.get(pk=id)
    if request.method=="POST":
        a=User.objects.get(username=request.user)
        form=ResponseForm(request.POST)
        if form.is_valid():
            l=form.cleaned_data['res']
            TSurvey.objects.create(user=a,ques=q,res=l)
            return redirect('survey')
    form=ResponseForm()
    return render(request,'answer.html',{'q':q,'form':form})

@login_required(login_url='login')
def PResponse(request,id):
    q=PQuestion.objects.get(pk=id)
    opt=POptions.objects.filter(ques=q)
    return render(request,'presponse.html',{'pquestion':q,'poption':opt})

@login_required(login_url='login')
def PVote(request,id):
    q=PQuestion.objects.get(pk=id)
    loc=q.id
    opt=POptions.objects.filter(ques=q)
    if request.method=="POST":
        o=request.POST.get("vote")
        for i in opt:
            if i.option==o:
                i.option_count+=1
                i.save()
                return redirect('/survey/')
    return render(request,'pvote.html',{'q':q,'poption':opt})

def Gallery(request):
    p=MyGallery.objects.all()
    return render(request,'gallery.html',{'p':p})
    
@login_required(login_url='login')
def VoteData(request,id):
    vote=[]
    q=PQuestion.objects.get(pk=id)
    opt=POptions.objects.filter(ques=q)
    for i in opt:
        vote.append({i.option:i.option_count})
    return JsonResponse(vote,safe=False)
@login_required(login_url='login')
def UserPage(request):
    if request.method=="POST":
        QForm=QuestionForm(request.POST)
        if QForm.is_valid():
            QForm.save()
        return redirect('survey')
    QForm=QuestionForm()
    PForm=PollForm()
    POForm=PollOptionForm()
    DForm=DynamicForm()
    DQForm=DynamicQuestionForm()
    GForm=GalleryForm()
    DOForm=DynamicOptionForm()
    GObj=MyGallery.objects.all()
    return render(request,'user.html',{'qform':QForm,'pform':PForm,'poform':POForm,'dform':DForm,'dqform':DQForm,'gform':GForm,'gobj':GObj,'doform':DOForm})

@login_required(login_url='login')
def DeleteQuestion(request,id):
    p=Question.objects.get(pk=id)
    p.delete()
    return redirect('survey')

@login_required(login_url='login')
def DeletePollQuestion(request,id):
    p=PQuestion.objects.get(pk=id)
    p.delete()
    return redirect('survey')

@login_required(login_url='login')
def ResponsesOn(request,id):
    p=Question.objects.get(pk=id)
    if p.view_response:
        p.view_response=False
    else:
        p.view_response=True
    p.save()
    return redirect('survey')

@login_required(login_url='login')
def PResponsesOn(request,id):
    p=PQuestion.objects.get(pk=id)
    if p.view_response:
        p.view_response=False
    else:
        p.view_response=True
    p.save()
    return redirect('survey')

def AnswerOn(request,id):
    p=Question.objects.get(pk=id)
    if p.user_response:
        p.user_response=False
    else:
        p.user_response=True
    p.save()
    return redirect('survey')

@login_required(login_url='login')
def PAnswerOn(request,id):
    p=PQuestion.objects.get(pk=id)
    if p.user_response:
        p.user_response=False
    else:
        p.user_response=True
    p.save()
    return redirect('survey')

@login_required(login_url='login')
def AddPollQuestion(request):
    if request.method=='POST':
        PForm=PollForm(request.POST)
        if PForm.is_valid():
            PForm.save()
        return redirect('userpage')
    PForm=PollForm()
    return redirect('userpage')

@login_required(login_url='login')
def AddPollOption(request):
    if request.method=='POST':
        POForm=PollOptionForm(request.POST)
        if POForm.is_valid():
            POForm.save()
        return redirect('userpage')
    POForm=PollForm()
    return redirect('userpage')
@login_required(login_url='login')
def DynamicPage(request,id):
    fname=Dynamic.objects.get(pk=id)
    questionlist=DynamicQuestion.objects.filter(form=fname)
    op=list()
    for i in questionlist:
        c=DynamicOptions.objects.filter(form=i)
        op.append(c)
    return render(request,'dynamic.html',{'fname':fname,'qlist':questionlist,'id':id,'op':op})

@login_required(login_url='login')
def AddDynamicResponse(request,id):
    fname=Dynamic.objects.get(pk=id)
    questionlist=DynamicQuestion.objects.filter(form=fname)
    if request.method=="POST":
        a=User.objects.get(username=request.user)
        for i in questionlist:
            ans=request.POST.get(str(i.id))
            s=DynamicResponses.objects.create(form=i,user=a,res=ans)
            s.save()
        return redirect('survey')
    return redirect('dynamicpage'+str(id))
@login_required(login_url='login')
def AddDynamic(request):
    if request.method=='POST':
        DForm=DynamicForm(request.POST)
        if DForm.is_valid():
            DForm.save()
        return redirect('userpage')
    DForm=DynamicForm()
    return redirect('userpage')
@login_required(login_url='login')
def AddDynamicQuestion(request):
    if request.method=='POST':
        DQForm=DynamicQuestionForm(request.POST)
        if DQForm.is_valid():
            DQForm.save()
        return redirect('userpage')
    DQForm=DynamicQuestionForm()
    return redirect('userpage')

@login_required(login_url='login')
def DeleteNews(request,id):
    s=MyGallery.objects.get(pk=id)
    s.delete()
    return redirect('userpage')

@login_required(login_url='login')
def AddNews(request):
    if request.method=='POST':
        GForm=GalleryForm(request.POST,request.FILES)
        if GForm.is_valid():
            GForm.save()
        return redirect('userpage')
    GForm=GalleryForm()
    return redirect('userpage')

@login_required(login_url='login')
def AddDynamicOption(request):
    if request.method=='POST':
        DOForm=DynamicOptionForm(request.POST,request.FILES)
        if DOForm.is_valid():
            DOForm.save()
        return redirect('userpage')
    DOForm=DynamicOptionForm()
    return redirect('userpage')

@login_required(login_url='login')
def DeleteDynamic(request,id):
    s=Dynamic.objects.get(pk=id)
    s.delete()
    return redirect('survey')

@login_required(login_url='login')
def DynamicAnswer(request,id):
    p=Dynamic.objects.get(pk=id)
    if p.user_response:
        p.user_response=False
    else:
        p.user_response=True
    p.save()
    return redirect('survey')

@login_required(login_url='login')
def DynamicResponsePage(request,id):
    fname=Dynamic.objects.get(pk=id)
    questionlist=DynamicQuestion.objects.filter(form=fname)
    k=list()
    for i in questionlist:
        f=DynamicResponses.objects.filter(form=i)
        for j in f:
                k.append(j)
    print(f)
    return render(request,'dresponse.html',{'fname':fname,'qlist':questionlist,'rlist':k})

@login_required(login_url='login')
def DynamicViewAnswer(request,id):
    p=Dynamic.objects.get(pk=id)
    if p.view_response:
        p.view_response=False
    else:
        p.view_response=True
    p.save()
    return redirect('survey')

@login_required(login_url='login')
def MyQuestionsList(request,id):
    fname=Dynamic.objects.get(pk=id)
    qlist=DynamicQuestion.objects.filter(form=fname)
    return render(request,'questions.html',{'fname':fname,'qlist':qlist})

@login_required(login_url='login')
def DeleteMyQuestion(request,id):
    p=DynamicQuestion.objects.get(pk=id)
    p.delete()
    return redirect('survey')

"""
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('survey.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        """