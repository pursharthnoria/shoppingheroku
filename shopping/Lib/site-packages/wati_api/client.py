# Copyright (c) 2020 kien@clare.ai.
# All Rights Reserved.

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json
import logging
import time

import requests

from wati_api import http
from wati_api import utils

LOG = logging.getLogger(__name__)


class Client(http.HTTPClient):
    """Client for the WATI API.
    :param endpoint: A user-supplied endpoint URL for the WATI service.
    :param token: A token get from: https://app.wati.io/register
    """

    def __init__(self, endpoint, token, **kwargs):
        """Initialize a new client for the WATI API."""
        super(Client, self).__init__(endpoint, **kwargs)
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    def get_messages(self, whatsapp_number, page_size=None, page_number=None):
        """Get Messages by whatsapp number

        :param whatsapp_number(str): Whatsapp Number
        :param page_size(int): Page size
        :param page_number(int): Page number
        """
        url = utils.generate_url('/api/v1/getMessages/', whatsapp_number,
                                 pageSize=page_size,
                                 pageNumber=page_number)
        return self.get(url, headers=self.headers).json()

    def get_message_templates(self, page_size=None, page_number=None):
        """Get Message Templates

        :param page_size(int): Page size
        :param page_number(int): Page number
        """
        url = utils.generate_url('/api/v1/getMessageTemplates',
                                 pageSize=page_size,
                                 pageNumber=page_number)
        return self.get(url, headers=self.headers).json()

    def get_contacts(self, page_size=None, page_number=None,
                     name=None, attribute=None, createdDate=None):
        """Get Contacts List

        :param page_size(int): Page size
        :param page_number(int): Page number
        :param name(str): Contact name
        :param attribute(string): Attribute (parameters format:
                [{name: "name", operator: "contain", value: "test"}] )
        :poram createdData(str): Created Date (YYYY-MM-DD or MM-DD-YYYY)
        """
        url = utils.generate_url('/api/v1/getContacts',
                                 pageSize=page_size,
                                 pageNumber=page_number,
                                 name=name, attribute=attribute,
                                 createdDate=createdDate)
        return self.get(url, headers=self.headers).json()

    def get_media(self, file_name):
        """Get media by file name

        param file_name(str): File name
        """
        url = utils.generate_url('/api/v1/getMedia', fileName=file_name)
        return self.get(url, headers=self.headers, stream=True).raw

    def update_contact_attributes(self, whatsapp_number, custom_params):
        """Update Contact Attributes

        :param whatsapp_number(str): Whatsapp number
        :param custom_params(list):
                [
                    {
                    "name": "string",
                    "value": "string"
                    }
                ]
        """
        payload = {
            "customParams": custom_params
        }
        url = utils.generate_url(
            '/api/v1/updateContactAttributes', whatsapp_number)
        return self.post(url, headers=self.headers,
                         body=payload).json()

    def add_contact(self, whatsapp_number, name, custom_params):
        """Add Contact

        :param whatsapp_number(str): Whatsapp number
        :param name(str):
        :param custom_params(list):
                [
                    {
                    "name": "string",
                    "value": "string"
                    }
                ]
        """
        payload = {
            "name": name,
            "customParams": custom_params
        }
        url = utils.generate_url('/api/v1/addContact', whatsapp_number)
        return self.post(url, headers=self.headers,
                         body=payload).json()

    def send_session_message(self, whatsapp_number, message_text):
        """Send Message to opened session

        :param whatsapp_number(str): Whatsapp number
        :param message_text(str): Message
        """
        url = utils.generate_url('/api/v1/sendSessionMessage', whatsapp_number,
                                 messageText=message_text)
        return self.post(url, headers=self.headers).json()

    def send_template_message_csv(self, template_name, broadcast_name,
                                  whatsapp_number_csv):
        """Send template messages (CSV)

        :param template_name(str): Defined in the Template Message under
                                   Broadcast
        :param broadcast_name(str): Broadcast name
        :param whatsapp_number_csv(str): Csv file absolute path
        """
        url = utils.generate_url('/api/v1/sendTemplateMessageCSV',
                                 template_name=template_name,
                                 broadcast_name=broadcast_name)
        headers = {
            'Authorization': self.headers['Authorization'],
            'Content-Type': 'multipart/form-data'
        }
        files = {'file': open(whatsapp_number_csv).read()}
        return self.post(url, headers=headers,
                         files=files).json()

    def send_template_message(self, whatsapp_number, broadcast_name,
                              template_name, template_parameters):
        """Send message templates"""
        url = utils.generate_url(
            '/api/v1/sendTemplateMessage/', whatsapp_number)
        payload = {
            "template_name": template_name,
            "broadcast_name": broadcast_name,
            "parameters": json.dumps(template_parameters)
        }
        return self.post(url, body=payload, headers=self.headers).json()
