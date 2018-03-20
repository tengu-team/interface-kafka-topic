# Overview
This interface is used for charms who want to send Kafka topic information.

# Usage
## Requires
By requiring the `kafka-topic` interface, your charm is receiving info about Kafka topics.

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one kafka topic is connected. This state is automatically removed.
- `endpoint.{relation-name}.new-topic-info` is set whenever a change happened in the connected kafka topics. This is triggered when a providing charm sends new/updated info or when a relation departs. This state needs to be **manually removed**.

Use the `get_topics()` method to get all topic info. It returns information in the following format:
```
[
    {
        'remote_unit_name': str,
        'topic_info': {
            'name': str,
            'partitions': int,
            'replication': int,
            'compact': boolean,
        }
    },
    ...
]
```

```python
@when('endpoint.{relation-name}.new-topic-info')
def topics_config():
    endpoint = get_endpoint_from_flag('endpoint.{relation-name}.new-topic-info')
    topics_info = endpoint.get_topics()
    # Do stuff with topics_info
    clear_flag('endpoint.{relation-name}.new-topic-info')
```


## Provides

By providing the `upstream` interface, your charm is providing Kafka topic information. 

This interface layer will set the following states, as appropriate:
- `endpoint.{relation-name}.available` indicates that at least one requirer is connected. This state is automatically removed.

Use `publish_topic_info(topic_info)` to send Kafka topic info. `topic_info` is expected to be a dict with at least the following fields:

```
topic_info = {
    'name': str,
    'partitions': int,
    'replication': int,
    'compact': boolean,
}
```
```python
@when('endpoint.{endpoint-name}.available')
def configure():
    endpoint = get_endpoint_from_flag('endpoint.{endpoint-name}.available')
    
    endpoint.publish_topic_info({
        'name': 'kafka-topic-name',
        'partitions': 25,
        'replication': 3,
        'compact': False,
    })
```


## Authors

This software was created in the [IDLab research group](https://www.ugent.be/ea/idlab) of [Ghent University](https://www.ugent.be) in Belgium. This software is used in [Tengu](https://tengu.io), a project that aims to make experimenting with data frameworks and tools as easy as possible.

 - Sander Borny <sander.borny@ugent.be>

