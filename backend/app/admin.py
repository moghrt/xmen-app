from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from app.models import User, Post, Like, Comment, Room, Message

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'caption', 'is_active', 'is_staff', 'avatar')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'caption', 'is_staff', 'avatar', 'user_type', 'tags')
    list_filter = ('is_staff', 'tags')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar', 'tags')}),
        ('Personal info', {'fields': ('name', 'caption',)}),
        ('Permissions', {'fields': ('is_staff', 'user_type')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'caption', 'password1', 'password2', 'avatar', 'tags')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

class MessageAdmin(admin.ModelAdmin):
    list_filter = ['room']


# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Room)
admin.site.register(Message, MessageAdmin)
