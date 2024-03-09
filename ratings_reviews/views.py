# ratings_reviews/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ReviewForm
from .models import Review

@login_required
def post_review(request):
    if Review.objects.filter(reviewer=request.user).exists():
        # If user has already posted a review, redirect them to edit it
        return redirect('edit_review', review_id=request.user.review_set.first().id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'ratings_reviews/post_review.html', {'form': form})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        if request.user.is_staff or request.user == review.reviewer:
            review.delete()
            messages.success(request, 'Review deleted successfully!')
            return redirect('home')
        else:
            messages.error(request, 'You are not authorized to delete this review.')
            return redirect('home')
    return render(request, 'ratings_reviews/delete_review.html', {'review': review})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'ratings_reviews/edit_review.html', {'form': form, 'review': review})

@login_required
def user_reviews(request):
    user_reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'ratings_reviews/user_reviews.html', {'user_reviews': user_reviews})
