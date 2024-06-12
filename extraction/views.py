from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm
from .models import Document, FailedUpload
from .tasks import process_document
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages, auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def signin(request):
    if request.method == "POST":
        form_error = False
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)

                # Store user information in session
                request.session['username'] = user.username
                request.session['user_id'] = user.id
                # You can store more information in the session as needed

                list(messages.get_messages(request))
                messages.success(request, f"Hello <strong>{request.user.username}</strong> You have been logged in")
                return redirect('extraction:documents')
        else:
            form_error = True
            for key, msg in list(form.errors.items()):
                error_message = list(msg)
                messages.error(request, error_message[0])
                return redirect('/')

    form = UserLoginForm()

    return render(request, 'extract/index.html', {'form': form})


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} created successfully.")
            return redirect('extraction:documents')
        else:
            for key, msg in list(form.errors.items()):
                error_message = list(msg)
                messages.error(request, error_message[0])
            return redirect('/')
    else:
        form = UserRegistrationForm()

    return render(request, 'extract/index.html', {'form': form})


def logout(request):
    user = request.user.username
    request.session.clear()
    auth.logout(request)
    list(messages.get_messages(request))
    messages.success(request, f"Dear user {user}, you have been logged out successfully.")
    return redirect('extraction:signin')


@login_required
def upload_file(request):
    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('file')

        for uploaded_file in uploaded_files:
            # Save each uploaded file
            doc = Document(user=request.user, file=uploaded_file)
            doc.save()
            try:
                # Determine file type
                file_extension = uploaded_file.name.lower().split('.')[-1]
                text_file_extensions = ['pdf', 'txt', 'doc', 'docx']

                if file_extension in text_file_extensions:
                    # For text-based files, process using Celery
                    process_document.delay(doc.id)
                else:
                    # For non-text-based files, just save the file URL
                    doc.file_url = doc.file.url
                    doc.save()

                messages.success(request, f"File '{uploaded_file.name}' uploaded successfully.")
            except Exception as e:
                # If upload fails, create a FailedUpload record
                FailedUpload.objects.create(user=request.user, file_name=uploaded_file.name)
                messages.error(request, f"Failed to upload file '{uploaded_file.name}'.")
                print(e)

        return redirect('extraction:documents')  # Adjust the namespace if necessary

    return render(request, 'extract/document_list.html')


@login_required(login_url="extraction:signin")
def document_list(request):
    data = Document.objects.filter(user__id=request.user.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    context = {
        'documents': data,
    }
    return render(request, 'extract/document_list.html', context)
