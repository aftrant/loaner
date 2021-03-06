# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Loaner Sync User Lib."""

import logging

from loaner.web_app import constants
from loaner.web_app.backend.auth import permissions
from loaner.web_app.backend.clients import directory
from loaner.web_app.backend.models import user_model

_DIR_CALL_INVALID_MSG = (
    'The call to the Directory client is invalid because: %s.')


class Error(Exception):
  """Default error class for this module."""


class InvalidCallToDirectoryError(Error):
  """Raised when the call to Directory client is invalid."""


def sync_user_roles():
  """Syncs all of the elevated user roles for each user in Google groups."""
  logging.info(
      'Using admin account (%s) to sync users.', constants.ADMIN_USERNAME)
  directory_client = directory.DirectoryApiClient(
      user_email=constants.ADMIN_USERNAME)
  technical_admin_users_from_group = _get_users_directory(
      constants.TECHNICAL_ADMINS_GROUP, directory_client)
  operational_admin_users_from_group = _get_users_directory(
      constants.OPERATIONAL_ADMINS_GROUP, directory_client)
  technician_users_from_group = _get_users_directory(
      constants.TECHNICIANS_GROUP, directory_client)

  ndb_technical_admin_users = (
      user_model.User.query(user_model.User.roles.IN(
          [permissions.TECHNICAL_ADMIN_ROLE.name])).fetch(keys_only=True))
  ndb_operational_admin_users = (
      user_model.User.query(user_model.User.roles.IN(
          [permissions.OPERATIONAL_ADMIN_ROLE.name])).fetch(keys_only=True))
  ndb_technician_users = (
      user_model.User.query(user_model.User.roles.IN(
          [permissions.TECHNICIAN_ROLE.name])).fetch(keys_only=True))
  _add_or_remove_user_roles(
      users_keys=ndb_technical_admin_users,
      group_users=technical_admin_users_from_group,
      role=permissions.TECHNICAL_ADMIN_ROLE.name)
  _add_or_remove_user_roles(
      users_keys=ndb_operational_admin_users,
      group_users=operational_admin_users_from_group,
      role=permissions.OPERATIONAL_ADMIN_ROLE.name)
  _add_or_remove_user_roles(
      users_keys=ndb_technician_users,
      group_users=technician_users_from_group,
      role=permissions.TECHNICIAN_ROLE.name)


def _get_users_directory(group_email, client):
  """Get all users from given Google Group.

  Args:
    group_email: str, the email used to retrieve a paged list of users.
    client: the directory client used to call the Directory API.

  Returns:
    user_group: a list of users for the group.
  """
  try:
    response = client.users_in_group(group_email=group_email)
  except directory.DirectoryRPCError as err:
    raise InvalidCallToDirectoryError(
        _DIR_CALL_INVALID_MSG % str(err))
  user_group = []
  while 'nextPageToken' in response:
    for member in response['members']:
      user_group.append(member['email'])
    try:
      response = client.users_in_group(
          group_email=group_email, page_token=response.get('nextPageToken'))
    except directory.DirectoryRPCError as err:
      raise InvalidCallToDirectoryError(
          _DIR_CALL_INVALID_MSG % str(err))
  if 'nextPageToken' not in response:
    for member in response['members']:
      user_group.append(member['email'])
  return user_group


def _add_or_remove_user_roles(users_keys, group_users, role):
  """Add or remove a user's role based on Google group membership.

  This will check the datastore users that are passed (ndb_users) against the
  users in the Google group that are passed (group_users). It will do nothing
  with the union of both. It will add the given role to the users that are in
  the Google group and not in the datastore users (creating a user object in
  datastore if nessesary). Similarly, it will remove the user permissions if
  the ndb_users are not in group_users.

  Args:
    users_keys: user_model.User obj, the user object keys from datastore.
    group_users: list, a list of users from a Google Group.
    role: str, the role to add or remove from user.
  """
  ndb_user_ids = [user.id() for user in users_keys]
  users_to_add_role = set(group_users) - set(ndb_user_ids)
  users_to_remove_role = set(ndb_user_ids) - set(group_users)
  for user_email in users_to_add_role:
    user = user_model.User.get_user(email=user_email)
    user.roles.append(role)
    user.put()
  for user_email in users_to_remove_role:
    user = user_model.User.get_by_id(user_email)
    user.roles.remove(role)
    user.put()
