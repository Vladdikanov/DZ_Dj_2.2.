from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        tags = []
        for form in self.forms:

            if self.deleted_forms and self._should_delete_form(form):
                continue
            # В form.cleaned_data будет словарь с данными
            tags.append(form.cleaned_data.get("tag"))# каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data.get("is_main") == True:
                count += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if count == 0:
            raise ValidationError(f'Укажите основной раздел')

        elif count > 1:
            raise ValidationError(f'Основным может быть только один раздел')
        for tag in tags:
            if tags.count(tag) > 1:
                raise ValidationError(f'Разделы не могут повторяться')


        return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "published_at"]
    inlines = [ScopeInline]
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
