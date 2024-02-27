from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

def create_review(request, reviewed_user_id):
    reviewed_user = User.objects.get(pk=reviewed_user_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'ratings_reviews/create_review.html', {'form': form, 'reviewed_user': reviewed_user})
