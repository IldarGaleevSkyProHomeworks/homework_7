import hashlib
import os.path
from django.core.files import File
from django.core.files.utils import validate_file_name
from django.core.files.storage import FileSystemStorage


class HashStorage(FileSystemStorage):

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        if not hasattr(content, "chunks"):
            content = File(content, name)

        if not self.exists(name):
            name = self._save(name, content)

        validate_file_name(name, allow_relative_path=True)
        return name


def _get_file_hash_path(root, ctx, instance, filename):
    ctx.open()
    context = ctx.read()
    _, ext = os.path.splitext(filename)

    file_path = os.path.join(root, hashlib.md5(context).hexdigest() + ext)

    return file_path


def user_avatar_images(instance, filename):
    return _get_file_hash_path('user_avatar_images', instance.avatar, instance, filename)


def course_preview_images(instance, filename):
    return _get_file_hash_path('course_preview_images', instance.preview, instance, filename)
