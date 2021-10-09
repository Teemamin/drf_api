from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        """
         the setUp method that will automatically  run before every test method in the class
         create a user that we can reference  later on in all the tests inside this class.  
         We’ll use this user’s credentials when  we need to log in to create a post.  
         We’ll also need this user when we manually  create a post and need to set its owner
        """
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        """
         To test protected routes (which are routes  that require the user to be logged in),  
         we’ll have to log in first using the  APITest client. To do this we would  
         use the client.login method and pass in the  username and password from the setUp method.
        """
        self.client.login(username='adam', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        """
         the setUp method that will automatically  run before every test method in the class
         create a user that we can reference  later on in all the tests inside this class.  
         We’ll use this user’s credentials when  we need to log in to create a post.  
         We’ll also need this user when we manually  create a post and need to set its owner
        """
        adam = User.objects.create_user(username='adam', password='pass')
        susu = User.objects.create_user(username='susu', password='pass')
        Post.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Post.objects.create(
            owner=susu, title='another title', content='susus content'
        )

    def test_user_can_retrieve_post_with_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_cannot_retrieve_post_with_invalid_id(self):
        response = self.client.get('/posts/12/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_post_they_own(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'changed title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(response.data['title'], 'changed title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_post_they_own(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'changed title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(response.data['title'], 'changed title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_cannot_update_post_they_dont_own(self):
        self.client.login(username='susu', password='pass')
        response = self.client.put('/posts/1/', {'title': 'make another title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


