#!/usr/bin/env python3
"""Generates example/input/* for an INVENTED bookshop app. Values are computed here from invented rows.
The scenario is the design case: an existing app, a mock with a new "Shipping estimate" panel, and a data
model that lacks what the panel needs. Proposed things are marked status: "proposed"."""
import json,os
O=os.path.join(os.path.dirname(os.path.abspath(__file__)),'input');os.makedirs(O,exist_ok=True)
w=lambda n,v:json.dump(v,open(f'{O}/{n}','w'),indent=1)
C=[dict(id=1,name='Ada Fake',zone='A'),dict(id=2,name='Bo Fake',zone='B'),dict(id=3,name='Cy Fake',zone='A')];N={c['id']:c for c in C}
OR=[(101,1,1,'paid',40),(102,1,1,'paid',25),(103,2,1,'paid',60),(104,3,1,'paid',15),(105,2,1,'refunded',30),(106,3,1,'paid',20),(107,None,1,'paid',55),(108,1,2,'paid',90)]
s0=[dict(record_id=str(i),customer_id=c,store_id=s,status=st,total=t) for i,c,s,st,t in OR]
s1=[dict(r,customer=N[r['customer_id']]['name']) for r in s0 if r['customer_id']]
s2=[r for r in s1 if r['store_id']==1];s3=[r for r in s2 if r['status']=='paid']
ids=lambda a,b:[r['record_id'] for r in a if r['record_id'] not in {x['record_id'] for x in b}]
tot={}
for r in s3:
    e=tot.setdefault(r['customer_id'],dict(customer_id=r['customer_id'],customer=r['customer'],order_count=0,total=0));e['order_count']+=1;e['total']+=r['total']
totals=list(tot.values());zones=[dict(customer_id=c['id'],shipping_zone=c['zone']) for c in C];RATE={'A':4,'B':7}
out=[dict(t,estimate=RATE[N[t['customer_id']]['zone']]*t['order_count']) for t in totals];rev=sum(t['total'] for t in totals)
roles=[('manager','manager',True),('clerk','clerk',False)]
def st(tag,rows):return dict(tag=tag,row_count=len(rows),rows=rows)
for rk,_,can in roles:
    resp=dict(revenueTotal=rev if can else None,orderCount=len(s3),customers=out)
    T=dict(s1=dict(vars=dict(canSeeRevenue=can)),s2=dict(stages=[st('from orders',s0),st('join customers',s1),st('where store',s2),st('where paid',s3)]),s3=dict(stages=[st('group by customer',totals)]),s4=dict(stages=[st('from customers',zones)]),s5=dict(vars=dict(customersOut=out)),s6=dict(vars=dict(response=resp)),c1=dict(vars=dict(heroTotal=f'${rev}' if can else '—')),c2=dict(vars=dict(rowsOut=[dict(name=t['customer'],total=f"${t['total']}",estimate=f"${t['estimate']}") for t in out])))
    for k,v in T.items():w(f'trace_{rk}_{k}.json',dict(step=k,**v))
F='src/orders/summary.js'
R={r:len(x) for r,x in [('a',s0)]}
both=lambda v:{'manager':v,'clerk':v}
model=dict(provenance='Invented example app. Values computed from invented rows.',roles=[dict(key=a,label=b) for a,b,_ in roles],endpoint=dict(method='GET',path='/api/stores/:id/summary',handler=F+':12'),
 steps=[dict(n=1,id='s1',op='call',text='Check whether this role may see revenue',side='server',at=F+':14',reads=['app.roles.can_see_revenue'],flag=None),
  dict(n=2,id='s2',op='query',text='Load this store’s paid orders',side='server',at=F+':18',reads=['app.orders.id','app.orders.customer_id','app.orders.store_id','app.orders.status','app.orders.total','app.customers.id','app.customers.name'],flag='Orders with no customer are dropped silently by the inner join.'),
  dict(n=3,id='s3',op='group',text='Total and count per customer',side='server',at=F+':31',reads=[],flag=None),
  dict(n=4,id='s4',op='query',text='Look up each customer’s shipping zone',side='server',at='(to build)',reads=['app.customers.shipping_zone'],status='proposed',flag=None),
  dict(n=5,id='s5',op='map',text='Attach a shipping estimate per customer',side='server',at='(to build)',reads=[],status='proposed',flag=None),
  dict(n=6,id='s6',op='format',text='Send revenue, count and customers',side='server',at=F+':40',reads=[],flag=None),
  dict(n=7,id='c1',op='format',text='Show revenue in the header',side='browser',at='web/Summary.tsx:22',reads=[],flag=None),
  dict(n=8,id='c2',op='map',text='Render one row per customer',side='browser',at='web/Summary.tsx:30',reads=[],flag=None)],
 work=[dict(name='canSeeRevenue',step=1,kind='boolean',type='boolean'),dict(name='orders',step=2,kind='list',type='{record_id, customer, status, total}[]'),dict(name='totals',step=3,kind='list',type='{customer_id, customer, order_count, total}[]'),dict(name='zones',step=4,kind='list',type='{customer_id, shipping_zone}[]'),dict(name='customersOut',step=5,kind='list',type='{…totals, estimate}[]'),dict(name='response',step=6,kind='object',type='{revenueTotal, orderCount, customers}'),dict(name='heroTotal',step=7,kind='string',type='string'),dict(name='rowsOut',step=8,kind='list',type='{name, total, estimate}[]')],
 payload=[dict(group='Response',field='revenueTotal',final={'manager':rev,'clerk':None},via=[dict(var='orders',step=2,why='Paid orders in this store',at=F+':18',focusCols=['total']),dict(var='totals',step=3,why='Summed per customer',at=F+':31',focusCols=['total']),dict(var='canSeeRevenue',step=1,why='Hidden unless the role may see it',at=F+':14'),dict(var='response',step=6,why='Sum of all customer totals',at=F+':41')]),
  dict(group='Response',field='orderCount',final=both(len(s3)),via=[dict(var='orders',step=2,why='Paid orders in this store',at=F+':18'),dict(var='response',step=6,why='Length of the list',at=F+':42')]),
  dict(group='Customer row (Ada Fake)',token='Ada',field='customers[].total',final=both(tot[1]['total']),via=[dict(var='orders',step=2,why='Ada’s paid orders',at=F+':18',focusCols=['total']),dict(var='totals',step=3,why='Summed',at=F+':31',focusCols=['total']),dict(var='customersOut',step=5,why='Carried through',at='(to build)'),dict(var='response',step=6,why='Sent',at=F+':43')]),
  dict(group='Customer row (Ada Fake)',token='Ada',field='customers[].estimate',status='proposed',final=both(out[0]['estimate']),via=[dict(var='totals',step=3,why='How many orders',at=F+':31',focusCols=['order_count']),dict(var='zones',step=4,why='Needs a column that doesn’t exist yet',at='(to build)',focusCols=['shipping_zone']),dict(var='customersOut',step=5,why='Zone rate × order count',at='(to build)',focusCols=['estimate']),dict(var='response',step=6,why='Sent',at=F+':43')]),
  dict(group='Browser',field='header revenue',final={'manager':f'${rev}','clerk':'—'},via=[dict(var='response',step=6,why='revenueTotal',at=F+':41'),dict(var='heroTotal',step=7,why='Formatted; a dash when hidden',at='web/Summary.tsx:22')])],
 queries=[dict(steps=[2],stages=[dict(tag='from',plain='Start with every order.',use=['app.orders.id','app.orders.customer_id','app.orders.store_id','app.orders.status','app.orders.total'],rows=both(len(s0)),why=None),dict(tag='join',plain='Attach the customer’s name.',use=['app.orders.customer_id','app.customers.id','app.customers.name'],rows=both(len(s1)),why='Order 107 has no customer, so it silently disappears.'),dict(tag='where',plain='Keep this store only.',use=['app.orders.store_id'],rows=both(len(s2)),why='Order 108 belongs to another store.'),dict(tag='where',plain='Keep paid orders only.',use=['app.orders.status'],rows=both(len(s3)),why='Order 105 was refunded.')]),dict(steps=[3],stages=[dict(tag='group',plain='Collapse to one row per customer and add up.',use=[],rows=both(len(totals)),why=None)]),dict(steps=[4],stages=[dict(tag='from',plain='Read each customer’s zone (column to be added).',use=['app.customers.shipping_zone'],rows=both(len(zones)),why=None)])],
 unresolved=['Who sets shipping_zone for existing customers? The mock doesn’t say.','Are the zone rates in the data model or in config?'])
w('model.json',model)
w('tables.json',[dict(id='app.orders',file='schema/orders.ts',columns=[dict(name=n) for n in ['id','customer_id','store_id','status','total']]),dict(id='app.customers',file='schema/customers.ts',columns=[dict(name='id'),dict(name='name'),dict(name='shipping_zone',status='proposed',type='new column')]),dict(id='app.roles',file='schema/roles.ts',columns=[dict(name='id'),dict(name='can_see_revenue')]),dict(id='app.shipping_rates',status='proposed',columns=[dict(name='zone',status='proposed'),dict(name='rate',status='proposed')])])
w('screen.json',dict(regions=[dict(id='hero',label='Header: revenue and order count',implementedBy='web/Summary.tsx:22'),dict(id='cust',label='Customers table',implementedBy='web/Summary.tsx:30'),dict(id='ship',label='Shipping estimate panel',implementedBy=None)],lit=['hero','cust','ship']))
print('ok')
