from typing import List
from app import schemas



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