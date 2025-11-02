"""Diagnostic script to inspect pycaw AudioUtilities.GetSpeakers() object.
Run this to print the object's type and attributes to help debug initialization issues.
"""
from pycaw.pycaw import AudioUtilities

dev = AudioUtilities.GetSpeakers()
print('repr:', repr(dev))
print('type:', type(dev))
try:
    import inspect
    print('members:', inspect.getmembers(dev)[:30])
except Exception as e:
    print('failed to list members:', e)

print('\nHas Activate?:', hasattr(dev, 'Activate'))
if hasattr(dev, 'Activate'):
    print('Activate callable:', callable(getattr(dev, 'Activate')))
else:
    # try to find similar methods
    names = [n for n in dir(dev) if 'activate' in n.lower()]
    print('activate-like names:', names)
