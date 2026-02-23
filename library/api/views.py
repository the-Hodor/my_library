from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..models import Book, Note
from .serializers import BookCreateSerializer, NoteSerializer, NoteCreateSerializer, MarkReadSerializer
from ..services.book_service import create_book, update_book, mark_book_as_read, get_user_books, get_user_book
from ..services.note_service import create_note
from drf_yasg.utils import swagger_auto_schema




class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: BookCreateSerializer(many=True)}
    )
    def get(self, request):
        books = get_user_books(request.user, request.GET)
        return Response(BookCreateSerializer(books, many=True).data)

    @swagger_auto_schema(
        request_body=BookCreateSerializer,
        responses={201: BookCreateSerializer}
    )
    def post(self, request):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = create_book(request.user, serializer.validated_data)
        return Response(BookCreateSerializer(book).data, status=status.HTTP_201_CREATED)


class BookUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=BookCreateSerializer,
        responses={200: BookCreateSerializer}
    )
    def put(self, request, pk):
        book = get_user_book(request.user, pk)

        serializer = BookCreateSerializer(instance=book, data=request.data)
        serializer.is_valid(raise_exception=True)
        update_book(book, serializer.validated_data)

        return Response(BookCreateSerializer(book).data)


class BookMarkReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=MarkReadSerializer)
    def post(self, request, pk):
        book = get_user_book(request.user, pk)
        mark_book_as_read(book)
        return Response({"status": "ok"})


class NoteCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=NoteCreateSerializer)
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = get_user_book(
            request.user,
            serializer.validated_data["book"].id
        )

        create_note(
            user=request.user,
            book=book,
            text=serializer.validated_data["text"],
        )

        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
