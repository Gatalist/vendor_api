from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from .cached import DatabaseCached
from ..mti.downloader import download_and_convert_images, download_file_in_zip


class CategoryView(DatabaseCached, TemplateView):
    def get(self, request):
        context = {
            "category_list": self.get_main_categories(),
            "is_search": True,
        }
        return render(request, 'include/category_list.html', context)


class SubCategoryView(DatabaseCached, TemplateView):
    def get(self, request, category_id):
        try:
            subcategory_list = self.get_subcategories(category_id)
        except (ValueError, TypeError):
            subcategory_list = []

        context = {
            "category_id": category_id,
            "subcategory_list": subcategory_list,
            "is_search": True,
        }
        return render(request, 'include/subcategory_list.html', context)


class ProductListView(DatabaseCached, TemplateView):
    def get(self, request, category_id, subcategory_id):
        try:
            context = self.get_products_category(subcategory_id)
        except (ValueError, TypeError):
            context = {"products_list": []}

        context["category_id"] = category_id
        context["subcategory_id"] = subcategory_id
        context["is_search"] = True
        return render(request, 'include/product_list.html', context)


class ProductDetailView(DatabaseCached, TemplateView):
    def get(self, request, category_id, subcategory_id, product_id):
        product = self.get_product_info(subcategory_id, product_id)
        context = {
            "product": product,
            "category_id": category_id,
            "subcategory_id": subcategory_id,
            "is_search": False,
        }
        return render(request, 'include/product_detail.html', context)


class ProductFilesView(DatabaseCached, APIView, TemplateView):
    pass
    def post(self, request):
        data = request.data
        option = data.get('option')
        subcategory_id = data.get('subcategoryId')
        product_id = data.get('productId')
        product = self.get_product_info(subcategory_id, product_id)
        print("data:", data)

        if option == 'getImageWebp':
            picture = product['detail_picture']
            photos = product['photos']

            imgs = []
            if picture:
                imgs.append({product_id: picture})
            if photos:
                imgs.extend(photos)
            if imgs:
                return download_and_convert_images(image_urls=imgs, name_zip=product_id)
            else:
                return Response({"error": "no images"}, status=status.HTTP_404_NOT_FOUND)

        if option == 'getImageOrigin':
            picture = product['detail_picture']
            photos = product['photos']

            imgs = []
            if picture:
                imgs.append({product_id: picture})
            if photos:
                imgs.extend(photos)
            if imgs:
                return download_file_in_zip(links=imgs, name_zip=product_id, filename="image")
            else:
                return Response({"error": "no images"}, status=status.HTTP_404_NOT_FOUND)

        if option == 'getInstruction':
            attributes = product.get('attributes')
            files = []
            count = 1
            print("attributes:", attributes)
            if attributes:
                for attribute in attributes:
                    if attribute.get('code_name') == 'file':
                        print(attribute)
                        files.append({attribute.get("id") or f"file_{count}": attribute.get("value")})
                        count += 1
            print("files:", files)
            if files:
                return download_file_in_zip(links=files, name_zip=product_id, filename="file")
            else:
                return Response({"error": "no files"}, status=status.HTTP_404_NOT_FOUND)


# http://127.0.0.1:5000/7/1815/3729196
