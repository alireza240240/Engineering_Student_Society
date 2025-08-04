

from rest_framework import serializers

from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    # status = serializers.ReadOnlyField() # read_only_fields=[] in khdsh kar in khat ro mkn
    author = serializers.StringRelatedField(read_only=True) # in kht br in ke to jsn pk nd str authr bde ke to mtd __str , par rdonli lzm nbd chn to meta gftm

    class Meta :
        model = Article
        fields = ['id','title','content','status','author','created_at']
        read_only_fields = ['id', 'status', 'author', 'created_at']# status hame read fght admin