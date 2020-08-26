# This test calling from main directory by command `make test`
# If test will complete successful - special IMG will be send to test chat
# Set this chat in (message.json -> chat -> id)

import pytest

from telebot import types
from main import answer_to_photo

data = {}

# Create mock from class <message obj>
@pytest.fixture()
def get_mock_message(request):
	file = open('./tests/message.json', 'r')
	lines = file.readlines()
	jsonstring = ''
	for line in lines:
	    jsonstring += line.rstrip().replace(' ', '')
	file.close()
	mock_message = types.Message.de_json(jsonstring)
	data['mock_message'] = mock_message



def test_answer_to_photo(get_mock_message):
	assert answer_to_photo(data['mock_message']) == "Return for test"
