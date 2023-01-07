
from django.urls    import path

from .views         import( home, 
                            IncomeList,
                            IncomeCreate, 
                            IncomeUpdate, 
                            IncomeDelete, 
                            incomeDetail,
                            CategoryCreateView,
                            SearchIncomeView )


app_name = 'income'

urlpatterns = [
    path('', home, name='home'),
    path('list/', IncomeList.as_view(), name = 'incomelist'),
    path('list/search', SearchIncomeView.as_view(), name = 'search'),
    path('list/search/page/<int:page>', SearchIncomeView.as_view(), name = 'search'),
    path('create/cat', CategoryCreateView.as_view(), name = 'create_cat'),
    path('create/', IncomeCreate.as_view(), name = 'create'),
    path('update/<int:pk>/', IncomeUpdate.as_view(), name = 'update'),
    path('delete/<int:pk>/', IncomeDelete.as_view(), name = 'delete'),
    path('detail/<id>/', incomeDetail.as_view(), name = 'detail'),

]






