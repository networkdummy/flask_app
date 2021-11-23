drop table drill;
drop table question;

create table drill (
	Id 		INT ,
    Title	varchar(400) not null,
    Topic	varchar(400),
    Level	char(12),
    Room	char(13),
    primary key(Id)
    );

create table question (
  Id 			INT ,
  Topic 		VARCHAR(45) NULL,
  QText 		VARCHAR(500) NULL,
  Answer 		VARCHAR(500) NULL,
  Feedback 	VARCHAR(500) NULL,
  primary key(Id)
  );

insert into question values (1001,'Basic Select','Select part P1 and display SNo and Part columns', 'Select SNo, Part from shipment where Part=''P1'';','Keep working hard'); 


create or replace procedure SelectQuestion(qid int)
language sql
as $BODY$
    return query select *
    from question
    where id = qid;
$BODY$;



call SelectQuestion(1001);
select * from shipment;



