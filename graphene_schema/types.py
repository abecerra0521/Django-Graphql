import graphene
from graphene_django.types import DjangoObjectType
from movies.models import Category, Movie

class CategoryType(DjangoObjectType):
  class Meta:
    model = Category


class MovieType(DjangoObjectType):
  class Meta:
    model = Movie


class CreateMovie(graphene.Mutation):
  id = graphene.Int()    
  name = graphene.String()
  year = graphene.String()
  rating = graphene.Int()
  category_id = graphene.Int()

  class Arguments:
    name = graphene.String()
    year = graphene.String()
    rating = graphene.Int()
    category_id = graphene.Int()


  def mutate(self, info, id, name, year, rating, category_id):
    movie = Movie(name = name, year=year, rating=rating, category_id=category_id)
    movie.save()

    return CreateMovie(
      id=movie.id,
      name=movie.name,
      year=movie.year,
      rating=movie.rating,
      category_id=movie.category
    )


class OperationCategory(graphene.Mutation):
  id = graphene.Int()    
  name = graphene.String()

  class Arguments:
    id = graphene.ID()
    name = graphene.String()

  def mutate(self, info, **kwargs):
    id = kwargs.get('id')
    _name = kwargs.get('name')
    if id is not None:
      category = Category.objects.get(pk=id)
      category.name = _name
      category.save()
    else:
      category = Category(name=_name)
      category.save()
    
    return OperationCategory(
      id=category.id,
      name = category.name
    )



class Query(object):
  movie = graphene.Field(MovieType, id=graphene.Int(),name=graphene.String())
  all_categories = graphene.List(CategoryType)
  all_movies = graphene.List(MovieType)

  def resolve_all_categories(self, info, **kwargs):
    return Category.objects.all()

  def resolve_all_movies(self, info, **kwargs):
    return Movie.objects.select_related('category').all()


  def resolve_movie(self, info, **kwargs):
   id = kwargs.get('id')
   name = kwargs.get('name')
   if id is not None:
    return Movie.objects.select_related('category').get(pk=id)
   if name is not None:
    return Movie.objects.select_related('category').get(name=name)
   return None

  
class Mutation(graphene.ObjectType):
  create_movie = CreateMovie.Field()
  create_category = OperationCategory.Field()
  update_category = OperationCategory.Field()