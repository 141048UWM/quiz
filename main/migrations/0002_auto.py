from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='main.category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='main.quiz'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quizzes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quiz_results', to='main.quiz'),
        ),
        migrations.AlterField(
            model_name='quizresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quiz_results', to=settings.AUTH_USER_MODEL),
        ),
    ]
