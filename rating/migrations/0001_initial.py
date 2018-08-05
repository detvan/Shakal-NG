# Generated by Django 2.1 on 2018-08-05 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	initial = True

	dependencies = [
		('contenttypes', '0002_remove_content_type_name'),
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name='Rating',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('value', models.SmallIntegerField(blank=True, null=True, verbose_name='Hodnotenie')),
				('marked_solution', models.BooleanField(default=False, verbose_name='Označené hodnotenie')),
			],
			options={
				'verbose_name_plural': 'Hodnotenia',
				'verbose_name': 'Hodnotenie',
			},
		),
		migrations.CreateModel(
			name='Statistics',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('object_id', models.PositiveIntegerField(verbose_name='ID objektu')),
				('rating_total', models.IntegerField(default=0, verbose_name='Celkové hodnotenie')),
				('rating_count', models.IntegerField(default=0, verbose_name='Počet hodnotiacich hlasov')),
				('solution_count', models.IntegerField(default=0, verbose_name='Počet označení ako riešenie')),
				('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='typ obsahu')),
			],
			options={
				'verbose_name_plural': 'Štatistiky hodnotenia',
				'verbose_name': 'Štatistika hodnotenia',
			},
		),
		migrations.AddField(
			model_name='rating',
			name='statistics',
			field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_set', to='rating.Statistics', verbose_name='Hodnotený objekt'),
		),
		migrations.AddField(
			model_name='rating',
			name='user',
			field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Používateľ'),
		),
		migrations.AlterUniqueTogether(
			name='statistics',
			unique_together={('content_type', 'object_id')},
		),
		migrations.AlterUniqueTogether(
			name='rating',
			unique_together={('statistics', 'user')},
		),
	]