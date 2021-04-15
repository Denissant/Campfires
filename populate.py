from general_crud import create, update
from resources.resources import users, pages_resource
from app import UserModel, PostsModel

# populate db with data from resources.resources

create(users, UserModel)
create(pages_resource, PostsModel)
