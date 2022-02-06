from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    print(list(posts_map))
    assert res.status_code == 200


def test_unauthorized_user_get_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401

def test_get_one_ost_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    print(post)
    assert post.Post.id == test_post[0].id
    assert post.Post.content == test_post[0].content

@pytest.mark.parametrize("title, content, published", [
    ("Title1", "content1", True),
    ("Title2", "content2", False),
    ("Title3", "content3", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json = {"title": title, "content":content, "published":published})
    created_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(authorized_client):
    res = authorized_client.post("/posts/", json = {"title": "title1", "content": "ABCD"})
    created_post = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title1"
    assert created_post.content == "ABCD"
    assert created_post.published == True

def test_unauthorized_user_create_post(client, test_post):
    res = client.post("/posts/", json = {"title": "title1", "content": "ABCD"})
    assert res.status_code == 401


def test_unautherized_user_delete_post(client, test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/500000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_post):
    data = {
        "title":"updated title",
        "content": "updated content",
        "id" : test_post[0].id
    }
    res = authorized_client.put(f"/posts/{test_post[0].id}", json = data)
    update_post = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user,test_user2, test_post):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[3].id
    }
    res = authorized_client.put(f"/posts/{test_post[3].id}", json=data)
    assert res.status_code == 403


def test_unautherized_user_udate_post(client, test_user, test_post):
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_post):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[3].id
    }
    res = authorized_client.put(f"/posts/500000", json = data)
    assert res.status_code == 404
