from store.signals.__init__ import order_created
from django.dispatch import Signal
def on_order_created(sender, **kwargs):
    print(kwargs['order'])