#提取18日加入购物车的，去除没有过购买行为的人
select t4.user_id as user_id ,t4.item_id as item_id 
from
(select distinct *
from
(
SELECT t1.user_id,t1.item_id,t1.behavior_type,t1.time,ifnull(t2.user_id,"no id") as t2id
from
(
select *
FROM tianchi.newtable
where behavior_type=3 and time > '2014-12-18' and time < '2014-12-19' 
) as t1
LEFT JOIN 
(
select *
from tianchi.newtable 
where behavior_type=4 and time > '2014-12-18' and time < '2014-12-19'
)
as t2
on (t1.user_id = t2.user_id and t1.item_id=t2.item_id)
)as t3
where t2id = 'no id' 
) aa
inner join
(select user_id,item_id,sum(behavior_type) as con
from newtable
where time > '2014-12-18' and time < '2014-12-19'
group by user_id,item_id
)as t4
on t4.user_id=aa.user_id and t4.item_id = aa.item_id
where con>4
