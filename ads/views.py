from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

import csv
import json

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView

from ads.models import Ads, Categories, User, City
from main_avito import settings


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def get(request):
    # Convert to JSON
    # with open('./datasets/ads.csv', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     rows = list(reader)
    # with open('./datasets/ads.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(rows, ensure_ascii=False, indent=4))
    # with open('./datasets/categories.csv', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     rows = list(reader)
    # with open('./datasets/categories.json', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(rows, ensure_ascii=False, indent=4))

    # Load data into model
    # with open('./ads/categories.json', encoding='utf-8') as data_file:
    #     json_data = json.loads(data_file.read())
    #     for item_data in json_data:
    #         item = Categories()
    #         item.id = item_data['id']
    #         item.name = item_data['name']
    #         item.save()
    # with open('./ads/ads.json', encoding='utf-8') as data_file:
    #     json_data = json.loads(data_file.read())
    #     for item_data in json_data:
    #         item = Ads()
    #         item.id = item_data['id']
    #         item.name = item_data['name']
    #         item.author = item_data['author']
    #         item.price = item_data['price']
    #         item.description = item_data['description']
    #         item.address = item_data['address']
    #         item.is_published = str2bool(item_data['is_published'])  # .replace("“", "")
    #         item.save()
    return JsonResponse({"status": "ok"}, status=200)


# Categories section
@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Categories
    queryset = Categories.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # cats = Categories.objects.all()
        # cats = self.object_list.all()
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_list = paginator.get_page(page_number)
        cat_list = []
        for cat_item in page_list:
            cat_list.append({
                "id": cat_item.id,
                "name": cat_item.name
            })
        response = {
            "items": cat_list,
            "page_number": paginator.num_pages,
            "total": page_list.paginator.count
        }
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            cat_item = Categories()
            cat_item.name = data["name"]
            cat_item.save()
            return JsonResponse({"id": cat_item.id, "name": cat_item.name}, status=201)
        except Exception:
            return JsonResponse({"error": "incorrect payload"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetail(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            # cat_item = Categories.objects.get(pk=pk)
            cat_item = self.get_object()
            cat_list = []
            cat_list.append({
                "id": cat_item.id,
                "name": cat_item.name
            })
            return JsonResponse(cat_list, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
        except Categories.DoesNotExist:
            return JsonResponse({"error": "do not exist"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdate(UpdateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()
        return JsonResponse({"id": self.object.id, "name": self.object.name}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDelete(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})


# Ads section
@method_decorator(csrf_exempt, name='dispatch')
class Ad(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        # ads = Ads.objects.all()
        # ads = self.object_list.all()
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_list = paginator.get_page(page_number)
        ads_list = []
        for ad_item in page_list:
            ads_list.append({
                "id": ad_item.id,
                "name": ad_item.name,
                "author": ad_item.author,
                "price": ad_item.price,
                "description": ad_item.description,
                "address": ad_item.address,
                "is_published": ad_item.is_published,
                "poster": ad_item.poster.url if ad_item.poster else ''
            })
        response = {
            "items": ads_list,
            "page_number": paginator.num_pages,
            "total": page_list.paginator.count
        }
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ad_item = Ads()
            ad_item.id = data.get('id', None)
            ad_item.name = data.get("name", None)
            ad_item.author = data.get("author", None)
            ad_item.price = data.get("price", None)
            ad_item.description = data.get("description", None)
            ad_item.address = data.get("address", None)
            ad_item.is_published = data.get("is_published", False)
            ad_item.save()
            return JsonResponse({"id": ad_item.id, "name": ad_item.name, "author": ad_item.author}, status=201)
        except Exception:
            return JsonResponse({"error": "incorrect payload"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetail(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            # ad_item = Ads.objects.get(pk=pk)
            ad_item = self.get_object()
            ads_list = []
            ads_list.append({
                "id": ad_item.id,
                "name": ad_item.name,
                "author": ad_item.author,
                "price": ad_item.price,
                "description": ad_item.description,
                "address": ad_item.address,
                "is_published": ad_item.is_published
            })
            return JsonResponse(ads_list, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
        except Ads.DoesNotExist:
            return JsonResponse({"error": "do not exist"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdate(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get('name', self.object.name)
        self.object.author = data.get('author', self.object.author)
        self.object.price = data.get('price', self.object.price)
        self.object.description = data.get('description', self.object.description)
        self.object.is_published = data.get('is_published', self.object.is_published)
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDelete(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['poster']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object = self.get_object()
        self.object.poster = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "poster": self.object.poster.url
        }, status=201)


# Users section
@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    # queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_list = paginator.get_page(page_number)
        user_list = []
        for item in page_list:
            user_list.append({
                "id": item.id,
                "username": item.username,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "role": item.role,
                "age": item.age,
                "total_ads": item.total_ads,
                "locations": list(map(str, item.locations.all()))
            })
        response = {
            "items": user_list,
            "page_number": paginator.num_pages,
            "total": page_list.paginator.count
        }
        return JsonResponse(response, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, *args, **kwargs):
        # try:
        data = json.loads(request.body)
        item = User()
        item.username = data["username"]
        item.first_name = data["first_name"]
        item.last_name = data["last_name"]
        item.role = data["role"]
        item.age = data["age"]
        item.save()
        for city in data["locations"]:
            city_obj, _ = City.objects.get_or_create(name=city)
            item.locations.add(city_obj)
        item.save()
        return JsonResponse({
            "id": item.id,
            "username": item.username,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "role": item.role,
            "age": item.age,
        }, status=201)
        # except Exception:
        #     return JsonResponse({"error": "incorrect payload"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            item = self.get_object()
            user_item = [{
                "id": item.id,
                "username": item.username,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "role": item.role,
                "age": item.age,
                "locations": list(map(str, item.locations.all()))
            }]
            return JsonResponse(user_item, status=200, safe=False, json_dumps_params={'ensure_ascii': False})
        except Ads.DoesNotExist:
            return JsonResponse({"error": "do not exist"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdate(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.username = data["username"]
        self.object.first_name = data["first_name"]
        self.object.last_name = data["last_name"]
        self.object.role = data["role"]
        self.object.age = data["age"]
        self.object.save()
        for city in data["locations"]:
            city_obj, _ = City.objects.get_or_create(name=city)
            self.object.locations.add(city_obj)
        self.object.save()
        return JsonResponse({
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all()))
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserDelete(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})
