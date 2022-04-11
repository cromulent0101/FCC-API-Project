from typing import List
from app import schemas
import pytest



def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts')
    def validate(post):
        return schemas.PostOut(**post)


    posts_map = map(validate,res.json())
    posts_list = list(posts_map)
    # posts = schemas.PostOut()
    # breakpoint()
    assert len(res.json())==len(test_posts)
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts): 
    res = client.get("/posts")
    assert res.status_code == 200 # Sanjeev says this should be 401 but we dont require token to get posts

def test_unauthorized_user_get_one_post(client, test_posts): 
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401 # only getting one post requires auth

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/123123123')
    assert res.status_code == 404
    # assert posts_list[0].Post.id == test_posts[0].id

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    # assert posts_list[0].Post.id == test_posts[0].id


@pytest.mark.parametrize('title,content,published',[
    ('test1','content1',True),
    ('test2','content2',False),
    ('ss@gmail.com','asdf',True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content,
                                                "published": published})           
    created_post = schemas.Post(**res.json())
    test_user = schemas.UserOut(**test_user)
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.owner_id == test_user.id

def test_create_post_default_published(authorized_client,test_user):
    res = authorized_client.post("/posts/", json={"title": "my title", "content": "my content"})
    created_post = schemas.Post(**res.json())
    assert created_post.published == True

def test_unauthorized_user_create_post(client, test_posts): 
    res = client.post("/posts/", json={"title": "my title", "content": "my content"})
    assert res.status_code == 401 # only getting one post requires auth


def test_unauthorized_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client,test_user,test_posts):
    res = authorized_client.delete("/posts/123123123")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "new content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "new content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_update_post(client,test_user,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client,test_user,test_posts):
    data = {
        "title": "updated title",
        "content": "new content",
        "id": test_posts[3].id
    }
    
    res = authorized_client.put("/posts/123123123",json=data)
    assert res.status_code == 404