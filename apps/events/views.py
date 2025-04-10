from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Event
from .serializers import EventSerializer
from datetime import date
from rest_framework.permissions import IsAuthenticated
from apps.subscriptions.models import Subscription
class EventAPIView(APIView):
    """
    API View to handle event creation and editing.
    """

    def post(self, request):
        """Create a new event."""
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save event to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



    def patch(self, request, pk):
        """Edit an existing event."""
        event = get_object_or_404(Event, pk=pk)  
        serializer = EventSerializer(event, data=request.data, partial=True)  #
        if serializer.is_valid():
            serializer.save()  # Save changes
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventUserView(APIView):
    
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        """Retrieve events for authenticated users with an active Premium or Super Premium subscription."""
        allowed_plans = ["PREMIUM", "SUPER_PREMIUM"]

        # Check if the user has an active subscription
        has_valid_subscription = Subscription.objects.filter(
            user=request.user,
            plan__name__in=allowed_plans,  # Ensure the plan is Premium or Super Premium
            is_active=True,
            start_date__lte=date.today(),
            end_date__gte=date.today()
        ).exists()

        if not has_valid_subscription:
            return Response(
                {"error": "Access restricted to users with an active Premium or Super Premium subscription."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch events only if the user has an active subscription
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)