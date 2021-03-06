{div, h1, p, a, i, ul, li, strong} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')
spinner = require('../components/spinner.tmpl')
icon = require('../components/icon.tmpl')

module.exports = (data) ->
    return spinner() unless data.follows

    return div(
        {id: 'follows'}
        h1('Follows')
        a(
            {href: '/notices'}
            icon('back')
            ' Back to notices.'
        )
        follows(data.follows)
    )

follows = (data) ->
    if not data.length
        return p(
            'No follows. '
            a(
                {href: '/search'}
                icon('search')
                ' Search'
            )
        )
    return ul(follow(f) for f in data)

follow = (data) ->
    return li(
        {className: 'follow'}
        a(
            {
                id: data.id
                href: '#'
                className: 'follows__unfollow-button'
            }
            icon('remove')
            ' Unfollow'
        )
        div(
            strong(ucfirst(data.entity.kind))
            ': '
            data.entity.name
        )
    )
