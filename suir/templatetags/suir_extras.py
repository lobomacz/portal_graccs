from django import template 
import math

register = template.Library()

@register.simple_tag
def grid_range(list, rowsize):
	return range(0, math.ceil(len(list)/rowsize))


@register.simple_tag
def list_slice(lista, fila, por_fila):
	return lista[fila*por_fila:(fila*por_fila)+por_fila]


@register.inclusion_tag('suir/Pagination.html')
def paginador(page_obj, rango_paginas):
	paginas = map(lambda x : int(x) if x != '...' else x, rango_paginas)
	return {'page':page_obj, 'paginas':paginas}
