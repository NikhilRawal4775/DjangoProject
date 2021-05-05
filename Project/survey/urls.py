from django.urls import path,include
from survey import views
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('',views.Home,name='home'),
    path('login/',views.Login,name='login'),
    path('signup/',views.Signup,name='signup'),
    path('account/',views.UserAccount,name='account'),
    path('logout/',views.Logout,name='logout'),
    path('profile/',views.Profile,name='profile'),
    path('survey/',views.SurveyPage,name='survey'),
    path('response/<int:id>',views.Response,name='response'),
    path('answer/<int:id>',views.Answer,name='answer'),
    path('presponse/<int:id>',views.PResponse,name='presponse'),
    path('pvote/<int:id>',views.PVote,name='pvote'),
    path('gallery/',views.Gallery,name='gallery'),
    path('votedata/<int:id>/',views.VoteData,name='votedata'),
    path('userpage/',views.UserPage,name='userpage'),
    path('deletequestion/<int:id>',views.DeleteQuestion,name='deletequestion'),
    path('deletepquestion/<int:id>',views.DeletePollQuestion,name='deletepquestion'),
    path('viewresponses/<int:id>',views.ResponsesOn,name='viewresponses'),
    path('pviewresponses/<int:id>',views.PResponsesOn,name='pviewresponses'),
    path('useranswer/<int:id>',views.AnswerOn,name='useranswer'),
    path('puseranswer/<int:id>',views.PAnswerOn,name='puseranswer'),
    path('addpollquestion',views.AddPollQuestion,name='addpollquestion'),
    path('addpolloption',views.AddPollOption,name='addpolloption'),
    path('dynamicpage/<int:id>',views.DynamicPage,name='dynamicpage'),
    path('adddynamicresponse/<int:id>',views.AddDynamicResponse,name='adddynamicresponse'),
    path('adddynamic/',views.AddDynamic,name='adddynamic'),
    path('adddynamicquestion/',views.AddDynamicQuestion,name='adddynamicquestion'),
    path('deletenews/<int:id>',views.DeleteNews,name='deletenews'),
    path('addnews/',views.AddNews,name='addnews'),
    path('adddynamicoption/',views.AddDynamicOption,name='adddynamicoption'),
    path('deletedynamic/<int:id>',views.DeleteDynamic,name='deletedynamic'),
    path('dynamicanswer/<int:id>',views.DynamicAnswer,name='dynamicanswer'),
    path('dynamicresponsepage/<int:id>',views.DynamicResponsePage,name='dynamicresponsepage'),
    path('dynamicviewanswer/<int:id>',views.DynamicViewAnswer,name='dynamicviewanswer'),
    path('myquestionlist/<int:id>',views.MyQuestionsList,name='myquestionlist'),
    path('deletemyquestion/<int:id>',views.DeleteMyQuestion,name='deletemyquestion'),
    
    #path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),



]
