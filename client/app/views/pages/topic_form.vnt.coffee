broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #topic-form.create form': (e, el) ->
        e.preventDefault() if e
        tasks.createTopic(getFormValues(el))

    'submit #topic-form.update form': (e, el) ->
        e.preventDefault() if e
        tasks.updateTopic(getFormValues(el))
})
