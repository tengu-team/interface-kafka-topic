#!/usr/bin/env python3
# Copyright (C) 2016  Ghent University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from charms.reactive import when_any, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import Endpoint


class KafkaTopicRequires(Endpoint):

    @when_any('endpoint.{endpoint_name}.joined')
    def kafka_topic_joined(self):
        set_flag(self.expand_name('available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def kafka_topic_broken(self):
        clear_flag(self.expand_name('available'))

    @when_any('endpoint.{endpoint_name}.changed.topic-info',
              'endpoint.{endpoint_name}.departed')
    def kafka_topic_changed(self):
        set_flag(self.expand_name('new-topic-info'))
        clear_flag(self.expand_name('changed.topic-info'))
        clear_flag(self.expand_name('departed'))

    def get_topics(self):
        """
        [
            {
                'remote_unit_name': str,
                'topic_info': {
                    'name': str,
                    'partitions': int,
                    'replication': int,
                    'compact': boolean,
                }
            }
        ]
        """
        configs = []
        for relation in self.relations:
            for unit in relation.units:
                if 'topic-info' in unit.received:
                    configs.append({
                        'remote_unit_name': unit.unit_name,
                        'topic_info': unit.received['topic-info'],
                    })
        return configs
