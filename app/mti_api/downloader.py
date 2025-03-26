import os
import requests
from PIL import Image
from io import BytesIO
import zipfile
import time
from flask import jsonify, send_file


def download_and_convert_images(image_urls, name_zip):
    output_zip = f"{name_zip}.zip"
    # Буфер в памяти для ZIP-архива
    zip_buffer = BytesIO()
    counter = 1
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # for index, url in enumerate(image_urls):
        for item in image_urls:
            img_id, url = next(iter(item.items()))
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                # Открываем изображение и конвертируем
                img = Image.open(BytesIO(response.content))
                img_io = BytesIO()
                img.save(img_io, format="WEBP", quality=90)
                img_io.seek(0)

                # Добавляем в ZIP-архив
                zipf.writestr(f"image_{counter}_{img_id}.webp", img_io.getvalue())
                counter += 1
            except requests.RequestException as e:
                return jsonify({"error": f"Failed to download image: {url}, {str(e)}"}), 400
            except Exception as e:
                return jsonify({"error": f"Failed to process image: {url}, {str(e)}"}), 400

    # Подготавливаем ZIP-архив для передачи
    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name=output_zip)