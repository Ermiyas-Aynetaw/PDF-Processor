import fitz  # PyMuPDF
import nltk
import re
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .models import DocumentAnalysis
from .serializers import DocumentAnalysisSerializer
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


class DocumentAnalysisView(views.APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "PDF file required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Extract text from PDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # Define patterns for phone numbers and email addresses
        phone_number_pattern = r"\b(?:\d[ -]?)?(?:(?:\(\d{3}\)|\d{3})[ -]?)?\d{3}[ -]?\d{4}\b"
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        # Remove phone numbers and email addresses from the text
        text = re.sub(phone_number_pattern, "", text)
        text = re.sub(email_pattern, "", text)

        # Process text to find nouns and verbs
        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)

        # Remove tokens containing special characters including underscores
        cleaned_tokens = [word for word, tag in tagged_tokens if not re.match(r'^[^\w\s]+$', word)]

        nouns = ", ".join([word for word, tag in tagged_tokens if tag.startswith("NN")])
        verbs = ", ".join([word for word, tag in tagged_tokens if tag.startswith("VB")])

        # Save to database
        serializer = DocumentAnalysisSerializer(
            data={
                "email": request.data.get("email"),
                "content": ' '.join(cleaned_tokens),
                "nouns": nouns,
                "verbs": verbs,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, "index.html")
