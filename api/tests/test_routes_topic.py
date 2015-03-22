import pytest

xfail = pytest.mark.xfail


from conftest import create_user_in_db
import json
import rethinkdb as r


def create_topic_in_db(topics_table, db_conn, user_id='abcd1234'):
    topics_table.insert({
        'id': 'wxyz7890',
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'name': 'A Modest Proposal',
        'entity': {
            'id': 'efgh5678',
            'kind': 'unit'
        }
    }).run(db_conn)


def create_post_in_db(posts_table, db_conn, user_id='abcd1234'):
    posts_table.insert({
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': user_id,
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }).run(db_conn)


def create_proposal_in_db(posts_table, db_conn):
    posts_table.insert({
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'proposal',
        'entity_version_id': '1',
        'name': 'New Unit',
        'status': 'pending',
        'action': 'create'
    }).run(db_conn)


def test_create_topic(app, db_conn, c_user, topics_table, posts_table):
    """
    Expect to create a topic with post.
    """
    response = c_user.post('/api/topics/', data=json.dumps({
        'topic': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            },
        },
        'post': {
            'body': 'Here\'s a pear.',
            'kind': 'post'
        }
    }), content_type='application/json')

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_proposal(app, db_conn, users_table, topics_table,
                               posts_table, c_user):
    """
    Expect to create a topic with proposal.
    """
    response = c_user.post('/api/topics/', data=json.dumps({
        'topic': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            },
        },
        'post': {
            'kind': 'proposal',
            'body': 'Here\'s a pear.'
        }
    }), content_type='application/json')

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


@xfail
def test_create_topic_flag(app, db_conn, users_table, topics_table,
                           posts_table, c_user):
    """
    Expect to create topic with a flag.
    """
    response = c_user.post('/api/topics/', data=json.dumps({
        'topic': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            },
        },
        'post': {
            'kind': 'flag',
            'reason': 'duplicate',
        }
    }), content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'post' in data
    assert 'topic' in data
    assert data['topic']['name'] == 'An entity'
    assert data['post']['body'] == 'Here\'s a pear.'


def test_create_topic_log_in(app, db_conn, users_table, topics_table,
                             posts_table):
    """
    Expect create topic to fail when logged out.
    """
    with app.test_client() as c:
        response = c.post('/api/topics/', data=json.dumps({
            'topic': {
                'name': 'An entity',
                'entity': {
                    'kind': 'unit',
                    'id': 'dfgh4567'
                },
            },
            'post': {
                'body': 'Here\'s a pear.'
            }
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode())
        assert 'errors' in data


def test_create_topic_no_post(app, db_conn, users_table, topics_table,
                              posts_table, c_user):
    """
    Expect create topic to fail without post.
    """
    response = c_user.post('/api/topics/', data=json.dumps({
        'topic': {
            'name': 'An entity',
            'entity': {
                'kind': 'unit',
                'id': 'dfgh4567'
            }
        }
    }), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert 'errors' in data


def test_topic_update(app, db_conn, users_table, topics_table,
                      posts_table, c_user):
    """
    Expect to update topic name.
    """
    create_topic_in_db(topics_table, db_conn)
    response = c_user.put('/api/topics/wxyz7890/', data=json.dumps({
        'name': 'Another entity',
        'topic_id': 'wxyz7890',
    }), content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data['topic']['name'] == 'Another entity'


def test_update_topic_author(app, db_conn, users_table, topics_table,
                             posts_table, c_user):
    """
    Expect update topic to require original author.
    """
    create_topic_in_db(topics_table, db_conn, user_id="qwerty")
    response = c_user.put('/api/topics/wxyz7890/', data=json.dumps({
        'name': 'Another entity',
        'topic_id': 'wxyz7890',
    }), content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 403
    assert 'errors' in data


def test_update_topic_fields(app, db_conn, users_table, topics_table,
                             posts_table, c_user):
    """
    Expect update topic to only change name.
    """
    create_topic_in_db(topics_table, db_conn)
    response = c_user.put('/api/topics/wxyz7890/', data=json.dumps({
        'topic_id': 'wxyz7890',
        'entity': {
            'kind': 'set'
        }
    }), content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert 'errors' in data


def test_get_posts(app, db_conn, users_table, topics_table, posts_table):
    """
    Expect to get posts for given topic.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    posts_table.insert([{
        'id': 'jklm',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
    }, {
        'id': 'tyui',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'body': 'A follow up.',
        'kind': 'post',
    }]).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts/')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert ('Beneficial to the Publick' in data['posts'][0]['body']
                or 'Beneficial to the Publick' in data['posts'][1]['body'])


def test_get_posts_not_topic(app, db_conn, users_table, topics_table,
                             posts_table):
    """
    Expect 404 to get posts for a nonexistant topic.
    """
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts/')
        assert response.status_code == 404


def test_get_posts_paginate(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect get posts for topic to paginate.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    for i in range(0, 25):
        posts_table.insert({
            'id': 'jklm%s' % i,
            'created': r.now(),
            'modified': r.now(),
            'user_id': 'abcd1234',
            'topic_id': 'wxyz7890',
            'body': 'test %s' % i,
            'kind': 'post',
        }).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts/')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert len(data['posts']) == 10
        response = c.get('/api/topics/wxyz7890/posts/?skip=20')
        data = json.loads(response.data.decode())
        assert len(data['posts']) == 5


def test_get_posts_proposal(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect get posts for topic to render a proposal correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts/')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data['posts'][0]['kind'] == 'proposal'


def test_get_posts_votes(app, db_conn, users_table, topics_table, posts_table):
    """
    Expect get posts for topic to render votes correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    posts_table.insert({
        'id': 'asdf4567',
        'created': r.now(),
        'modified': r.now(),
        'kind': 'vote',
        'body': 'Hooray!',
        'proposal_id': 'jklm',
        'topic_id': 'wxyz7890',
        'response': True,
    }).run(db_conn)
    with app.test_client() as c:
        response = c.get('/api/topics/wxyz7890/posts/')
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        assert data['posts'][0]['kind'] in ('proposal', 'vote')
        assert data['posts'][1]['kind'] in ('proposal', 'vote')


def test_create_post(app, db_conn, users_table, topics_table, posts_table,
                     c_user):
    """
    Expect create post.
    """
    create_topic_in_db(topics_table, db_conn)
    response = c_user.post('/api/topics/wxyz7890/posts/', data=json.dumps({
        # Should default to > 'kind': 'post',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'kind': 'post',
        'topic_id': 'wxyz7890',
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert 'Beneficial to the Publick' in data['post']['body']


def test_create_post_errors(app, db_conn, users_table, topics_table,
                            posts_table, c_user):
    """
    Expect create post missing field to show errors.
    """
    create_topic_in_db(topics_table, db_conn)
    response = c_user.post('/api/topics/wxyz7890/posts/',
                           data=json.dumps({
                               'kind': 'post',
                               'topic_id': 'wxyz7890',
                           }),
                           content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    assert 'errors' in data


def test_create_post_log_in(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect create post to require log in.
    """
    create_topic_in_db(topics_table, db_conn)
    with app.test_client() as c:
        response = c.post('/api/topics/wxyz7890/posts/', data=json.dumps({
            # Should default to > 'kind': 'post',
            'body': '''A Modest Proposal for Preventing the Children of Poor
                People From Being a Burthen to Their Parents or Country, and
                for Making Them Beneficial to the Publick.''',
            'topic_id': 'wxyz7890',
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode())
        assert 'errors' in data


@xfail
def test_create_post_proposal(app, db_conn, users_table, topics_table,
                              posts_table, c_user):
    """
    Expect create post to create a proposal.
    """
    create_topic_in_db(topics_table, db_conn)
    response = c_user.post('/api/topics/wxyz7890/posts/', data=json.dumps({
        'kind': 'proposal',
        'name': 'New Unit',
        'body': '''A Modest Proposal for Preventing the Children of Poor
            People From Being a Burthen to Their Parents or Country, and
            for Making Them Beneficial to the Publick.''',
        'action': 'create',
        'unit': {
            'name': 'Satire',
            'body': '''Learn the use of humor, irony, exaggeration, or
            ridicule to expose and criticize people's
            stupidity or vices.''',
            'tags': ['literature']
        },
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['post']['kind'] == 'proposal'


@xfail
def test_create_post_vote(app, db_conn, users_table, topics_table,
                          posts_table, c_user):
    """
    Expect create post to create a vote.
    """
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    response = c_user.post('/api/topics/wxyz7890/posts/', data=json.dumps({
        'kind': 'vote',
        'body': 'Hooray!',
        'proposal_id': 'jklm',
        'response': True,
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data['post']['kind'] == 'vote'


def test_update_post_log_in(app, db_conn, users_table, topics_table,
                            posts_table):
    """
    Expect update post to require log in.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn)
    with app.test_client() as c:
        response = c.put('/api/topics/wxyz7890/posts/jklm/', data=json.dumps({
            'body': '''Update.''',
        }), content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data.decode())
        assert 'errors' in data


def test_update_post_author(app, db_conn, users_table, topics_table,
                            posts_table, c_user):
    """
    Expect update post to require own post.
    """
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn, user_id='1234yuio')
    response = c_user.put('/api/topics/wxyz7890/posts/jklm/', data=json.dumps({
        'body': '''Update.''',
    }), content_type='application/json')
    assert response.status_code == 403
    data = json.loads(response.data.decode())
    assert 'errors' in data


def test_update_post_body(app, db_conn, users_table, topics_table,
                          posts_table, c_user):
    """
    Expect update post to change body for general post.
    """
    create_topic_in_db(topics_table, db_conn)
    create_post_in_db(posts_table, db_conn)
    response = c_user.put('/api/topics/wxyz7890/posts/jklm/', data=json.dumps({
        'body': '''Update.''',
    }), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert 'Update' in data['post']['body']


def test_update_proposal(app, db_conn, users_table, topics_table,
                         posts_table, c_user):
    """
    Expect update post to handle proposals correctly.
    """
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    response = c_user.put('/api/topics/wxyz7890/posts/jklm/', data=json.dumps({
        'status': 'declined'
    }), content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert 'declined' in data['post']['status']


def test_update_vote(app, db_conn, users_table, topics_table,
                     posts_table, c_user):
    """
    Expect update vote to handle proposals correctly.
    """
    create_user_in_db(users_table, db_conn)
    create_topic_in_db(topics_table, db_conn)
    create_proposal_in_db(posts_table, db_conn)
    posts_table.insert({
        'id': 'vbnm1234',
        'created': r.now(),
        'modified': r.now(),
        'user_id': 'abcd1234',
        'topic_id': 'wxyz7890',
        'proposal_id': 'jklm',
        'body': 'Boo!',
        'response': False,
        'kind': 'vote',
        'replies_to_id': 'val2345t',
    }).run(db_conn)
    response = c_user.put(
        '/api/topics/wxyz7890/posts/vbnm1234/',
        data=json.dumps({
            'body': 'Yay!',
            'response': True,
        }),
        content_type='application/json')
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert True == data['post']['response']
