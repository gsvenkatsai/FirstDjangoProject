import uuid
from django.db import migrations, models

def populate_uuid(apps, schema_editor):
    Cart = apps.get_model('store', 'Cart')
    for cart in Cart.objects.all():
        # Assign a new UUID to each row
        cart.id = uuid.uuid4()
        cart.save(update_fields=['id'])

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_orderitem_product_alter_product_collection_and_more'),  # replace with your last migration
    ]

    operations = [
        # Step 1: Assign new UUIDs
        migrations.RunPython(populate_uuid),

        # Step 2: Alter the field type
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False),
        ),
    ]
