from main import ma

class DiarySchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "date", "user_id")

diary_schema = DiarySchema()

diaries_schema = DiarySchema(many=True)
