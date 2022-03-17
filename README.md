### Собственное «Авито». Django, GenericView
- Создал модели на основе фейковых данных 
- Корневой роут использует подход FBV
- Все остальные view используют подход CBV и GenericView
- Реализовал для категорий и объявлений CRUD.

# Добавлено: 
## Postgres, Модели с relations и QuerySet.

- Подключил к проекту PostgreSQL
- Переписаны View на наследников ListView, DetailView и CreateView
- Реализованы недостающие для категорий и объявлений методы PATCH/DELETE
- Добавлены отношения ForeignKey и ManyToManyField
- Добавлен URL /ad/<int:pk>/upload_image/ для загрузки картинок к объявлениям 
- Добавлена пагинацию
- CRUD для пользователей
- Переписано на get_or_create, get_object_or_404
- Определен class Meta для названий и сортировок по умолчанию (ordering и __str__)
- Тест метода aggregate / annotate

## Todo 
- Переписать на select_relation/prefetch_related