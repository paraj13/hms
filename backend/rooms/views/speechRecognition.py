import os
import speech_recognition as sr
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def voice_to_text(request):
    try:
        if request.method == "POST":
            # Check if audio file exists in request
            if 'audio' not in request.FILES:
                return JsonResponse({"error": "No audio file provided"}, status=400)

            # Get uploaded file
            audio_file = request.FILES['audio']

            # Initialize recognizer
            r = sr.Recognizer()

            # Use AudioFile directly with Django InMemoryUploadedFile
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)

            # Convert to text
            text = r.recognize_google(audio_data)

            return JsonResponse({"transcription": text})

        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    except sr.UnknownValueError:
        return JsonResponse({"error": "Could not understand the audio"}, status=400)
    except sr.RequestError as e:
        return JsonResponse({"error": f"Google API error: {e}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
