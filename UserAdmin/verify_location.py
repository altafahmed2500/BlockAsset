from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

ALLOWED_COUNTRIES = ['US', 'IN']


def get_client_ip(request):
    # Handles proxy headers like X-Forwarded-For
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Error fetching IP location:", e)
    return None


class VerifyLocationView(APIView):
    def post(self, request):
        ip = get_client_ip(request)
        location_data = get_location_from_ip(ip)

        if not location_data:
            return Response({"error": "Could not determine location"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        country = location_data.get("country")
        city = location_data.get("city")

        if country in ALLOWED_COUNTRIES:
            return Response({
                "status": "verified",
                "country": country,
                "city": city,
                "ip": ip
            })
        else:
            return Response({
                "status": "denied",
                "country": country,
                "city": city,
                "ip": ip
            }, status=status.HTTP_403_FORBIDDEN)
