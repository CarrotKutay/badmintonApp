# Generated by Django 3.1.7 on 2021-07-30 12:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_club_league_ranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='league_pos',
            field=models.IntegerField(help_text='Standing of the league compared to other leagues of its type, e.g. 1st national league, 2nd national league, ...', null=True, verbose_name='League Standing'),
        ),
        migrations.AddField(
            model_name='league',
            name='name',
            field=models.CharField(default='name', max_length=200),
        ),
        migrations.AddField(
            model_name='league',
            name='type',
            field=models.CharField(choices=[('I', 'international'), ('C', 'continental'), ('N', 'national')], default='N', max_length=3),
        ),
        migrations.AddField(
            model_name='ranking',
            name='league',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.league'),
        ),
        migrations.AddField(
            model_name='ranking',
            name='update',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last update'),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.club')),
                ('ranking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.ranking')),
            ],
        ),
    ]
