require('./matches_polyfill')

eventRegExp = /^(\S+) (.*)$/

module.exports = {
    events: {
        click: {}
        change: {}
        keyup: {}
        submit: {}
    }

    init: (fn) ->
        fn.call(this)

    observe: (@el) ->
        for type in Object.keys(@events)
            @el.addEventListener(type, @delegate(type))

    add: (obj) ->
        for query, fn of obj
            match = query.match(eventRegExp)
            type = if match then match[1] else query
            selector = if match then match[2] else ''
            @events[type][selector] = fn
        return obj

    delegate: (type) ->
        return (e) =>
            el = e.target
            while el and el isnt @el
                for selector, fn of @events[type]
                    fn.call(this, e, el) if el.matches(selector)
                el = el.parentNode
}
