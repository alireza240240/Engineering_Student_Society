from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True) # in toy model news goftim ama age nbshe serlzr to jsom autor=1 mizr msln primarykeyralatedfield hast pishfarzsh ma miaim migim string bde
    # va inke read only hst ke fght to get bre to post nre ke karbar ke login hast khokar sbt she
    # va inke mghdar __str__ model User ro mide

    class Meta :
        model = News
        fields = ['id','title','content','created_at','author']
        # read_only_fields = ['id', 'created_at', 'author'] # age to Post Khast ino mzrm ke nkhd