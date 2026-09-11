import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from livekit import api
from django.shortcuts import render

def home_classroom(request):
    return render(request, 'index.html')

def get_livekit_token(request): 
    """
    Rest API Endpoints: Generate a secure, short-lived video room access token.
    Expects GET parameters: ?room=python-101&name=Alex
    """
    # 1. Grab parameters sent from the frontend
    room_name = request.GET.get('room')
    participant_name = request.GET.get('name')

    # Validation: If the browser forgot to send room or name, reject it
    if not room_name or not participant_name:
        return HttpResponseBadRequest("Missing 'room' or 'name' parameters.")
    
    try:
        # 2. Initialize the Token Maker using our secret backend settings
        token = api.AccessToken(
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET
        )

        # 3. Define the user's identity inside the call
        token.with_identity(participant_name)
        token.with_name(participant_name)

        # 4. Set Permissions (Grants): Grant permission to JOIN the specific room
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room_name
        ))

        # 5. Convert the token payload into a clean, encrypted JWT string
        token_jwt = token.to_jwt()

        # 6. Send it back to the browser as a standard JSON object
        return JsonResponse({
            'token': token_jwt,
            'server_url': settings.LIVEKIT_URL
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

