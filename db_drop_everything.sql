-- Drop tables and views
drop table users cascade;
drop table events cascade;
drop table todos cascade;
drop table votes cascade;
drop table confirmed_score_log cascade;

drop function check_voting_completion;
drop view events_and_votes_master_view;