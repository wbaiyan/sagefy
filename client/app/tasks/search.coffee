store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    search: ({q, skip = 0, limit = 10, order}) ->
        recorder.emit('search', q)
        if q isnt @data.searchQuery
            @data.searchResults = []
        @data.searchQuery = q
        ajax({
            method: 'GET'
            url: '/s/search'
            data: {q, skip, limit, order}
            done: (response) =>
                @data.searchResults ?= []
                @data.searchResults = mergeArraysByKey(
                    @data.searchResults
                    response.hits
                    'id'
                )
                recorder.emit('search success', q, response.hits.length)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('search failure', errors)
            always: =>
                @change()
        })
})
