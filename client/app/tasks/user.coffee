store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
cookie = require('../modules/cookie')

# TODO move setting and unsetting of currentUserID back to the server

module.exports = store.add({
    createUser: (data) ->
        @data.sending = true
        @change()
        ajax({
            method: 'POST'
            url: '/s/users'
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create user')
                window.location = '/my_sets'
                # Hard redirect to get the HTTP_ONLY cookie
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create user', errors)
            always: =>
                @data.sending = false
                @change()
        })

    updateUser: (data) ->
        @data.sending = true
        @change()
        ajax({
            method: 'PUT'
            url: "/s/users/#{data.id}"
            data: data
            done: (response) =>
                @data.users ?= {}
                @data.users[response.user.id] = response.user
                recorder.emit('update user', response.user.id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on update user', errors)
            always: =>
                @data.sending = false
                @change()
        })

    getCurrentUser: ->
        ajax({
            method: 'GET'
            url: '/s/users/current'
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                @data.users ?= {}
                @data.users[response.user.id] = response.user
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('fail get current user', errors)
            always: =>
                @change()
        })

    getUser: (id, opts = {}) ->
        ajax({
            method: 'GET'
            url: "/s/users/#{id}"
            data: opts
            done: (response) =>
                @data.users ?= {}
                user = response.user
                ['avatar', 'posts', 'sets', 'follows'].forEach((t) ->
                    user[t] = response[t] if response[t]
                )
                @data.users[response.user.id] = user
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('fail get user', id, errors)
            always: =>
                @change()
        })

    logInUser: (data) ->
        @data.sending = true
        @change()
        ajax({
            method: 'POST'
            url: '/s/sessions'
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('log in user')
                # Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on log in user', errors)
            always: =>
                @data.sending = false
                @change()
        })

    logOutUser: ->
        @data.sending = true
        @change()
        ajax({
            method: 'DELETE'
            url: '/s/sessions'
            done: =>
                @data.currentUserID = null
                cookie.unset('currentUserID')
                window.location = '/'
                # Hard redirect to delete the HTTP_ONLY cookie
                recorder.emit('log out user')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on log out user', errors)
            always: =>
                @data.sending = false
                @change()
        })

    getUserPasswordToken: (data) ->
        @data.sending = true
        @change()
        ajax({
            method: 'POST'
            url: '/s/password_tokens'
            data: data
            done: (response) =>
                @data.passwordPageState = 'inbox'
                recorder.emit('obtain password token')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on password token', errors)
            always: =>
                @data.sending = false
                @change()
        })

    createUserPassword: (data) ->
        @data.sending = true
        @change()
        ajax({
            method: 'POST'
            url: "/s/users/#{data.id}/password"
            data: data
            done: (response) =>
                @data.currentUserID = response.user.id
                cookie.set('currentUserID', response.user.id)
                recorder.emit('create password')
                # Hard redirect to get the HTTP_ONLY cookie
                window.location = '/my_sets'
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on create password', errors)
            always: =>
                @data.sending = false
                @change()
        })
})
