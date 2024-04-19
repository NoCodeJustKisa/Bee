from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from beehive.models import User, Activity, Mood, Note, Message, Record
# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Activity)
admin.site.register(Mood)
admin.site.register(Note, NoteAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Record, RecordAdmin)



#бля я ебу чоли какова хуя в админке не пояявлется мой экстендед юзер sooooqa ну хоть тзшка есть