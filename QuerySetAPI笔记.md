# QuerySet API：


# 模型.objects：
这个对象是`django.db.models.manager.Manager`的对象，这个类是一个空壳类，他上面的所有方法都是从`QuerySet`这个类上面拷贝过来的。因此我们只要学会了`QuerySet`，这个`objects`也就知道该如何使用了。
`Manager`源码解析：
```python
class_name = "BaseManagerFromQuerySet"

class_dict = {
    '_queryset_class': QuerySet
}

class_dict.update(cls._get_queryset_methods(QuerySet))

# type动态的时候创建类
# 第一个参数是用来指定创建的类的名字。创建的类名是：BaseManagerFromQuerySet
# 第二个参数是用来指定这个类的父类。
# 第三个参数是用来指定这个类的一些属性和方法
return type(class_name,(cls,),class_dict)

_get_queryset_methods：这个方法就是将QuerySet中的一些方法拷贝出来
```

## filter/exclude/annotate：过滤/排除满足条件的/给模型添加新的字段。



# order_by：
```python
# 根据创建的时间正序排序
articles = Article.objects.order_by("create_time")
# 根据创建的时间倒序排序
articles = Article.objects.order_by("-create_time")
# 根据作者的名字进行排序
articles = Article.objects.order_by("author__name")
# 首先根据创建的时间进行排序，如果时间相同，则根据作者的名字进行排序
articles = Article.objects.order_by("create_time",'author__name')
```

一定要注意的一点是，多个`order_by`，会把前面排序的规则给打乱，而使用后面的排序方式。比如以下代码：

```python
articles = Article.objects.order_by("create_time").order_by("author__name")
```

他会根据作者的名字进行排序，而不是使用文章的创建时间。
当然，也可以在模型定义的在`Meta`类中定义`ordering`来指定默认的排序方式。示例代码如下：
```python
    class Meta:
        db_table = 'book_order'
        ordering = ['create_time','-price']
```

还可以根据`annotate`定义的字段进行排序。比如要实现图书的销量进行排序，那么示例代码如下：
```python
books = Book.objects.annotate(order_nums=Count("bookorder")).order_by("-order_nums")
    for book in books:
        print('%s/%s'%(book.name,book.order_nums))
```



# values ：
用来指定在提取数据出来，需要提取哪些字段。默认情况下会把表中所有的字段全
部都提取出来，可以使用 'values' 来进行指定，并且使用了 'values' 方法后，提取出
的 QuerySet 中的数据类型不是模型，而是在 'values' 方法中指定的字段和值形成的字典：

 ```python
 articles = Article.objects.values("title",'content')
    for article in articles:
    print(article)
 ```
 
以上打印出来的 'article' 是类似于 `{"title":"abc","content":"xxx"}` 的形式。
如果在 'values' 中没有传递任何参数，那么将会返回这个恶模型中所有的属性。

## 如果我们想要提取的是这个模型上关联的属性，那么也是可以的，查找顺序跟'filter'的用法是一样的，示例代码如下：
```python
books = Book.objects.valuse('id', 'name', author_name=("author__name"))
```
## 以上将会提取作者的名字字段，如果想要更改一个名字，可以使用关键字参数，示例代码如下：
```python
books = Book.objects.valuse('id', 'name', author_name=F("author__name"))
```
自定义的名字不能和已经存在的名字一样，比如`author_name`不能重复。
##  在`values`中可以使用聚合函数来形成一个新的字段，比如想要获取每本书的销量，示例代码如下：
```python
books = Book.objects.values('id', 'name', order_nums=Count("bookorder"))
```



# values_list
## 跟`values`是一样的作用，只不过这个方法返回的`QuerySet`中装的不是字典，而是元组，示例如下：
```python
books = Book.objects.values_list('id', 'name')
```
那么以上返回的结果是`(1,'三国演义')`，
## 如果给`values_list`只指定一个字段，那么可以指定`flat=True`,这样返回的结果就不是一个元组，而是这个字段的值，示例代码入下：
```python
books = Book.objects.values_list('name', flat=True)
```
## 注意`flat`只能用在只有一个字段的情况下，否则会报错



# all方法
## 返回一个`QuerySet`对象，没有做任何更改，会返回所有属性，很少用到。



# select_related方法
## 在提取某个模型的数据的同时，也提前将相关联的其他表的数据取出来，在以后访问相关联的的表的数据的时候，不用再次查找，节省开销。
比如提取文章数据的同时，可以取作者信息表的数据，示例代码如下：
```python
books = Book.objects.select_related("author","publisher")
for book in books:
    print(book.author.name)
    print(book.publisher.name)
    # 因为在提取Book的时候，使用了select_related，那么以后在访问book.author 的时候，不会再次发起请求。
```
## 注意：这个方法只能用在外键的关联对象上，对于那种多对多、多对一的情况，不能使用此方法，而应该使用`prefetch_related`来实现。



# prefetch_related方法
## 和`select_related`方法类似，用在处理那种多对多、多对一的情况。
这个方法会产生两个查询语句，所以，如果在这个方法中查询使用外键关联的模型的时候，也会产生两个查询语句，因此，如果查询的是外键关联的模型，建议使用`select_related`方法。
在查询多对多关系或者一对多的关联的对象的时候，你在使用模型怎么访问这个多对多，那么久在这个方法中传递什么字符串，比如要获取图书的所有订单，示例代码如下:
```python
 books = Book.objects.prefetch_related("bookorder_set")
```
## 注意：如果在使用`prefetch_related`查找出的`bookorder_set`，建议不要对他进行任何操作，比如`filter`,不然又会产生更多的查询语句，是不对的：
```python
books = Book.objects.prefetch_related("bookorder_set")
    for book in books:
        print('='*30)
        print(book.name)
        orders = book.bookorder_set.filter(price__gte=90)
        for order in orders:
            print(order.id)

```
## 如果确实想要对预先查找的集合进行操作，那么我们可以使用`models.Prefetch`来完成：
```python
# 先使用prefetch将查询的条件写好，再来使用。
prefetch = Prefetch("bookorder_set",queryset=BookOrder.objects.filter(price__gte=90))
    books = Book.objects.prefetch_related(prefetch)
    for book in books:
        print('='*30)
        print(book.name)
        orders = book.bookorder_set.all()
        for order in orders:
            print(order.id)
```



# defer 方法
## 在一些表中，可能存在很多字段，但是一些字段的数据量可能是比较大的，而你此时又不需要，这个时候可以使用`defer`来过滤掉一些字段（可以是多个），这个字段跟`values`有点类似，只不过`defer`返回的不是字典，而是模型。
```python
 books = Book.objects.defer("name")
```
## 注意： 使用`defer`的字段，以后再次使用的话，会再次发起请求，请谨慎操作。


# only
## 跟`defer`类似，不过`only`是只提取某些字段（可以是多个）。
```python
   books = Book.objects.only('name')
   # 默认是提取 'id'的
```
## 注意： 没有使用`only`的字段，以后想要使用的话，会再次发起请求，请谨慎操作。



# get 方法 
## 获取满足条件的数据，这个函数只能返回一条数据，并且如果给的条件有多条数据，那么这个方法会抛出错误，如果给的条件没有任何数据，也会抛出错误，送一这个方法在获取数据的时候，只能有一条数据。
```pyhton
book = Book.objects.get(id=5)
```



# create 方法
## 创建一条数据，并且保存到数据库中，这个方法相当于先用指定的模型创建一个对象，然后再调用这个对象的`save`方法，示例如下：
```python
# publisher = Publisher(name='知了出版社')
    # publisher.save()
    publisher = Publisher.objects.create(name='知了课堂出版社')
```



# get_or_create 方法
## 根据某个条件进行查找，如果找到就返回这条数据，如果没有找到，那么就创建一个，示例代码如下：
```python
# result = Publisher.objects.get_or_create(name='知了abc出版社')
# print(result[0])
```


# bulk_create 方法
## 一次性创建多个数据，示例代码如下：
```
publisher = Publisher.objects.bulk_create([
    Publisher(name='123出版社'),
    Publisher(name='abc出版社'),
])
```
优势在于执行一次，将所有的数据都插入到数据库，效率高。


# count 方法
## 获取提取的数据的个数，如果想要知道总共有多少条数据，那么建议使用`count`，而不是`len(articles)`这种，因为`count`在底层使用`select count(*)`来实现，更加高效。
```python
count = Book.objects.count()
```


# first 和last 方法
## 返回`QuerySet`中的第一条和最后一条数据。


# aggregate 方法
## 使用聚合函数。


# exists 方法
## 判断某个条件的数据是否存在，如果要判断某个条件的元素是否存在，那么建议使用`exists`,这比直接使用`count`或者直接判读`QuerySet`更有效，实例代码如下：
```python
result = Book.objects.filter(name='三国演义').exists()
```


# distinct 方法
## 去掉那重复的数据，这个方法如果底层数据库用的是MySQL，那么不能传递任何值，比如想要提取所有销售的价格超过80元的图书，并且删掉那些重复的，那么可以使用`distinct`来实现，示例代码如下：
```python
order = BookOrder.objects.filter(bookorder__price__gte=80).distinct()
```
## 需要注意的是，如果`distinct`之前使用了`order_by`，那么因为`order_by`会提取`order_by`中指定的字段，因此再使用`distinct`就会根据多个字段来进行唯一化，所以就不会把那些重复的数据删掉。示例代码如下：
```python
order = BookOrder.objects.order_by('create_time').values('book_id').distinct()
```
那么以上代码因为使用了`order_by`，即使使用了`distinct`，也会把重复的`book_id`提取出来。



# update 方法
## 执行更新操作，在SQL底层走的也是`update`命令，比如将所有图书价格都怎加5，示例代码如下：
```python
Book.objects.update(price=F("price")+5)
```



# delete 方法
## 一次性可以把所有满足条件的数据都删除掉。
```python
Author.objects.filter(id__gte=3).delete()
```
## 注意：删除的时候注意数据表之间的关系（模板中`on_delete`指定的方式）。



# 切片操作
## 有时候我们查找数据，有可能只需要其中的一部分，那么这时候可以使用切片操作来帮助我们完成，`QuerySet`使用切片操作就跟列表使用切片操作是一样的，示例代码如下：
```python
books = Book.objects.all()[1:2]
```
切片操作并不是把所有数据从数据库中提取出来再进行切片操作，而是在数据库底层使用`limie`和`offset`来帮我们完成，所以如果只需要提取其中的一部分，建议使用切片操作。



# 什么时候`Django`会将`QuertSet`转化为SQL去执行：
    生成一个`QuerySet`不会马上转化为SQL去执行。

1. 迭代：在遍历`QuerySet`对象的时候，会首先执行这个SQL语句，然后再把这个结果返回进行迭代，比如以下代码：
```python
for book in Book.objects.all():
    print(book)
```
2. 使用步长进行切片操作：`QuerySet`可以类似于列表一样做切片操作，做切片操作本身不会执行SQL语句，但如果在做切片操作的时候提供了步长，那么就会立马执行SQL语句，需要注意的是，做切片后不能再执行`filter`方法，否则会报错。
3. 调用`len`函数：调用`len`函数来获取`QuerySet`中总共有多少条数据也会执行SQL语句
4. 调用`list`函数：调用`list`函数用来将一个`QuerySet`对象转化为`list`对象也会执行SQL语句
5. 判断：如果对某个`QuerySet`进行判断，也会执行SQL语句
