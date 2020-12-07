from django import template

# 自定义序号累加

register = template.Library()


@register.filter
def my_multiply(value, num):
    # 定义一个乘法过滤器
    try:
        int_va = int(value)
        res = (int_va - 1) * num
        return res
    except Exception as e:
        print(str(e))

