import time
import json
from datetime import date,timedelta

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string


from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import proper_paginate
from .models import  Region, Product, Client, SalesMan,Transaction,Voucher


dic = {}
serial = []
pairs = []

def cmp(client):
		return dic[client]


def index(request):
	today 		= date.today()
	qs			= Transaction.objects.all()
	qyear		= qs.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)
	qmonth		= qs.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
	qweek		= qs.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)


	# begin & end
	weekBegin		= today - timedelta(days = 6)
	weekEnd			= today

	weekTransaction	= len(qweek)
	salesAmount		= 0
	data			= [0]*7
	amount 			= [0]*7
	for i in qweek:
		v 				= i.voucher.date - weekBegin
		data[v.days]	= data[v.days] + 1
		amount[v.days]	= amount[v.days] + i.amount
		salesAmount		= salesAmount + i.amount


	labels			= []
	temp 			= weekBegin
	while temp <= weekEnd:
		labels.append(temp.strftime('%a'))
		temp = temp + timedelta(days = 1)



	#month data
	monthBegin 			= today - timedelta(days = 29)
	monthEnd			= today
	monthTransaction	= len(qmonth)
	monthSales			= 0
	monthAmount			= [0]*30
	monthTransactionList	= [0]*30
	for i in qmonth	:
		monthSales += i.amount
		v = i.voucher.date - monthBegin
		monthAmount[v.days] += i.amount
		monthTransactionList[v.days] += 1

	monthLabels			= []
	temp 			= monthBegin
	while(temp <= monthEnd) :
		monthLabels.append(temp.strftime('%d'))
		temp 	= temp + timedelta(days = 1)


	#year data
	yearBegin			= today.replace(month = 1, day = 1)
	yearEnd				= today
	yearTransaction		= len(qyear)
	yearSales			= 0
	yearAmount			= [0]*(today.month)
	yearTransactionList = [0]*(today.month)
	for i in qyear:
		yearSales += i.amount
		yearAmount[i.voucher.date.month-1] += i.amount
		yearTransactionList[i.voucher.date.month-1] += 1

	yearLabels 			= []
	temp 		= today.replace(month = 1, day = 1)
	while(temp <= today) :
		yearLabels.append(temp.strftime('%b'))
		temp = temp + timedelta(days = 32)



	latest		= qs.order_by('-voucher__date')[:10]
	latestPaginator	= Paginator(latest, 10)
	context		= {
		'weekBegin'			: weekBegin,
		'weekEnd'			: weekEnd,
		'weekTransaction' 	: weekTransaction,
		'salesAmount'		: salesAmount,
		'weekReport'		: {
				'labels'	: json.dumps(labels),
				'transaction'		: data,
				'amount'	: amount,
		},

		'monthBegin'		: monthBegin,
		'monthEnd'			: monthEnd,
		'monthSales'		: monthSales,
		'monthTransaction'	: monthTransaction,
		'monthTransactionList' : monthTransactionList,
		'monthReport'		: {
			'labels'		: json.dumps(monthLabels),
			'transaction'	: monthTransactionList,
			'amount'	: monthAmount,
		},

		'yearBegin'			: yearBegin,
		'yearEnd'			: yearEnd,
		'yearSales'			: yearSales,
		'yearTransaction'	: yearTransaction,


		'yearReport'		: {
			'labels'		: json.dumps(yearLabels),
			'transaction'	: yearTransactionList,
			'amount'		: yearAmount,
		},

		'latestTransaction'	: latest,
	}


	return render(request, 'main/index.html', context)





def clients(request):
	today 		= date.today()
	qs			= Transaction.objects.all()
	qyear		= qs.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)
	qmonth		= qs.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
	qweek		= qs.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)


	# begin & end
	weekBegin		= today - timedelta(days = 6)
	weekEnd			= today
	monthBegin 		= today - timedelta(days = 29)
	monthEnd		= today
	yearBegin		= today.replace(month = 1, day = 1)
	yearEnd			= today
	context		= {
		'weekBegin'			: weekBegin,
		'weekEnd'			: weekEnd,
		'monthBegin'		: monthBegin,
		'monthEnd'			: monthEnd,
		'yearBegin'			: yearBegin,
		'yearEnd'			: yearEnd,
	}
	return render(request, 'main/clients.html', context)


class ChartData(APIView):
	authentication_classes 	= []
	permission_classes 		= []
	def get(self, request, *args, **kwargs) :
		populate()

		paginator = Paginator(pairs, 10)
		page = kwargs.get('page_id', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)


		data = {
			'labels': [x.id for x,y in users],
			'data'	: [y for x,y in users],

		}
		return Response(data)

class Check(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		print(render(request,'main/base.html'))
		data = {
			'labels': [1,2,3,4],
			'data'	: [10,20,30,40],
			'div'	: render_to_string('main/index.html',),

		}
		return Response(data)


class LatestPurchase(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :

		page 	= kwargs.get('page',1)
		qs		= Transaction.objects.all()
		latest  = qs.order_by('-voucher__date')
		paginator = Paginator(latest, 10)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)

		print(users)
		data = {
			'LatestPurchase': render_to_string('main/includes/transactiontable.html', {'transaction': users,}),
			'latestPaginator': render_to_string('main/includes/Paginator.html', {'page': users, 'page_range': pg })

		}
		return Response(data)


class LatestClient(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		today = date.today()
		table 	= kwargs['type']
		if(table == None):
			return None

		query = []
		if table == 'week':
			query	= Transaction.objects.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)
		elif table == 'month':
			query	= Transaction.objects.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
		else:
			query	= Transaction.objects.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)

		for c in Client.objects.all():dic[c] = 0
		for i in query:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		yearTable 	= [(i, dic[i])  for i in serial]
		yearData	= [ dic[i] for i in serial]

		paginator = Paginator(yearTable, 10)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageYear = paginator.page(page)
		except PageNotAnInteger:
			pageYear = paginator.page(1)
		except EmptyPage:
			pageYear = paginator.page(paginator.num_pages)


		data = {
			'Table'		: render_to_string('main/includes/clientTable.html', {'page' : pageYear}),
			'Data'		: yearData[pageYear.start_index()-1: pageYear.end_index()],
			'Labels'	: [' ']*(pageYear.end_index()- pageYear.start_index() + 1),
			'Paginator': render_to_string('main/includes/Paginator.html', {'page': pageYear, 'page_range': pg })

		}



		return Response(data)


class LoadDefaultClients(APIView):
	authentication_classes 	= []
	permission_classes 		= []

	def get(self, request, *args, **kwargs) :
		today = date.today()
		qs			= Transaction.objects.all()
		qyear		= qs.filter(voucher__date__gte = today.replace(month=1, day=1), voucher__date__lte = today)
		qmonth		= qs.filter(voucher__date__gte = today - timedelta(days = 30), voucher__date__lte = today)
		qweek		= qs.filter(voucher__date__gte = today - timedelta(days = 7) , voucher__date__lte = today)


		for c in Client.objects.all():dic[c] = 0
		for i in qyear:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		yearTable 	= [(i, dic[i])  for i in serial]
		yearData	= [ dic[i] for i in serial]

		paginator = Paginator(yearTable, 10)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageYear = paginator.page(page)
		except PageNotAnInteger:
			pageYear = paginator.page(1)
		except EmptyPage:
			pageYear = paginator.page(paginator.num_pages)


		for c in Client.objects.all():dic[c] = 0
		for i in qweek:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		weekTable 	= [(i, dic[i])  for i in serial]
		weekData	= [ dic[i] for i in serial]

		paginator = Paginator(weekTable, 10)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pageWeek = paginator.page(page)
		except PageNotAnInteger:
			pageWeek = paginator.page(1)
		except EmptyPage:
			pageWeek = paginator.page(paginator.num_pages)


		for c in Client.objects.all():dic[c] = 0
		for i in qmonth:dic[i.voucher.client] += i.amount
		serial 		= sorted(Client.objects.all(), key=cmp, reverse = True)
		monthTable 	= [(i, dic[i])  for i in serial]
		monthData	= [ dic[i] for i in serial]

		paginator = Paginator(monthTable, 10)
		page = kwargs.get('page', 1)
		pg = proper_paginate(paginator, int(page))

		try:
			pagemonth = paginator.page(page)
		except PageNotAnInteger:
			pagemonth = paginator.page(1)
		except EmptyPage:
			pagemonth = paginator.page(paginator.num_pages)




		data = {
			'yearTable'		: render_to_string('main/includes/clientTable.html', {'page' : pageYear}),
			'yearData'		: yearData[pageYear.start_index()-1: pageYear.end_index()],
			'yearLabels'	: [' ']*(pageYear.end_index()- pageYear.start_index() + 1),
			'yearPaginator': render_to_string('main/includes/Paginator.html', {'page': pageYear, 'page_range': pg }),

			'weekTable'		: render_to_string('main/includes/clientTable.html', {'page' : pageWeek}),
			'weekData'		: yearData[pageWeek.start_index()-1: pageWeek.end_index()],
			'weekLabels'	: [' ']*(pageWeek.end_index()- pageWeek.start_index() + 1),
			'weekPaginator': render_to_string('main/includes/Paginator.html', {'page': pageWeek, 'page_range': pg }),

			'monthTable'		: render_to_string('main/includes/clientTable.html', {'page' : pagemonth}),
			'monthData'		: yearData[pagemonth.start_index()-1: pagemonth.end_index()],
			'monthLabels'	: [' ']*(pagemonth.end_index()- pagemonth.start_index() + 1),
			'monthPaginator': render_to_string('main/includes/Paginator.html', {'page': pagemonth, 'page_range': pg }),

		}



		return Response(data)



