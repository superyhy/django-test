from django.db import models


class TbSubject(models.Model):
    no = models.AutoField(primary_key=True, db_comment='学科编号')
    name = models.CharField(max_length=50, db_comment='学科名称')
    intro = models.CharField(max_length=1000, db_comment='学科介绍')
    is_hot = models.IntegerField(db_comment='是不是热门学科')

    class Meta:
        managed = False  # 若你希望 Django 不去管理这个表结构（例如已存在的数据库）
        db_table = 'tb_subject'


class TbTeacher(models.Model):
    no = models.AutoField(primary_key=True, db_comment='老师编号')
    name = models.CharField(max_length=20, db_comment='老师姓名')
    sex = models.IntegerField(db_comment='老师性别')
    birth = models.DateField(db_comment='出生日期')
    intro = models.CharField(max_length=1000, db_comment='老师介绍')
    photo = models.CharField(max_length=255, db_comment='老师照片')
    gcount = models.IntegerField(db_comment='好评数')
    bcount = models.IntegerField(db_comment='差评数')
    sno = models.ForeignKey(
        TbSubject,
        models.DO_NOTHING,
        db_column='sno',
        db_comment='所属学科'
    )

    class Meta:
        managed = False
        db_table = 'tb_teacher'
