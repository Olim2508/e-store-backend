from main.models import ProductCategory
from main.utils import except_shell


class ProductService:

    @staticmethod
    @except_shell((ProductCategory.DoesNotExist,))
    def get_category(id: int):
        return ProductCategory.objects.get(id=id)
