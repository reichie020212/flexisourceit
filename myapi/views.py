from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework import views
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.models import User
from . import serializers
from .models import Account
from .models import Stock


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, *args, **kwargs)


class RegistrationView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            user = User(username=username)
            user.set_password(password)
            user.save()
            Account.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
            )
            return Response(
                'User has been created',
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StockView(views.APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        pass

    def post(self, request, *args, **kwargs):
        serializer = serializers.StockSerializer(
            data=request.data,
            instance=self.get_object(),
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Stock has been created'
            if self.get_object():
                message = 'Stock has been updated'
            return Response(
                message,
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class StockUpdateView(StockView):
    """Update a Stock"""
    def get_object(self):
        return Stock.objects.get(id=self.kwargs.get('pk'))


class StockCreateView(StockView):
    """Create a new Stock"""
    def get_object(self):
        return None


class StockListView(views.APIView):
    """List all Stocks"""
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        return Response(
            Stock.objects.all().values('id', 'name', 'price'),
            status=status.HTTP_200_OK,
        )


class TransactionStockSerializer(views.APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    transaction_serializer = None

    def post(self, request, *args, **kwargs):
        serializer = self.transaction_serializer(
            data=request.data,
            context={
                'request': request
            },
        )
        if serializer.is_valid(raise_exception=True):
            user = request.user
            my_stock = serializer.save(user.account)
            return Response(
                {
                    'stock_id': my_stock.stock.id,
                    'stock_name': my_stock.stock.name,
                    'stock_quantity': my_stock.quantity,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class BuyStockView(TransactionStockSerializer):
    """Buy a Stock"""
    transaction_serializer = serializers.BuyStockSerializer


class SellStockView(TransactionStockSerializer):
    """Sell a Stock"""
    transaction_serializer = serializers.SellStockSerializer


class MyStockListView(views.APIView):
    """List all of the your account's Stocks"""
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        return Response(
            request.user.account.get_stocks().values('stock__name', 'quantity'),
            status=status.HTTP_200_OK,
        )


class MyStockTotalInvestedView(views.APIView):
    """Get total amount invested on a specific Stock"""
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        stock_name = self.request.GET.get('stock_name') or None
        if not stock_name:
            return Response(
                "stock_name is required",
                status=status.HTTP_400_BAD_REQUEST,
            )
        stock = Stock.objects.filter(name=stock_name).first()

        if not stock:
            return Response(
                "There's no Stock named %s" % (stock_name),
                status=status.HTTP_400_BAD_REQUEST,
            )

        account = request.user.account
        my_stock = account.mystock_set.filter(stock=stock).first()

        if not my_stock:
            return Response(
                "You do not have a stock named %s" % (stock_name),
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'stock': stock_name,
                'total': my_stock.get_total_invested(),
            },
            status=status.HTTP_200_OK,
        )
