# Generated by Django 3.1.7 on 2021-08-02 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_player_club'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='participation',
        ),
        migrations.AddField(
            model_name='discipline',
            name='discipline_gender',
            field=models.CharField(choices=[('W', 'Women'), ('M', 'Men'), ('MXD', 'Mixed')], default='W', max_length=3),
        ),
        migrations.AddField(
            model_name='player',
            name='disciplines',
            field=models.ManyToManyField(related_name='participants', to='core.Discipline'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplines', to='core.sport'),
        ),
        migrations.AlterField(
            model_name='player',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='core.club'),
        ),
    ]
