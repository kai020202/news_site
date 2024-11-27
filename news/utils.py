from .models import ViewCount

def increment_view_count():
    record = ViewCount.objects.first()

    record.view_count += 1
    record.save()

    return record.view_count

# 1,viewsでview_count = increment_view_count()を実行
# 2 record.view_count += 1
#    record.save()でカウントを保存
# 3 home.htmlのページビュー回数: {{ view_count }}で出力
# 4 再度ホームにアクセスしたら２から
#
