from django import forms
from django.contrib.admin import AdminSite
from django.test import RequestFactory

from src.apps.common.admin import ModelAdmin
from src.apps.users.models import User


class TestModelAdmin:
    """Test custom `ModelAdmin`."""

    def test_get_help_texts(self) -> None:
        class TestAdmin(ModelAdmin):
            help_texts = {"field": "Some temporary field for testing."}

        admin = TestAdmin(User, AdminSite())
        help_texts = admin.get_help_texts()

        assert help_texts.keys() == {"id", "field"}
        assert help_texts["field"] == "Some temporary field for testing."

    def test_get_help_texts_default(self) -> None:
        admin = ModelAdmin(User, AdminSite())

        assert admin.get_help_texts().keys() == {"id"}

    def test_get_form(self, rf: RequestFactory) -> None:
        class TestForm(forms.ModelForm):
            class Meta:
                model = User
                fields = ("id",)  # Don't care
                help_texts = {"field": "Should override me!"}

        class TestAdmin(ModelAdmin):
            form = TestForm
            help_texts = {
                "field": "Overridden help text.",
                "another_field": "Some function or property field that need help texts",
            }

        admin = TestAdmin(User, AdminSite())
        request = rf.get(path="/")
        form = admin.get_form(request)
        help_texts = form._meta.help_texts

        assert isinstance(help_texts, dict)
        assert help_texts.keys() == {"id", "field", "another_field"}
        assert help_texts["field"] == "Overridden help text."
        assert help_texts["another_field"] == "Some function or property field that need help texts"
