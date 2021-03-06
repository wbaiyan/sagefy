{div, a, i, h2, ul, li, span, p} = require('../../modules/tags')
timeago = require('./timeago.tmpl')
{ucfirst} = require('../../modules/auxiliaries')
icon = require('./icon.tmpl')

module.exports = (kind, entityID, topics) ->
    return div(
        {className: 'entity-topics'}
        h2('Topics')
        a(
            {
                href: "/topics/create?kind=#{kind}&id=#{entityID}"
            }
            icon('create')
            ' Create a new topic'
        )
        ul(
            li(
                timeago(topic.created, {right: true})
                # TODO-2 update time ago to latest post time
                a(
                    {href: "/topics/#{topic.id}"}
                    topic.name
                )
                # TODO-3 number of posts
            ) for topic in topics
            li(
                a(
                    {href: "/search?kind=topic&q=#{entityID}"}
                    '... See more topics '
                    icon('next')
                )
            )
        ) if topics?.length
        p(
            'No topics yet.'
        ) unless topics?.length
    )
