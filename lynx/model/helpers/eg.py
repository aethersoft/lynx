import json

__all__ = [
    'project',
    'document',
    'document_many',
    'task',
    'user',
    'user_roles',
]

project = json.dumps({
    'name': 'Project 1',
    'description': 'Added by Swagger Examples'
})

document = json.dumps({
    'text': 'the quick brown fox jumps over the lazy dog',
    'meta': {}
})

document_many = json.dumps([{
    'text': 'the quick brown fox jumps over the lazy dog',
    'meta': {}
}, {
    'text': 'she sells sea shells by the sea shore',
    'meta': {}
}, ])

task = json.dumps({
    'name': 'Task 1',
    'description': 'Added by Swagger Examples',
    'type': 'document_labeling',
    'labels': [
        {
            'label': 'Positive',
            'properties': {
                'color': 'black',
                'background': 'white',
            }
        },
        {
            'label': 'Negative',
            'properties': {
                'color': 'black',
                'background': 'white',
            }
        }
    ]
})

user = json.dumps({
    'username': 'admin@example.com',
    'password': 'sample_password',
    'first_name': 'admin',
    'last_name': 'example',
    'email': 'admin@example.com',
})

user_roles = json.dumps({
    'username': 'admin@example.com',
    'role': 'project_admin',
})
