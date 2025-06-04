from django.http import JsonResponse
from .tasks import collect_wearable_data


def wearable_data_view(request):
    try:
        # Collect wearable data and summary
        wearable_data_df, summary = collect_wearable_data()

        # Convert DataFrame to JSON
        data_json = wearable_data_df.to_dict(orient='records')

        # Return the JSON response
        return JsonResponse({
            "data": data_json,
            "summary": summary,  # Assuming this is a single string summary
        })

    except Exception as e:
        # Handle errors gracefully
        return JsonResponse({
            "error": str(e),
            "message": "An error occurred while processing wearable data."
        }, status=500)
