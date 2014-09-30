# coding: utf8
db2.define_table('member',
                 Field('id_no','integer'),
                 Field('name', 'string','length=21'),
                 Field('first_name', 'string', 'length=21'),
                 Field('minst', 'string', 'length=7'),
                 Field('address','string', 'length=35'),
                 Field('zip','string', 'length=10'),
                 Field('stat','string','length=3'),
                 primarykey = ['id_no'],
                 migrate = False)
