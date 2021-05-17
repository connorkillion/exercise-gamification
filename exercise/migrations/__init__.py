

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_type', models.CharField(choices=[('CAR', 'cardio'), ('STR', 'strength'), ('SPT', 'sports'), ('FLX', 'yoga/flexibility')], default='CAR', max_length=3, null=True)),
                ('exercise_date', models.DateTimeField(null=True, verbose_name='date completed')),
                ('time_taken', models.IntegerField(default=0, null=True)),
                ('points', models.IntegerField(default=0)),
                ('description', models.CharField(default='daily workout', max_length=200, null=True)),
            ],
        ),
    ]


