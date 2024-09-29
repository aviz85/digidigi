from django.contrib import admin
from .models import Author, Book, Member, Loan

# Register Author model
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)

# Register Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'genre', 'available_copies')
    list_filter = ('genre', 'author', 'publication_date')
    search_fields = ('title', 'author__name', 'isbn')

# Register Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'membership_date')
    search_fields = ('user__username', 'user__email', 'phone_number')

# Register Loan model
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'loan_date', 'return_date', 'is_returned')
    list_filter = ('is_returned',)
    search_fields = ('book__title', 'member__user__username')

# Remove these lines as they're now redundant
# admin.site.register(Author)
# admin.site.register(Member)
# admin.site.register(Loan)
