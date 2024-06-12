# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Document, FailedUpload
from .utils import extract_text_from_file


@shared_task
def process_document(doc_id):
    try:
        doc = Document.objects.get(id=doc_id)
        text = ""

        if doc.file:
            file_path = doc.file.path
            text = extract_text_from_file(file_path)

            doc.extracted_text = text
            doc.save()

        # Send a notification email after extraction
        send_success_email(doc)

    except Document.DoesNotExist:
        pass


def send_success_email(doc):
    try:
        subject = f'Data Extraction Complete for {doc.file.name}'
        message = f'The data extraction for your file {doc.file.name} has been completed successfully.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [doc.user.email]

        send_mail(subject, message, email_from, recipient_list)

        doc.email_sent = True
        doc.save()

        print(f"Email sent successfully for document: {doc.file.name}")
    except Exception as e:
        print(f"Error sending email for document {doc.file.name}: {e}")


@shared_task
def send_failed_upload_emails():
    # Get all failed uploads
    failed_uploads = FailedUpload.objects.all()

    for upload in failed_uploads:
        user = upload.user
        recipient_email = user.email
        try:
            # Compose the email subject and message
            subject = 'Upload Failed'
            message = f'Your upload for the file "{upload.file_name}" has failed. Please try again.'
            email_from = settings.EMAIL_HOST_USER
            recipient_email = user.email

            # Send the email
            send_mail(subject, message, email_from, recipient_email)
            print(f"Email sent successfully for failed document: {upload.file_name}")

            # Delete the failed upload record
            upload.delete()
        except Exception as e:
            print(f"Error sending email failed  for document:{upload.file_name}: {e}")
