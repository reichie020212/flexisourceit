from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MyStock
from .models import Stock


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        errors = {}

        if User.objects.filter(username=username).exists():
            errors.update({'username': 'Username is already used.'})
        if len(password) < 4:
            errors.update(
                {'password': 'Password must have a length of 4 or more.'})
        if password != confirm_password:
            errors.update({'confirm_password': 'Password and Confirm Password do not match.'})

        if errors:
            raise serializers.ValidationError(errors)

        return data


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['name', 'price']


class TransactionStockSerializer(serializers.Serializer):
    name = serializers.CharField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        name = data.get('name')
        quantity = data.get('quantity')

        stock = Stock.objects.filter(name=name).first()

        errors = {}
        if not stock:
            errors.update({'name': 'No stock named %s' % (name)})

        if quantity < 0:
            errors.update({'quantity': 'Quantity must be greater than or equal to 1'})

        if errors:
            raise serializers.ValidationError(errors)

        return data


class BuyStockSerializer(TransactionStockSerializer):

    def save(self, account):
        name = self.validated_data.get('name')
        quantity = self.validated_data.get('quantity')
        my_stock = MyStock.objects.filter(stock__name=name, account=account).first()
        if not my_stock:
            stock = Stock.objects.filter(name=name).first()
            my_stock = MyStock.objects.create(stock=stock, quantity=quantity, account=account)
        else:
            my_stock.quantity += quantity
            my_stock.save()
        return my_stock


class SellStockSerializer(TransactionStockSerializer):

    def validate(self, data):
        super().validate(data)
        name = data.get('name')
        quantity = data.get('quantity')
        stock = Stock.objects.filter(name=name).first()
        account = self.context['request'].user.account

        if not account.mystock_set.filter(stock=stock):
            raise serializers.ValidationError({'name': 'You do not have a stock named %s' % (name)})

        my_stock = account.mystock_set.filter(stock=stock).first()

        if my_stock.quantity < quantity:
            raise serializers.ValidationError({'quantity': 'Quantity must not exceed to %s' % (my_stock.quantity)})

        return data

    def save(self, account):
        name = self.validated_data.get('name')
        quantity = self.validated_data.get('quantity')
        my_stock = MyStock.objects.filter(stock__name=name, account=account).first()
        my_stock.quantity -= quantity
        my_stock.save()
        return my_stock
