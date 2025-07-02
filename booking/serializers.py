from rest_framework import serializers
from pytz import timezone
from .models import FitnessClass, Booking

class FitnessClassSerializer(serializers.ModelSerializer):
    date_time_local = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = '__all__'

    def get_date_time_local(self, obj):
        request = self.context.get('request')
        tz = request.query_params.get('tz', 'Asia/Kolkata')  # default timezone is IST
        try:
            return obj.date_time.astimezone(timezone(tz)).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            return obj.date_time.astimezone(timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        fitness_class = data['fitness_class']
        if fitness_class.available_slots <= 0:
            raise serializers.ValidationError("No slots available for this class.")
        return data

    def create(self, validated_data):
        fitness_class = validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()
        return super().create(validated_data)
