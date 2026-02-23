from rest_framework import serializers
from ..models import Book, Note



class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "status", "read_date", "genres"]


class NoteCreateSerializer(serializers.Serializer):
    text = serializers.CharField()

class MarkReadSerializer(serializers.Serializer):
    status = serializers.CharField()


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "text",
            "book",
        ]

