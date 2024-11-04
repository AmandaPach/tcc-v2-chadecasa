from django import template
import re

register = template.Library()


@register.filter
def format_date(date_str):
    # 2024-11-02 00:00:00-03:00
    formated_pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    javascript_pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")

    if date_str.endswith("-03:00"):
        date_str = date_str[:-6]
    if formated_pattern.match(date_str):
        date = date_str.split(" ")[0]
        ano, mes, dia = date.split("-")
        return f"{dia}/{mes}/{ano}"
    elif javascript_pattern.match(date_str):
        date, time = date_str.split("T")
        ano, mes, dia = date.split("-")
        return f"{dia}/{mes}/{ano}"