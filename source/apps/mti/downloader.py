import requests
from PIL import Image
from io import BytesIO
import zipfile
from django.http import JsonResponse, HttpResponse


def download_and_convert_images(image_urls, name_zip):
    output_zip = f"{name_zip}.zip"
    zip_buffer = BytesIO()
    counter = 1

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in image_urls:
            img_id, url = next(iter(item.items()))
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                img = Image.open(BytesIO(response.content))
                img_io = BytesIO()
                img.save(img_io, format="WEBP", quality=90)
                img_io.seek(0)

                zipf.writestr(f"image_{counter}_{img_id}.webp", img_io.getvalue())
                counter += 1
            except requests.RequestException as e:
                return JsonResponse({"error": f"Failed to download image: {url}, {str(e)}"}, status=400)
            except Exception as e:
                return JsonResponse({"error": f"Failed to process image: {url}, {str(e)}"}, status=400)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{output_zip}"'
    return response


def download_file_in_zip(links: list[dict], name_zip: str, filename: str):
    output_zip = f"{name_zip}.zip"
    zip_buffer = BytesIO()
    counter = 1

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item in links:
            img_id, url = next(iter(item.items()))
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                # add in ZIP
                zipf.writestr(f"{filename}_{counter}_{img_id}{get_file_extension(url)}", response.content)
                counter += 1
            except requests.RequestException as e:
                return JsonResponse({"error": f"Failed to download image: {url}, {str(e)}"}, status=400)
            except Exception as e:
                return JsonResponse({"error": f"Failed to process image: {url}, {str(e)}"}, status=400)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{output_zip}"'
    return response


def get_file_extension(url: str):
    """Extracts the file extension from a URL"""
    parts = url.split('.')
    if len(parts) > 1:
        return f".{parts[-1].split('?')[0]}"  # Handle query parameters
    return ""
