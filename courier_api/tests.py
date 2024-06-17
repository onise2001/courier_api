from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import Parcel, DeliveryProof
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from users.serializers import CustomUserSerializer
# Create your tests here.


class ParcelApiTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        
        self.test_customer = CustomUser.objects.create_user(username='customer', password='test1234', role='Customer')
        self.test_customer_1 = CustomUser.objects.create_user(username='customer1', password='test1234', role='Customer')
        self.test_courier = CustomUser.objects.create_user(username='courier', password='test1234', role='Courier')
        self.test_admin = CustomUser.objects.create_user(username='admin', password='test1234', role='Admin')
        
        Parcel.objects.create(title='test parcel', description='test parcel', reciever_name='test reciever', reciever_address='test address', reciever=self.test_customer)
        Parcel.objects.create(title='test parcel 1', description='test parcel 1', reciever_name='test reciever 1', reciever_address='test address 1', reciever=self.test_customer_1)

    
    def test_parcel_list(self):
        url = reverse('parcels-list')
        auth_url = reverse('login')
       
        # Test GET request with an unauthenticated user
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        
        #Test GET request with an authenticated user with the role of Customer
        customer_token = self.client.post(auth_url, {'username': 'customer', 'password': 'test1234'},format='json')
        self.assertEqual(customer_token.status_code, status.HTTP_200_OK)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ customer_token.json()['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all([parcel['reciever']['id'] == self.test_customer.id for parcel in response.json()]))
        self.client.credentials()

        # Test GET request with an authenticated user with the role of Courier
        courier_token = self.client.post(auth_url, {'username': 'courier', 'password': 'test1234'},format='json')
        self.assertEqual(customer_token.status_code, status.HTTP_200_OK)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ courier_token.json()['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.credentials()

        # Test GET request with an authenticated user with the role of Admin
        admin_token = self.client.post(auth_url, {'username': 'admin', 'password': 'test1234'},format='json')
        self.assertEqual(customer_token.status_code, status.HTTP_200_OK)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+ admin_token.json()['access'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.credentials()



    
    # def test_create_parcel(self):
    #     url = reverse('parcels-list')
    
    #     # Test POST request with an unauthenticated user
    #     response = self.client.post(url, { 'title': 'test parcel 2', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2'}, format='json')
    #     self.assertEqual(response.status_code, 401)
        
    #     # Test POST request with an authenticated user with the role of Customer
    #     self.client.force_authenticate(user=self.test_customer)
    #     response = self.client.post(url,{ 'title': 'test parcel 2', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2'}, format='json')
    #     self.assertEqual(response.status_code, 201)

    #     # Test POST request with an authenticated user with the role of Courier
    #     self.client.force_authenticate(user=self.test_courier)
    #     response = self.client.post(url,{ 'title': 'test parcel 2', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2'}, format='json')
    #     self.assertEqual(response.status_code, 403)

    #     # Test POST request with an authenticated user with the role of Admin
    #     self.client.force_authenticate(user=self.test_admin)
    #     response = self.client.post(url, { 'title': 'test parcel 2', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2'}, format='json')
    #     self.assertEqual(response.status_code, 403)



   
    
    def test_update_parcel(self):
        url = '/parcel/1'
        auth_url = reverse('login')
        user_serializer = CustomUserSerializer(self.test_customer)

    
                
        
        # Test PUT request with an unauthenticated user
        response = self.client.put(url, { 'id': 3, 'title': 'test parcel update', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2','reciever': user_serializer.data}, format='json')
        self.assertEqual(response.status_code, 401)
        
        # Test PUT request with an authenticated user with the role of Customer, who is not the owner of this Parcel object
       
        self.client.force_authenticate(user=self.test_customer_1)

        response = self.client.put(url,{ 'id': 1, 'title': 'test parcel update', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2', 'reciever': user_serializer.data}, format='json')
        self.assertEqual(response.status_code, 404)
        self.client.force_authenticate(user=None)

       
        

        # Test PUT request with an authenticated user with the role of Customer, who is the owner of this Parcel object
        
        self.client.force_authenticate(user=self.test_customer)

        response = self.client.put(url,{ 'id': 1, 'title': 'test parcel update', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2', 'reciever': user_serializer.data}, format='json')
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(user=None)


        # Test PUT request with an authenticated user with the role of Courier
        
        self.client.force_authenticate(user=self.test_courier)
        response = self.client.put(url,{ 'id': 1, 'title': 'test parcel update', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2', 'reciever': self.test_customer.id}, format='json')
        self.assertEqual(response.status_code, 404)
        self.client.force_authenticate(user=None)


        # Test PUT request with an authenticated user with the role of Admin
        
        self.client.force_authenticate(user=self.test_courier)
        response = self.client.put(url, { 'id': 1, 'title': 'test parcel update', 'description':'test parcel 2', 'reciever_name':'test reciever 2', 'reciever_address':'test address 2', 'reciever': self.test_customer.id}, format='json')
        self.assertEqual(response.status_code, 404)
        self.client.force_authenticate(user=None)





