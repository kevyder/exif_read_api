import re
import os
import exifread
import tempfile

ALLOWED_EXTENSIONS = ("tiff", "jpeg", "jpg", "png", "webp", "heic")


def allowed_file_extension(file_extension: str) -> bool:
    return file_extension.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def camel_case_2_snake_case(camel_case_string: str) -> str:
    camel_case_string = camel_case_string.replace("EXIF", "")
    camel_case_string = camel_case_string.replace(" ", "")
    snake_case_string = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case_string).lower()
    return snake_case_string


def get_image_exit_data(image_path) -> dict:
    exif_data = {}
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f, details=False)
        for tag in tags.keys():
            value = str(tags.get(tag, None))
            tag_camel_case = camel_case_2_snake_case(tag)
            exif_data[tag_camel_case] = value
    return exif_data


def process_image(image) -> dict:
    image_data = image.read()
    tmp_img = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp_img_path = tmp_img.name
        tmp_img.write(image_data)
        exif_data = get_image_exit_data(tmp_img_path)
    finally:
        tmp_img.close()
        os.unlink(tmp_img_path)

    return exif_data
