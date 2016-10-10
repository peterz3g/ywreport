--变更工单数据查询
select substr(建单时间,1,10) as 日期,变更类型,应用系统,工单状态, count(*) from VIEW_BO_CHG 
where 建单时间 >='2016-06-01' group by substr(建单时间,1,10),变更类型,应用系统,工单状态 order by 日期;

--xbank事件工单数据查询
select substr(建单时间,1,10) as 日期,'Xbank事件工单',机构号,机构,归属模块,工单状态, count(*) from view_bo_xbank_event 
where 建单时间 >='2016-06-01' group by substr(建单时间,1,10), 机构号,机构,归属模块,工单状态 order by 日期;

--变更工单分析，增加紧急变更原因属性
--紧急工单:1-按时间总量趋势;2-单天按原因饼图;3-系统状态分类柱状竖排名.
--常规工单:1-按时间总量趋势;2-系统状态分类柱状竖排名;3-工单某系统状态分布饼图.---已完成,可进行改造
select substr(建单时间,1,10) as 日期,变更类型,应用系统,工单状态,紧急变更原因属性, count(*) from VIEW_BO_CHG 
where 建单时间 >='2016-06-01' group by substr(建单时间,1,10),变更类型,应用系统,工单状态,紧急变更原因属性 order by 日期;

--参数修改单分析
--1-按时间总量趋势;2-单天按原因饼图;3-系统状态分类柱状竖排名.
select substr(建单时间,1,10) as 日期,修改类型,业务系统,分类,工单状态,修改原因, count(*) from VIEW_BO_PARA_MOD
where 建单时间 >='2016-06-01' group by substr(建单时间,1,10),修改类型,业务系统,分类,工单状态,修改原因;


--

select substr(建单时间,1,10) as 日期,变更类型,应用系统,紧急变更原因属性,工单状态, count(*) from VIEW_BO_CHG 
where 建单时间 >='2016-06-01' and 变更类型='紧急变更' group by substr(建单时间,1,10),变更类型,应用系统,紧急变更原因属性,工单状态 order by 日期;

select distinct(紧急变更判断属性) from VIEW_BO_CHG 
where 建单时间 >='2016-08-01' and 变更类型='紧急变更' ;



select distinct(紧急变更原因说明) from VIEW_BO_CHG 
where 建单时间 >='2016-08-01' and 变更类型='紧急变更' ;

select a.*,b.*,c.* from view_bo_pro a, view_bo_pro_rl b, view_bo_rl_qc c
where a.流水号=b.工单流水号 and b.工单流水号=c.流水号

--参数修改原因分析
select * from VIEW_BO_PARA_MOD where 建单时间 >='2016-08-01'




