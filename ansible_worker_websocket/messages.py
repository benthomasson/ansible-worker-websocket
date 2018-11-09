
from collections import namedtuple


def serialize(message):
    return [message.__class__.__name__, dict(message._asdict())]


Deploy = namedtuple('Deploy', ['data'])
Complete = namedtuple('Complete', [])
Error = namedtuple('Error', [])
RunnerStdout = namedtuple('RunnerStdout', ['data'])
RunnerMessage = namedtuple('RunnerMessage', ['data'])
