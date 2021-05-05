from django.contrib import admin
from survey.models import Account,Question,TSurvey,PQuestion,POptions,MyGallery,Dynamic,DynamicQuestion,DynamicResponses,DynamicOptions

# Register your models here.
admin.site.register(Account)
admin.site.register(TSurvey)
admin.site.register(Question)
admin.site.register(MyGallery)
admin.site.register(POptions)
admin.site.register(PQuestion)
admin.site.register(Dynamic)
admin.site.register(DynamicQuestion)
admin.site.register(DynamicResponses)
admin.site.register(DynamicOptions)

