path('edit', views.edit, name="edit")
def edit(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        form2 =ProfileCreationForm(data=request.POST)
        if form.is_valid() and form2.is_valid():
            form.save()
            user_id = User.objects.last()
            postcode = form2['postcode'].value()
            form2.save(user_id, postcode)
            return redirect('/users/login/') #TODO:Check if this is the right path
    return render(request, 'users/edit.html', {
        'form': UserCreationForm(),
        'form2': ProfileCreationForm()
    }),