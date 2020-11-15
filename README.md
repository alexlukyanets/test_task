Link of task https://www.notion.so/Python-test-assessment-by-DevelopsToday-901e35b8314d4ddc962bebf5041871d6

# Tasks setp 1
- [x] Create Post CRUD API 
- [x] Create Comment CRUD API 
- [x] endpoint to upvote the post


# Создание моделей, стерилизаторов и контроллера
Создано три модели: New – для новостей, Comment – для комментариев к новостям и Vote – для голосования к новостям. 

## Модель New, содержит поля, приведенные ниже. Комментарий от разработчика – сущность новости должна была быть названа Post, не переименована по причине отсутствие важности в названии)
title (тип - CharField)
link (URLField, unique=True – новость должна содержать уникальную ссылку)
created_at (DateTimeField(auto_now_add=True)
author ForeignKey ссылается на существую модельUser из Django – новость может создать авторизированный пользователь)

## Модель Comment, содержит поля приведенные ниже
Author - ForeignKey ссылается на существую модельUser из Django – комментарий может создать только авторизированный пользователь
Content (тип TextField) 
created_at (DateTimeField(auto_now_add=True)
new - ForeignKey ссылается на новость New, реализует связь один ко многим, новость может содержать множество коментриев, но один отдельный комментарий должен быть привязан только к одной новости.  

## Модель Vote
voter – ForeignKey ссылается на существую модельUser из Django – голосовать за новость может только авторизированный пользователь
new – ForeignKey ссылается на новость New. Реализация связи один ко многим. Один голос пользователя может принадлежать только одной новости, но за новость можно голосовать большому количеству пользователей. 

# Создание стерилизаторов
Создано 3 класса стериализаторов: NewSerializer, CommentSerializer, VoteSerializer

## NewSerializer – для сериализации модели новостей из модели New, сериализует все поля. 
Дополнительная настройка полей: 
author – ReadOnlyField (поле только для чтения), при создании, имя автора извлекается из запроса пользователя из обтьекта requests – user. Username
author_id – ReadOnlyField, при создании также извлекается из запроса пользователя. 
votes – SerializerMethodField, к полю привязан метод get_votes, который возвращает из модели Vote все голоса за новость и выводит их количество функцией count. 
comments - SerializerMethodField, к полю привязан метод get_comments, который возвращает из модели Comment все комментарий к новости и сериализует такие поля как ('id', 'content', 'author__username', 'created_at'). При отсутствии комментариев возвращает null. 

## CommentSerializer – для сериализации модели коментариев Comment, сериализует все поля. 
Дополнительные поля. 
author – ReadOnlyField (поле только для чтения), при создании, имя автора извлекается из запроса пользователя из обтьекта requests – user. Username
author_id – ReadOnlyField, при создании также извлекается из запроса пользователя. 
new – ReadOnlyField, при создании извлекается из адресного запроса пользователя. 

## VoteSerializer – класс для сериализации голосов из модели Vote, сериализует поле id. 

# Создание Контролеров
Создано 5 контролеров: NewListCreate,  NewRetrieveUpdateDestroy,  CommentListCreate,  CommentRetrieveUpdateDestroy,  VoteCreateDestroy,

## NewListCreate 
Наследован от generic класса ListCreateAPIView. Реализует функционал получение всех новостей и создание новости (метод perform_create). Принимает методы GET и POST. Обращаться нужно по URL 'api/news/'. 

## NewRetrieveUpdateDestroy
Наследовано от generic класса NewRetrieveUpdateDestroy. Реализует функционал получение, обновление (метод put), удаление (метод delete) - одной новости. Метод put_delete осуществляет схожую проверку для вышеперечисленных методов и возвращает исключение при не корректном id новости или попытке изменить новость, не созданную пользователем. Методы GET, PUT, DELETE. Обращаться нужно по URL 'api/new/ <int:pk>'.

## CommentListCreate
Класс наследован от genericкласса ListCreateAPIView. Позволяет создавать (метод perform_create) и просматривать (get_queryset, get) все комментарии к новости. Возвращает исключение при попытке комментировать не существующую новость. Принимает методы GET и POST. Обращаться нужно по URL ‘ api/new/<int:pk>/comments/ ‘.

## CommentRetrieveUpdateDestroy 
Наследован от generic клас'а. Позволяет получать отдельный комментарий по id изменять, удалять. Возвращает исключение при остсутствие комментария и попытке изменить комментарий не созданный авторизированым пользователем.  Методы GET, PUT, DELETE. Обращаться нужно по URL ‘api/comment/<int:pk>’.

## VoteCreateDestroy
Наследован от generic класса и миксина DestroyModelMixin. Позволяет удалять и создавать (голосовать) за отдельную новость. Возвращает исключение при попытке голосования за несуществующую новость,  попытке повторного голосования и при попытке удаление голоса от пользователя который за неё не голосовал. Методы POST, DELETE. Обращаться нужно по URL 'api/new/<int:pk>/vote/'.

- [x] Recurring job running once a day to reset post upvotes count
- [x] Documented with Postman
- [x] Add Postman collection link to the README

- [ ] Docker container. API + Postgres 
- [ ] Deploy API for testing to Heroku



Documented with Postman
https://documenter.getpostman.com/view/9950425/TVep8TBa#886473de-7c41-423e-91e4-2da94e6a8127



Heroku app
https://secure-reef-11170.herokuapp.com/
http://git.heroku.com/secure-reef-11170.git

